# coding: utf-8

# Import constants
from constant import *

# Import libraries
from pathlib import Path
from colorama import Fore, Back, Style

# Import classes
from src.controllers.Module.Reposerver.Config import Config as ReposerverConfig
from src.controllers.Module.Reposerver.Args import Args
from src.controllers.Exit import Exit

class Reposerver:
    def __init__(self):
        self.reposerverConfigController = ReposerverConfig()
        self.exitController = Exit()

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Load Reposerver module
    #
    #-------------------------------------------------------------------------------------------------------------------
    def load(self):
        try:
            # Generate config file if not exist
            self.reposerverConfigController.generateConf()

            # Check config file
            self.reposerverConfigController.checkConf()

        except Exception as e:
            print(Fore.YELLOW + ' Error while loading reposerver module: ' + str(e) + Style.RESET_ALL)
            self.exitController.cleanExit(1)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Execute pre-update actions
    #
    #-------------------------------------------------------------------------------------------------------------------
    def pre(self):
        # Note: no need of try / except block here, as it is already handled in the global module pre function

        # Retrieve global configuration from reposerver
        self.reposerverConfigController.getReposerverConf()

        # Retrieve profile configuration from reposerver
        self.reposerverConfigController.getProfilePackagesConf()

        # Retrieve profile repositories from reposerver
        self.reposerverConfigController.getProfileRepos()


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Reposerver main function
    #
    #-------------------------------------------------------------------------------------------------------------------
    def main(self):
        try:
            myArgs = Args()

            # Parse reposerver arguments
            myArgs.parse()
        except Exception as e:
            print(Fore.YELLOW + str(e) + Style.RESET_ALL)
            self.exitController.cleanExit(1)
