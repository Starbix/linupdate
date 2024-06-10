# coding: utf-8

# Import constants
from constant import *

# Import libraries
from pathlib import Path
from colorama import Fore, Back, Style

# Import classes
from src.controllers.Module.Reposerver.Config import Config as ReposerverConfig
from src.controllers.Module.Reposerver.Status import Status
from src.controllers.Module.Reposerver.Args import Args
from src.controllers.Exit import Exit

class Reposerver:
    def __init__(self):
        self.reposerverConfigController = ReposerverConfig()
        self.statusController = Status()
        self.argsController = Args()
        self.exitController = Exit()

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Load Reposerver module
    #
    #-------------------------------------------------------------------------------------------------------------------
    def load(self):
        # Note: no need of try / except block here, as it is already handled in the Module load() function

        # Generate config file if not exist
        self.reposerverConfigController.generateConf()

        # Check config file
        self.reposerverConfigController.checkConf()


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Execute pre-update actions
    #
    #-------------------------------------------------------------------------------------------------------------------
    def pre(self):
        # Note: no need of try / except block here, as it is already handled in the Module pre() function

        # Retrieve global configuration from reposerver
        self.reposerverConfigController.getReposerverConf()

        # Retrieve profile configuration from reposerver
        self.reposerverConfigController.getProfilePackagesConf()

        # Retrieve profile repositories from reposerver
        self.reposerverConfigController.getProfileRepos()


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Execute post-update actions
    #
    #-------------------------------------------------------------------------------------------------------------------
    def post(self, updateSummary):
        # Note: no need of try / except block here, as it is already handled in the Module pre() function
        
        # TODO : à finir si pas fini

        # Quit if there was no packages updates
        if updateSummary['update']['success']['count'] == 0:
            return
        
        # Generaly "*-release" packages on Redhat/CentOS reset .repo files. If a package of this type has been updated then we update the repos configuration from the repo server (profiles)
        # If a package named *-release is present in the updated packages list
        for package in updateSummary['update']['success']['packages']:
            if package.endswith('-release'):
                # Update repositories
                self.reposerverConfigController.getProfileRepos()
                break

        # Send last 4 packages history entries to the reposerver
        self.statusController.sendFullHistory(4)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Reposerver main function
    #
    #-------------------------------------------------------------------------------------------------------------------
    def main(self):
        try:
            # Generate config file if not exist
            self.reposerverConfigController.generateConf()

            # Check config file
            self.reposerverConfigController.checkConf()

            # Parse reposerver arguments
            self.argsController.parse()
        except Exception as e:
            raise Exception(str(e))
