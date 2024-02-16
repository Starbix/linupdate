# coding: utf-8

# Import constants
from constant import *

# Import libraries
from colorama import Fore, Back, Style
import ipaddress
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

        # Retrieve URL, ID and token
        self.url = self.reposerverConfigController.getUrl()
        self.id = self.reposerverConfigController.getId()
        self.token = self.reposerverConfigController.getToken()


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Update Reposerver request status
    #
    #-------------------------------------------------------------------------------------------------------------------
    def updateRequestStatus(self, requestType: str, status: str):
        # Do not print message if aknowledge request has been sent successfully
        self.httpRequestController.quiet = True

        data = {
            'status': status,
        }
        self.httpRequestController.put(self.url + '/api/v2/host/request/' + requestType, self.id, self.token, data)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send general status
    #
    #-------------------------------------------------------------------------------------------------------------------
    def sendGeneralStatus(self):
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

        print(' ▪ Sending status to ' + Fore.YELLOW + self.url + Style.RESET_ALL + ':')

        # Update Reposerver's request status, set it to 'running'
        self.updateRequestStatus('general-status-update', 'running')

        try:
            self.httpRequestController.quiet = False
            self.httpRequestController.put(self.url + '/api/v2/host/status', self.id, self.token, data)
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
            print('Error while updating request status: ' + str(e))
            rc = 1

        # Exit with the appropriate return code        
        self.exitController.cleanExit(rc)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send list of available packages
    #
    #-------------------------------------------------------------------------------------------------------------------
    def sendAvailablePackagesStatus(self):
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
        print(' ▪ Sending data to ' + Fore.YELLOW + self.url + Style.RESET_ALL + ':')

        self.httpRequestController.quiet = False
        self.httpRequestController.put(self.url + '/api/v2/host/packages/available', self.id, self.token, data)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send list of installed packages
    #
    #-------------------------------------------------------------------------------------------------------------------
    def sendInstalledPackagesStatus(self):
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
            print(Fore.RED + '✕' + Style.RESET_ALL + ' error while retrieving installed packages: ' + str(e))

            # Raise an exception to set status to 'error'
            raise Exception()
        
        # Send installed packages to Reposerver
        print(' ▪ Sending data to ' + Fore.YELLOW + self.url + Style.RESET_ALL + ':')

        self.httpRequestController.quiet = False
        self.httpRequestController.put(self.url + '/api/v2/host/packages/installed', self.id, self.token, data)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send packages history (installed, removed, upgraded, downgraded, etc.)
    #
    #-------------------------------------------------------------------------------------------------------------------
    def sendFullHistory(self):
        

