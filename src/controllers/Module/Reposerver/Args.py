# coding: utf-8

# Import constants
from constant import *

# Import libraries
from colorama import Fore, Back, Style

import argparse

# Import classes
from src.controllers.Exit import Exit
from src.controllers.Module.Reposerver.Config import Config
from src.controllers.Module.Reposerver.Register import Register
from src.controllers.Module.Reposerver.Status import Status
from src.controllers.Module.Reposerver.Agent import Agent
from src.controllers.HttpRequest import HttpRequest

class Args:
    def __init__(self):
        self.exitController        = Exit()
        self.configController      = Config()
        self.registerController    = Register()
        self.statusController      = Status()
        self.agentController       = Agent()
        self.httpRequestController = HttpRequest()

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Parse arguments
    #
    #-------------------------------------------------------------------------------------------------------------------
    def parse(self):
        # TODO renseigner toutes les descriptions
        try:
            # Parse arguments
            parser = argparse.ArgumentParser()

            # Define valid arguments

            # URL
            parser.add_argument("--url", action="store", nargs='?', default="null", help="Specify target reposerver URL")
            # API key
            parser.add_argument("--api-key", action="store", nargs='?', default="null", help="Specify API key to authenticate to the reposerver")
            # IP
            parser.add_argument("--ip", action="store", nargs='?', default="null", help="Specify an alternative local IP address to use to authenticate to the reposerver")
        
            # Allow configuration update
            parser.add_argument("--allow-conf-update", action="store", nargs='?', default="null", help="")
            # Allow repos update
            parser.add_argument("--allow-repos-update", action="store", nargs='?', default="null", help="")

            # Agent enable
            parser.add_argument("--agent-enable", action="store", nargs='?', default="null", help="Enable reposerver module agent. This agent will regularly send informations about this host to reposerver (global informations, packages informations...)")
            # Agent listen enable
            parser.add_argument("--agent-listen-enable", action="store", nargs='?', default="null", help="Enable or disable agent listening for requests coming from the reposerver")
            # Agent listen interface
            parser.add_argument("--agent-listen-int", action="store", nargs='?', default="null", help="Specify the local network interface to use to listen for requests coming from the reposerver")

            # Register to reposerver
            parser.add_argument("--register", action="store_true", default="null", help="Register this host to the reposerver (--api-key required)")
            # Unregister from server
            parser.add_argument("--unregister", action="store_true", default="null", help="Unregister this host from the reposerver")

            # Retrieve reposerver main configuration
            parser.add_argument("--get-reposerver-conf", action="store_true", default="null", help="Get reposerver global configuration")
            # Retrieve profile packages configuration from reposerver
            parser.add_argument("--get-profile-packages-conf", action="store_true", default="null", help="Get profile packages configuration from reposerver")
            # Retrieve profile repositories from reposerver
            parser.add_argument("--get-profile-repos", action="store_true", default="null", help="Get profile repositories from reposerver")
            
            # Send status
            parser.add_argument("--send-general-status", action="store_true", default="null", help="Send host global informations (OS, version, kernel..) to the reposerver")
            # Send packages status
            parser.add_argument("--send-packages-status", action="store_true", default="null", help="Send this host packages status to the reposerver (available, installed)")
            # Send full history
            parser.add_argument("--send-full-history", action="store_true", default="null", help="Send host packages events history (updates, downgrades, uninstallations...) to the reposerver")
            # Send full status
            parser.add_argument("--send-full-status", action="store_true", default="null", help="Send all of the previous status to the reposerver")

            # Parse arguments
            args, unknown = parser.parse_known_args()

            # If unknown arguments are passed
            # if unknown:
            #     raise Exception('unknown argument(s): ' + str(unknown))
            
        except Exception as e:
            raise Exception('error while parsing arguments: ' + str(e))

        try:
            #
            # If --url param has been set
            #
            if args.url != "null":
                # If a URL is set (not 'None'), change the app URL
                if args.url:
                    # Set new URL
                    self.configController.setUrl(args.url)

                    # Print URL change
                    print(' Reposerver URL set to ' + Fore.YELLOW + args.url + Style.RESET_ALL)
                # Else print the current URL
                else:
                    print(' Current Reposerver URL: ' + Fore.YELLOW + self.configController.getUrl() + Style.RESET_ALL)

            #
            # If --api-key param has been set
            #
            if args.api_key != "null":
                Args.api_key = args.api_key

            #
            # If --ip param has been set
            #
            if args.ip != "null":
                Args.ip = args.ip

            #
            # If --agent-enable param has been set
            #
            if args.agent_enable != "null":
                if args.agent_enable == 'true':
                    self.agentController.setEnable(True)
                else:
                    self.agentController.setEnable(False)

            # 
            # If --agent-listen-enable param has been set
            #
            if args.agent_listen_enable != "null":
                if args.agent_listen_enable == 'true':
                    self.agentController.setListenEnable(True)
                else:
                    self.agentController.setListenEnable(False)

            #
            # If --agent-listen-int param has been set
            #
            if args.agent_listen_int != "null":
                # If an interface is set (not 'None'), change the agent interface
                if args.agent_listen_int:
                    # Get current interface
                    currentInterface = self.agentController.getListenInterface()

                    # Set new interface
                    self.agentController.setListenInterface(args.agent_listen_int)

                    # Print interface change
                    print(' Switched from interface ' + currentInterface + ' to ' + args.agent_listen_int)
                # Else print the current interface
                else:
                    print(' Current interface: ' + self.agentController.getListenInterface())

            #
            # If --allow-conf-update param has been set
            #
            if args.allow_conf_update != "null":
                if args.allow_conf_update == 'true':
                    self.configController.setAllowConfUpdate(True)
                else:
                    self.configController.setAllowConfUpdate(False)
        
            #
            # If --allow-repos-update param has been set
            #
            if args.allow_repos_update != "null":
                if args.allow_repos_update == 'true':
                    self.configController.setAllowReposUpdate(True)
                else:
                    self.configController.setAllowReposUpdate(False)

            #
            # If --register param has been set
            #
            if args.register != "null" and args.register:
                # Register to the URL with the API key and IP (could be "null" if not set)
                self.registerController.register(args.api_key, args.ip)
                self.exitController.cleanExit()

            #
            # If --unregister param has been set
            #
            if args.unregister != "null" and args.unregister:
                # Unregister from the reposerver
                self.registerController.unregister()
                self.exitController.cleanExit()

            #
            # If --get-server-conf param has been set
            #
            if args.get_server_conf != "null" and args.get_server_conf:
                # Get server configuration
                self.configController.getReposerverConf()
                self.exitController.cleanExit()

            #
            # If --get-profile-packages-conf param has been set
            #
            if args.get_profile_packages_conf != "null" and args.get_profile_packages_conf:
                # Get profile packages configuration
                self.configController.getProfilePackagesConf()
                self.exitController.cleanExit()

            #
            # If --get-profile-repos param has been set
            #
            if args.get_profile_repos != "null" and args.get_profile_repos:
                # Get profile repositories
                self.configController.getProfileRepos()
                self.exitController.cleanExit()

            #
            # If --send-general-status param has been set
            #
            if args.send_general_status != "null" and args.send_general_status:
                # Send general status
                self.statusController.sendGeneralStatus()
                self.exitController.cleanExit()

            #
            # If --send-packages-status param has been set
            #
            if args.send_packages_status != "null" and args.send_packages_status:
                self.statusController.sendPackagesStatus()
                self.exitController.cleanExit()

            # 
            # If --send-full-history param has been set
            #
            if args.send_full_history != "null" and args.send_full_history:
                # Send full history
                self.statusController.sendFullHistory()
                self.exitController.cleanExit()

            #
            # If --send-full-status param has been set
            #
            if args.send_full_status != "null" and args.send_full_status:
                # Send full status including general status, available packages status, installed packages status and full history
                self.statusController.sendGeneralStatus()
                self.statusController.sendPackagesStatus()
                self.exitController.cleanExit()
    
        except Exception as e:
            raise Exception(str(e))
