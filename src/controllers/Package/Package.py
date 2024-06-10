# coding: utf-8

# https://github.com/excid3/python-apt/blob/master/doc/examples/inst.py

# Import libraries
from tabulate import tabulate
from colorama import Fore, Back, Style
import re

# Import classes
from src.controllers.System import System
from src.controllers.App.App import App
from src.controllers.Exit import Exit

class Package:
    def __init__(self):
        self.systemController = System()
        self.appController = App()
        self.exitController = Exit()

        # Import libraries depending on the OS family

        # If Debian, import apt
        if (self.systemController.getOsFamily() == 'Debian'):
            from src.controllers.Package.Apt import Apt
            self.myPackageManagerController = Apt()

        # If Redhat, import yum
        if (self.systemController.getOsFamily() == 'Redhat'):
            from src.controllers.Package.Dnf import Dnf
            self.myPackageManagerController = Dnf()

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Check for package exclusions
    #
    #-------------------------------------------------------------------------------------------------------------------
    def exclude(self, ignore_exclude):
        try:
            # Unhold / unexclude all packages
            self.myPackageManagerController.unholdAll()

            # Create a new empty list of packages to update
            packagesToUpdateList = []

            # Retrieve the list of packages to exclude from the config file
            configuration = self.appController.getConf()
            excludeAlways = configuration['packages']['exclude']['always']
            excludeOnMajorUpdate = configuration['packages']['exclude']['on_major_update']

            # Loop through the list of packages to update
            for package in self.packagesToUpdateList:
                excluded = False

                # Check for exclusions and exclude packages only if the ignore_exclude parameter is False
                if not ignore_exclude:
                    # If the package is in the list of packages to exclude (on major update), check if the available version is a major update
                    if excludeOnMajorUpdate:
                        # There can be regex in the excludeOnMajorUpdate list (e.g. apache.*), so we need to convert it to a regex pattern
                        # https://www.geeksforgeeks.org/python-check-if-string-matches-regex-list/
                        regex = '(?:% s)' % '|'.join(excludeOnMajorUpdate)

                        # Check if the package name matches the regex pattern
                        if re.match(regex, package['name']):
                            # Retrieve the first digit of the current and available versions
                            # If the first digit is different then it is a major update, exclude the package
                            if package['current_version'].split('.')[0] != package['available_version'].split('.')[0]:
                                self.myPackageManagerController.exclude(package['name'])
                                excluded = True

                    # If the package is in the list of packages to exclude (always), exclude it
                    if excludeAlways:
                        # There can be regex in the excludeAlways list (e.g. apache.*), so we need to convert it to a regex pattern
                        # https://www.geeksforgeeks.org/python-check-if-string-matches-regex-list/
                        regex = '(?:% s)' % '|'.join(excludeAlways)

                        # Check if the package name matches the regex pattern
                        if re.match(regex, package['name']): 
                            self.myPackageManagerController.exclude(package['name'])
                            excluded = True

                # Add the package to the list of packages to update
                packagesToUpdateList.append({
                    'name': package['name'],
                    'current_version': package['current_version'],
                    'available_version': package['available_version'],
                    'excluded': excluded
                })

            # Replace the list of packages to update with the new list
            self.packagesToUpdateList = packagesToUpdateList

            del configuration, excludeAlways, excludeOnMajorUpdate, packagesToUpdateList
        except Exception as e:
            raise Exception('error while excluding packages: ' + str(e))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Get installed packages
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getInstalledPackages(self):
        try:
            # Get a list of installed packages
            return self.myPackageManagerController.getInstalledPackages()
        
        except Exception as e:
            raise Exception('error while getting installed packages: ' + str(e))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Get available packages
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getAvailablePackages(self):
        try:
            # First, clear package manager cache
            self.myPackageManagerController.updateCache()

            # Get a list of available packages
            return self.myPackageManagerController.getAvailablePackages()

        except Exception as e:
            raise Exception('error while getting available packages: ' + str(e))
    

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Update packages
    #
    #-------------------------------------------------------------------------------------------------------------------
    def update(self, assume_yes: bool = False, ignore_exclude: bool = False, check_updates: bool = False, dist_upgrade: bool = False, keep_oldconf: bool = True):        
        # Package update summary
        self.summary = {
            'update': {
                'status': 'running',
                'success': {
                    'count': 0,
                    'packages': []
                },
                'failed': {
                    'count': 0,
                    'packages': []
                }
            }
        }

        try:
            # Retrieve configuration
            configuration = self.appController.getConf()

            # Retrieve the exit_on_package_update_error option
            exit_on_package_update_error = configuration['main']['exit_on_package_update_error']

            # Retrieve available packages
            self.packagesToUpdateList = self.getAvailablePackages()

            # Check for package exclusions
            self.exclude(ignore_exclude)

            # Count packages to update and packages excluded
            self.packagesToUpdateCount = 0
            self.packagesExcludedCount = 0

            for package in self.packagesToUpdateList:
                if 'excluded' in package and package['excluded']:
                    self.packagesExcludedCount += 1
                else:
                    self.packagesToUpdateCount += 1

            # Print the number of packages to update
            print('\n ' + Fore.GREEN + str(self.packagesToUpdateCount) + Style.RESET_ALL + ' packages will be updated, ' + Fore.YELLOW + str(self.packagesExcludedCount) + Style.RESET_ALL + ' will be excluded \n')

            # Convert the list of packages to a table
            table = []
            for package in self.packagesToUpdateList:
                # If package is excluded
                if 'excluded' in package and package['excluded']:
                    installOrExclude = Fore.YELLOW + '✕ (excluded)' + Style.RESET_ALL
                else:
                    installOrExclude = Fore.GREEN + '✔' + Style.RESET_ALL

                table.append(['', package['name'], package['current_version'], package['available_version'], installOrExclude])

            # Print the table list of packages to update
            # TODO : check prettytable for table with width control https://pypi.org/project/prettytable/
            print(tabulate(table, headers=["", "Package", "Current version", "Available version", "Install decision"], tablefmt="simple"), end='\n\n')

            # Quit if there are no packages to update
            if self.packagesToUpdateCount == 0:
                print(Fore.GREEN + ' No package updates \n' + Style.RESET_ALL)
                self.summary['status'] = 'nothing-to-do'
                return
            
            # Quit if --check-updates param has been specified
            if check_updates == True:
                exit(0)

            # If --assume-yes param has not been specified, then ask for confirmation before installing the printed packages update list
            if not assume_yes:
                # Ask for confirmation
                print('\n ' + Fore.YELLOW + 'Update now [y/N]' + Style.RESET_ALL, end=' ')

                answer = input()

                # Quit if the answer is not 'y'
                if answer.lower() != 'y':
                    print(Fore.YELLOW + ' Cancelled' + Style.RESET_ALL)
                    exit(1)

            print('\n Updating packages...')

            # Execute the packages update
            self.myPackageManagerController.update(self.packagesToUpdateList, exit_on_package_update_error, dist_upgrade, keep_oldconf)

            print('\n' + Fore.GREEN + ' Packages update completed' + Style.RESET_ALL)

            # Update the summary status
            self.summary['update']['status'] = 'done'

        except Exception as e:
            print('\n' + Fore.RED + ' Packages update failed: ' + str(e) + Style.RESET_ALL)
            self.summary['update']['status'] = 'failed'

        # Update the summary with the number of packages updated and failed
        self.summary['update']['success']['count'] = self.myPackageManagerController.summary['update']['success']['count']
        self.summary['update']['failed']['count'] = self.myPackageManagerController.summary['update']['failed']['count']

        # Print the number of packages updated and failed
        print('\n ' + Fore.GREEN + str(self.summary['update']['success']['count']) + Style.RESET_ALL + ' packages updated, ' + Fore.RED + str(self.summary['update']['failed']['count']) + Style.RESET_ALL + ' packages failed' + Style.RESET_ALL)

        # If there was a failed package update and the package update error is critical, then raise an exception to exit
        if exit_on_package_update_error == True and self.summary['update']['failed']['count'] > 0:
            raise Exception('Critical error: package update failed')


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return history items (log file or history Ids) for a specific order
    #
    #-------------------------------------------------------------------------------------------------------------------
    def get_history(self, order):
        return self.myPackageManagerController.get_history(order)
