# coding: utf-8

# Import constants
from constant import *

# Import libraries
from colorama import Fore, Back, Style
import socket
import subprocess

# Import classes
from src.controllers.System import System
from src.controllers.App.App import App
from src.controllers.App.Config import Config
from src.controllers.Module.Reposerver.Config import Config as ReposerverConfig
from src.controllers.Exit import Exit
from src.controllers.Package.Package import Package
from src.controllers.HttpRequest import HttpRequest

class Status:
    def __init__(self):
        self.systemController           = System()
        self.appController              = App()
        self.configController           = Config()
        self.reposerverConfigController = ReposerverConfig()
        self.httpRequestController      = HttpRequest()
        self.packageController          = Package()
        self.exitController             = Exit()


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Update Reposerver request status
    #
    #-------------------------------------------------------------------------------------------------------------------
    def updateRequestStatus(self, requestType: str, status: str):
        try:
            # Retrieve URL, ID and token
            url = self.reposerverConfigController.getUrl()
            id = self.reposerverConfigController.getId()
            token = self.reposerverConfigController.getToken()

            # Do not print message if aknowledge request has been sent successfully
            self.httpRequestController.quiet = True

            data = {
                'status': status,
            }

            self.httpRequestController.put(url + '/api/v2/host/request/' + requestType, id, token, data)
        except Exception as e:
            raise Exception('could not acknowledge reposerver request of type ' + requestType + ': ' + str(e))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send general status
    #
    #-------------------------------------------------------------------------------------------------------------------
    def sendGeneralStatus(self):
        try:
            # Retrieve URL, ID and token
            url = self.reposerverConfigController.getUrl()
            id = self.reposerverConfigController.getId()
            token = self.reposerverConfigController.getToken()

            data = {
                'hostname': socket.gethostname(),
                'os_family': self.systemController.getOsFamily(),
                'os': self.systemController.getOsName(),
                'os_version': self.systemController.getOsVersion(),
                'type': self.systemController.getVirtualization(),
                'kernel': self.systemController.getKernel(),
                'arch': self.systemController.getArch(),
                'profile': self.configController.getProfile(),
                'env': self.configController.getEnvironment(),
                'agent_status': self.appController.getAgentStatus(),
                'linupdate_version': self.appController.getVersion(),
                'reboot_required': str(self.systemController.rebootRequired()).lower() # Convert True/False to 'true'/'false'
            }

            print(' ▪ Sending status to ' + Fore.YELLOW + url + Style.RESET_ALL + ':')

        except Exception as e:
            raise Exception('could not build general status data: ' + str(e))

        # Update Reposerver's request status, set it to 'running'
        self.updateRequestStatus('general-status-update', 'running')

        try:
            self.httpRequestController.quiet = False
            self.httpRequestController.put(url + '/api/v2/host/status', id, token, data)
            # Update Reposerver's request status
            self.updateRequestStatus('general-status-update', 'done')
        except Exception as e:
            # Update Reposerver's request status
            self.updateRequestStatus('general-status-update', 'error')

            raise Exception('error while sending general status to reposerver: ' + str(e))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send all packages status
    #
    #-------------------------------------------------------------------------------------------------------------------
    def sendPackagesStatus(self):
        rc = 0

        # Update Reposerver's request status, set it to 'running'
        self.updateRequestStatus('packages-status-update', 'running')

        try:
            # Send all status
            self.sendFullHistory()
            self.sendAvailablePackagesStatus()
            self.sendInstalledPackagesStatus()

            self.updateRequestStatus('packages-status-update', 'done')
        except Exception as e:
            self.updateRequestStatus('packages-status-update', 'error')
            
            raise Exception('error while sending packages status to reposerver: ' + str(e))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send list of available packages
    #
    #-------------------------------------------------------------------------------------------------------------------
    def sendAvailablePackagesStatus(self):
        # Retrieve URL, ID and token
        url = self.reposerverConfigController.getUrl()
        id = self.reposerverConfigController.getId()
        token = self.reposerverConfigController.getToken()

        available_packages = 'none'

        print(' ▪ Building available packages list...')

        try:
            # Retrieve available packages
            packages = self.packageController.getAvailablePackages()

            if len(packages) > 0:
                available_packages = ''

                for package in packages:
                    name = package['name']
                    available_version = package['available_version']

                    # Ignore package if name is empty
                    if name == '':
                        continue

                    # Redhat only
                    if self.systemController.getOsFamily() == 'Redhat':
                        # Remove epoch if it is equal to 0
                        if available_version.startswith('0:'):
                            available_version = available_version[2:]

                    # Add package name, its available version to the available_packages string
                    available_packages += name + '|' + available_version + ','

                # Remove last comma
                available_packages = available_packages[:-1]

            # Convert to JSON
            data = {
                'available_packages': available_packages
            }

        except Exception as e:
            # Raise an exception to be caught in the main function
            raise Exception('error while retrieving available packages: ' + str(e))

        # Send available packages to Reposerver
        print(' ▪ Sending data to ' + Fore.YELLOW + url + Style.RESET_ALL + ':')

        self.httpRequestController.quiet = False
        self.httpRequestController.put(url + '/api/v2/host/packages/available', id, token, data)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send list of installed packages
    #
    #-------------------------------------------------------------------------------------------------------------------
    def sendInstalledPackagesStatus(self):
        # Retrieve URL, ID and token
        url = self.reposerverConfigController.getUrl()
        id = self.reposerverConfigController.getId()
        token = self.reposerverConfigController.getToken()

        installed_packages = ''

        print(' ▪ Building installed packages list...')

        try:
            # Retrieve installed packages
            packages = self.packageController.getInstalledPackages()

            if len(packages) > 0:
                for package in packages:
                    name = package['name']
                    version = package['version']

                    # Ignore package if name is empty
                    if name == '':
                        continue

                    # Redhat only
                    if self.systemController.getOsFamily() == 'Redhat':
                        # Remove epoch if it is equal to 0
                        if version.startswith('0:'):
                            version = version[2:]

                    # Add package name, its available version to the installed_packages string
                    installed_packages += name + '|' + version + ','

                # Remove last comma
                installed_packages = installed_packages[:-1]

            # Convert to JSON
            data = {
                'installed_packages': installed_packages
            }

        except Exception as e:
            # Raise an exception to set status to 'error'
            raise Exception('error while retrieving installed packages: ' + str(e))
        
        # Send installed packages to Reposerver
        print(' ▪ Sending data to ' + Fore.YELLOW + url + Style.RESET_ALL + ':')

        self.httpRequestController.quiet = False
        self.httpRequestController.put(url + '/api/v2/host/packages/installed', id, token, data)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send packages history (installed, removed, upgraded, downgraded, etc.)
    #
    #-------------------------------------------------------------------------------------------------------------------
    def sendFullHistory(self, entries_limit: int = 999999):
        # Initialize a limit counter which will be incremented until it reaches the entries_limit
        limit_counter = 0

        # History parsing will start from the oldest to the newest
        history_order = 'oldest'

        print(' ▪ Building packages history...')

        # Update Reposerver's request status, set it to 'running'
        self.updateRequestStatus('full-history-update', 'running')

        # If limit is set (not the default 999999), history parsing will start from the newest to the oldest
        if entries_limit != 999999:        
            history_order = 'newest'

        try:
            # Retrieve history Ids or files
            items = self.packageController.get_history(history_order)
        except Exception as e:
            self.updateRequestStatus('full-history-update', 'error')
            raise Exception('error while retrieving history: ' + str(e))

        # If there is no item (would be strange), exit
        if len(items) == 0:
            print(' no history found')
            return

        # Parse each apt history files
        for item in items:
            # Retrieve all Start-Date in the history file
            result = subprocess.run(
                ['zgrep "^Start-Date:*" ' + item],
                capture_output = True,
                text = True,
                shell = True
            )

            # Quit if an error occurred
            if result.returncode != 0:
                raise Exception('could not retrieve Start-Date from ' + item + ': ' + result.stderr)

            # Split the result into a list
            start_dates = result.stdout.strip().split('\n')

            for start_date in start_dates:
                # Quit if the limit of entries to send has been reached
                if limit_counter > entries_limit:
                    break
                
                # On ignore cet évènement si celui-ci a le même Id (même date) que le précédent
                # if [ ! -z "$IGNORE_EVENT" ] && [ "$IGNORE_EVENT" == "$START_DATE" ];then
                #     continue
                # fi

                # TODO à terminer


        self.updateRequestStatus('full-history-update', 'done')

        

