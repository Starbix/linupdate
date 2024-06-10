# coding: utf-8

# Import constants
from constant import *

# Import libraries
from colorama import Fore, Back, Style


# Import classes
from src.controllers.Module.Reposerver.Config import Config

class Agent:
    def __init__(self):
        self.configController = Config()

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Enable or disable agent
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setEnable(self, value: bool):
        try:
            # Get current configuration
            configuration = self.configController.getConf()

            # Set allow_repos_update
            configuration['agent']['enabled'] = value

            # Write config file
            self.configController.writeConf(configuration)

            if value:
                print(' Reposerver agent ' + Fore.GREEN + 'enabled' + Style.RESET_ALL)
            else:
                print(' Reposerver agent ' + Fore.YELLOW + 'disabled' + Style.RESET_ALL)

        except Exception as e:
            raise Exception('could not set agent enable to ' + str(value) + ': ' + str(e))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Get current agent listening interface
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getListenInterface(self):
        # Get current configuration
        configuration = self.configController.getConf()

        # Return watch_interface
        return configuration['agent']['listen']['interface']


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Set agent listening interface
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setListenInterface(self, value: str):
        try:
            # Get current configuration
            configuration = self.configController.getConf()

            # Set listen interface
            configuration['agent']['listen']['interface'] = value

            # Write config file
            self.configController.writeConf(configuration)
        
            print(' Agent listening interface set to ' + Fore.GREEN + value + Style.RESET_ALL)
        
        except Exception as e:
            raise Exception('could not set agent listening interface to ' + value + ': ' + str(e))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Enable or disable agent listening
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setListenEnable(self, value: bool):
        try:
            # Get current configuration
            configuration = self.configController.getConf()

            # Set allow_repos_update
            configuration['agent']['listen']['enabled'] = value

            # Write config file
            self.configController.writeConf(configuration)

            if value:
                print(' Agent listening ' + Fore.GREEN + 'enabled' + Style.RESET_ALL)
            else:
                print(' Agent listening ' + Fore.YELLOW + 'disabled' + Style.RESET_ALL)

        except Exception as e:
            raise Exception('could not set agent listening enable to ' + str(value) + ': ' + str(e))
