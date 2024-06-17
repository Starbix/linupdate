# coding: utf-8

# Import libraries
import os
import subprocess
import time

class Dnf:

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return list of available dnf packages, sorted by name
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getAvailablePackages(self):
        # Get list of packages to update sorted by name
        # e.g. dnf repoquery -q -a --qf="%{name} %{version}-%{release}.%{arch} %{repoid}" --upgrades
        result = subprocess.run(
            ["dnf", "repoquery", "--upgrades", "-q", "-a", "--qf=%{name} %{version}-%{release}.%{arch} %{repoid}"],
            capture_output = True,
            text = True
        )

        # Quit if an error occurred
        if result.returncode != 0:
            raise Exception('could not retrieve available packages list: ' + result.stderr)

        list = []

        for line in result.stdout.split('\n'):
            if line != '':
                package = line.split(' ')

                # Retrieve current version with dnf
                # e.g. rpm -q --qf="%{version}-%{release}.%{arch}" <package>
                result = subprocess.run(
                    ["rpm", "-q", "--qf=%{version}-%{release}.%{arch}", package[0]],
                    capture_output = True,
                    text = True
                )

                # Quit if an error occurred
                if result.returncode != 0:
                    raise Exception('could not retrieve current version of package ' + package[0] + ': ' + result.stderr)

                current_version = result.stdout.strip()

                list.append({
                    'name': package[0],
                    'current_version': current_version,
                    'available_version': package[1],
                    'repository': package[2]
                })

        return list


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Clear dnf cache
    #
    #-------------------------------------------------------------------------------------------------------------------
    def clear_cache(self):
        # Check if dnf lock is present
        self.check_lock

        result = subprocess.run(
            ["dnf", "clean", "all"],
            capture_output = True,
            text = True,
        )

        # Quit if an error occurred
        if result.returncode != 0:
            raise Exception('Error while clearing dnf cache: ' + result.stderr)
    

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Update dnf cache
    #
    #-------------------------------------------------------------------------------------------------------------------
    def updateCache(self):
        # Useless because dnf update command already updates the cache
        return


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return dnf history Ids sorted by modification time
    #
    #-------------------------------------------------------------------------------------------------------------------
    def get_history(self, order):
        # Get history IDs
        result = subprocess.run(
            ["dnf history list | tail -n +3 | awk '{print $1}'"],
            capture_output = True,
            text = True,
            shell = True
        )

        # Quit if an error occurred
        if result.returncode != 0:
            raise Exception('could nt retrieve dnf history: ' + result.stderr)

        # Retrieve history IDs
        ids = result.stdout.splitlines()

        # If order is newest, then sort by date in ascending order
        if order == 'newest':
            ids.reverse()

        return ids


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Wait for DNF lock to be released
    #
    #-------------------------------------------------------------------------------------------------------------------
    def check_lock(self):
        if os.path.isfile('/var/run/dnf.pid'):
            print(' Waiting for dnf lock...', end=' ')

            while os.path.isfile('/var/run/dnf.pid'):
                time.sleep(2)
