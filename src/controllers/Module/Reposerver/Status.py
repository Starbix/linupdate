# coding: utf-8

# Import constants
from constant import *

# Import libraries
from colorama import Fore, Back, Style
import socket

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
            print(' Error while updating request status: ' + str(e))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send general status
    #
    #-------------------------------------------------------------------------------------------------------------------
    def sendGeneralStatus(self):
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

        # Update Reposerver's request status, set it to 'running'
        self.updateRequestStatus('general-status-update', 'running')

        try:
            self.httpRequestController.quiet = False
            self.httpRequestController.put(url + '/api/v2/host/status', id, token, data)
            status = 'done'
        except Exception as e:
            status = 'error'

        # Update Reposerver's request status
        self.updateRequestStatus('general-status-update', status)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send all packages status
    #
    #-------------------------------------------------------------------------------------------------------------------
    def sendPackagesStatus(self):
        rc = 0

        try:
            # Update Reposerver's request status, set it to 'running'
            self.updateRequestStatus('packages-status-update', 'running')

            # Send all status
            self.sendFullHistory()
            self.sendAvailablePackagesStatus()
            self.sendInstalledPackagesStatus()

            status = 'done'
        except Exception as e:
            status = 'error'
            rc = 1

        # Update Reposerver's request status to 'done' or 'error'
        try:
            self.updateRequestStatus('packages-status-update', status)
        except Exception as e:
            print(' Error while updating request status: ' + str(e))
            rc = 1

        # Exit with the appropriate return code        
        self.exitController.cleanExit(rc)


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
            print(Fore.RED + '✕' + Style.RESET_ALL + ' error while retrieving available packages: ' + str(e))

            # Raise an exception to be caught in the main function
            raise Exception()


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
            print(Fore.RED + ' ✕ ' + Style.RESET_ALL + 'error while retrieving installed packages: ' + str(e))

            # Raise an exception to set status to 'error'
            raise Exception()
        
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

        # TODO here : update request full-history-update => 'running'

        # If limit is set (not the default 999999), history parsing will start from the newest to the oldest
        if entries_limit != 999999:        
            history_order = 'newest'

        try:
            # Retrieve history Ids or files
            items = self.packageController.get_history(history_order)
        except Exception as e:
            print(Fore.RED + ' ✕ ' + Style.RESET_ALL + str(e))




        for item in items:
            print(item)


        exit()




        return
        

