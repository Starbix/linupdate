# coding: utf-8

# Import libraries
import apt
import subprocess
from colorama import Fore, Back, Style

class Apt:
    def __init__(self):
        # Unhold all packages
        self.unholdAll()

        # Create an instance of the apt cache
        self.aptcache = apt.Cache()

        # self.aptcache.update()
        self.aptcache.open(None)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return list of installed apt packages, sorted by name
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getInstalledPackages(self):
        list = []

        # Loop through all installed packages
        for pkg in self.aptcache:
            # If the package is installed, add it to the list of installed packages
            if pkg.is_installed:
                myPackage = {
                    'name': pkg.name,
                    'version': pkg.installed.version,
                }

                list.append(myPackage)
        
        # Sort the list by package name
        list.sort(key=lambda x: x['name'])

        return list


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return list of available apt packages, sorted by name
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getAvailablePackages(self):
        try:
            list = []

            # Simulate an upgrade
            self.aptcache.upgrade()

            # Loop through all packages marked for upgrade
            for pkg in self.aptcache.get_changes():
                # If the package is upgradable, add it to the list of available packages
                if pkg.is_upgradable:
                    # TODO debug
                    # if pkg.name != 'vim':
                    #     continue

                    myPackage = {
                        'name': pkg.name,
                        'current_version': pkg.installed.version,
                        'available_version': pkg.candidate.version
                    }

                    list.append(myPackage)
            
            # Sort the list by package name
            list.sort(key=lambda x: x['name'])

            return list

        except Exception as e:
            print('Error while getting available packages: ' + str(e))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Update apt cache
    #
    #-------------------------------------------------------------------------------------------------------------------
    def updateCache(self):
        try:
            self.aptcache.upgrade()

        except Exception as e:
            print('Error while updating apt cache: ' + str(e))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Unhold all packages
    #
    #-------------------------------------------------------------------------------------------------------------------
    def unholdAll(self):
        # Retrieve the list of packages on hold
        result = subprocess.run(
            ["apt-mark", "showhold"],
            capture_output = True,
            text = True
        )

        if result.returncode != 0:
            print('Error while getting holded packages: ' + result.stderr)
            exit(1)

        list = result.stdout.splitlines()

        # Quit if there are no packages on hold
        if list == '':
            return

        # Unhold all packages
        for package in list:
            result = subprocess.run(
                ["apt-mark", "unhold", package],
                capture_output = True,
                text = True
            )

            if result.returncode != 0:
                print('Error while unholding package: ' + result.stderr)
                exit(1)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Exclude (hold) specified package
    #
    #-------------------------------------------------------------------------------------------------------------------
    def exclude(self, package):
        result = subprocess.run(
            ["apt-mark", "hold", package],
            capture_output = True,
            text = True
        )

        if result.returncode != 0:
            print('Error while excluding package from update: ' + result.stderr)
            exit(1)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Update packages
    #
    #-------------------------------------------------------------------------------------------------------------------
    def update(self, packagesList, exit_on_package_update_error: bool = True, dist_upgrade: bool = False, keep_oldconf: bool = True):
        # Total count of success and failed package updates
        self.upgraded = {
            'success': 0,
            'failed': 0
        }

        # Loop through the list of packages to update
        for pkg in packagesList:
            # If the package is excluded, ignore it
            if pkg['excluded']:
                continue

            print('\n ▪ Updating ' + Fore.GREEN + pkg['name'] + Style.RESET_ALL + ' (' + pkg['current_version'] + ' → ' + pkg['available_version'] + '):')

            # If --keep-oldconf is True, then keep the old configuration file
            if keep_oldconf:
                cmd = ['apt-get', 'install', pkg['name'], '-y', '-o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"']
            else:
                cmd = ['apt-get', 'install', pkg['name'], '-y']

            popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)

            # Print lines as they are read
            for line in popen.stdout:
                line = line.replace('\r', '')
                print(' | ' + line, end='')

            # Wait for the command to finish
            popen.wait()

            # If command failed, either raise an exception or print a warning
            if popen.returncode != 0:

                self.upgraded['failed'] += 1

                # If error is critical, raise an exception
                if (exit_on_package_update_error == True):
                    raise Exception('error while updating ' + pkg['name'])

                # Else print a warning and continue to the next package
                else:
                    print('error while updating ' + pkg['name'])
                    continue

            # Close the pipe
            popen.stdout.close()

            # If command succeeded, increment the success counter
            self.upgraded['success'] += 1
