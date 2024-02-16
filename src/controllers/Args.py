# coding: utf-8

# Import constants
from constant import *

# Import libraries
from colorama import Fore, Back, Style

import argparse

# Import classes
from src.controllers.App.App import App
from src.controllers.App.Config import Config
from src.controllers.Module.Module import Module
from src.controllers.Exit import Exit

class Args:

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Pre-parse arguments
    #
    #-------------------------------------------------------------------------------------------------------------------
    def preParse(self):
        # Default values
        Args.from_agent = False

        # Parse arguments
        parser = argparse.ArgumentParser()

        # Define valid arguments

        # Agent
        parser.add_argument("--from-agent", action="store_true", default="null", help="")

        # Parse arguments
        args, unknown = parser.parse_known_args()

        #
        # If --from-agent param has been set
        #
        if args.from_agent != "null":
            Args.from_agent = True


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Parse arguments
    #
    #-------------------------------------------------------------------------------------------------------------------
    # TODO: écrire le help de chaque argument
    def parse(self):
        # Default values
        Args.verbosity = False
        Args.assume_yes = False
        Args.check_updates = False
        Args.ignore_exclude = False
        Args.dist_upgrade = False
        Args.keep_oldconf = True # TODO peut être abandonner ce paramètre et le mettre à True tout le temps

        myApp       = App()
        myAppConfig = Config()
        myModule    = Module()
        myExit      = Exit()

        # Parse arguments
        parser = argparse.ArgumentParser()

        # Define valid arguments

        # Version
        parser.add_argument("-V", "--version", action="store_true", default="null", help="show program version")
        # Verbosity
        parser.add_argument("-v", "--verbosity", action="store_true", default="null", help="increase output verbosity")
        # Force / assume-yes
        parser.add_argument("-y", "--assume-yes", action="store_true", default="null", help="assume yes")
        # Check updates
        parser.add_argument("--check-updates", action="store_true", default="null", help="check updates")
        # Ignore exclude
        parser.add_argument("--ignore-exclude", action="store_true", default="null", help="ignore-exclude")

        # Profile
        parser.add_argument("--profile", action="store", nargs='?', default="null", help="profile")
        # Environment
        parser.add_argument("--env", action="store", nargs='?', default="null", help="environment")
        
        # Dist upgrade
        parser.add_argument("--dist-upgrade", action="store_true", default="null", help="dist-upgrade")
        # Keep oldconf
        parser.add_argument("--keep-oldconf", action="store_true", default="null", help="keep-oldconf")

        # Get excluded packages
        parser.add_argument("--get-exclude", action="store", nargs='?', default="null", help="Get excluded packages")
        # Get excluded packages on major update
        parser.add_argument("--get-exclude-major", action="store", nargs='?', default="null", help="Get excluded packages on major update")
        # Get services to restart after package update
        parser.add_argument("--get-service-restart", action="store", nargs='?', default="null", help="Get services to restart")
        # Exclude
        parser.add_argument("--exclude", action="store", nargs='?', default="null", help="exclude packages")
        # Exclude on major update
        parser.add_argument("--exclude-major", action="store", nargs='?', default="null", help="exclude packages on major update")
        # Services to restart after package update
        parser.add_argument("--service-restart", action="store", nargs='?', default="null", help="restart services")

        # List modules
        parser.add_argument("--mod-list", action="store_true", default="null", help="")
        # Module enable
        parser.add_argument("--mod-enable", action="store", nargs='?', default="null", help="enable module")
        # Module disable
        parser.add_argument("--mod-disable", action="store", nargs='?', default="null", help="disable module")
        # Module configure
        parser.add_argument("--mod-configure", action="store", nargs='?', default="null", help="configure module")

        # Parse arguments
        args, unknown = parser.parse_known_args()

        #
        # If --version param has been set
        #
        if args.version != "null":
            if args.version:
                print(' Current version: ' + myApp.getVersion())
                myExit.cleanExit() 

        #
        # If --verbosity param has been set
        #
        if args.verbosity != "null":
            Args.verbosity = True

        #
        # If --assume-yes param has been set
        #
        if args.assume_yes != "null":
            Args.assume_yes = True

        #
        # If --profile param has been set
        #
        if args.profile != "null":
            try:
                # If a profile is set (not 'None'), change the app profile
                if args.profile:
                    # Get current profile
                    currentProfile = myAppConfig.getProfile()

                    # If a profile was already set
                    if currentProfile:
                        # Print profile change
                        print(' Switching from profile ' + Fore.YELLOW + currentProfile + Style.RESET_ALL + ' to ' + Fore.YELLOW + args.profile + Style.RESET_ALL)
                    else:
                        # Print profile change
                        print(' Switching to profile ' + Fore.YELLOW + args.profile + Style.RESET_ALL)

                    # Set new profile
                    myAppConfig.setProfile(args.profile)
                # Else print the current profile
                else:
                    print(' Current profile: ' + Fore.YELLOW + myAppConfig.getProfile() + Style.RESET_ALL)
            except Exception as e:
                print(Fore.YELLOW + ' Error while changing profile: ' + str(e) + Style.RESET_ALL)
                myExit.cleanExit(1)    

            myExit.cleanExit()

        #
        # If --env param has been set
        #
        if args.env != "null":
            try:
                # If a environment is set (not 'None'), change the app environment
                if args.env:
                    # Get current environment
                    currentEnvironment = myAppConfig.getEnvironment()

                    # Print environment change
                    print(' Switching from environment ' + Fore.YELLOW + currentEnvironment + Style.RESET_ALL + ' to ' + Fore.YELLOW + args.env + Style.RESET_ALL)

                    # Set new environment
                    myAppConfig.setEnvironment(args.env)
                # Else print the current environment
                else:
                    print('Current environment: ' + Fore.YELLOW + myAppConfig.getEnvironment() + Style.RESET_ALL)
            except Exception as e:
                print(Fore.YELLOW + ' Error while changing environment: ' + str(e) + Style.RESET_ALL)
                myExit.cleanExit(1)    

            myExit.cleanExit()

        #
        # If --ignore-exclude param has been set
        #
        if args.ignore_exclude != "null":
            Args.ignore_exclude = True

        #
        # If --check-updates param has been set
        #
        if args.check_updates != "null":
            Args.check_updates = True

        #
        # If --dist-upgrade param has been set
        #
        if args.dist_upgrade != "null":
            Args.dist_upgrade = True

        #
        # If --keep-oldconf param has been set
        #
        if args.keep_oldconf != "null":
            Args.keep_oldconf = True

        #
        # If --get-exclude param has been set
        #
        if args.get_exclude != "null":
            print(' Currently excluded packages: ' + Fore.YELLOW + str(myAppConfig.getExclude()) + Style.RESET_ALL)
            myExit.cleanExit()

        #
        # If --get-exclude-major param has been set
        #
        if args.get_exclude_major != "null":
            print(' Currently excluded packages on major update: ' + Fore.YELLOW + str(myAppConfig.getExcludeMajor()) + Style.RESET_ALL)
            myExit.cleanExit()

        #
        # If --get-service-restart param has been set
        #
        if args.get_service_restart != "null":
            print(' Services to restart after package update: ' + Fore.YELLOW + str(myAppConfig.getServiceToRestart()) + Style.RESET_ALL)
            myExit.cleanExit()

        #
        # If --exclude param has been set
        #
        if args.exclude != "null":
            try:
                myAppConfig.setExclude(args.exclude)

                print(' Excluding packages: ' + Fore.YELLOW + str(myAppConfig.getExclude()) + Style.RESET_ALL)
            except Exception as e:
                print(Fore.YELLOW + ' Error while excluding packages: ' + str(e) + Style.RESET_ALL)
                myExit.cleanExit(1)

            myExit.cleanExit()

        #
        # If --exclude-major param has been set
        #
        if args.exclude_major != "null":
            try:
                myAppConfig.setExcludeMajor(args.exclude_major)

                print(' Excluding packages on major update: ' + Fore.YELLOW + str(myAppConfig.getExcludeMajor()) + Style.RESET_ALL)
            except Exception as e:
                print(Fore.YELLOW + ' Error while excluding packages on major update: ' + str(e) + Style.RESET_ALL)
                myExit.cleanExit(1)

            myExit.cleanExit()

        #
        # If --service-restart param has been set
        #
        if args.service_restart != "null":
            try:
                myAppConfig.setServiceToRestart(args.service_restart)

                print(' Services to restart after package update: ' + Fore.YELLOW + str(myAppConfig.getServiceToRestart()) + Style.RESET_ALL)
            except Exception as e:
                print(Fore.YELLOW + ' Error while setting services to restart after package update: ' + str(e) + Style.RESET_ALL)
                myExit.cleanExit(1)

            myExit.cleanExit()
        
        #
        # If --mod-list param has been set
        #
        if args.mod_list != "null":
            myModule.list()
            myExit.cleanExit()

        #
        # If --mod-enable param has been set
        #
        if args.mod_enable != "null":
            # If module to enable is set (not 'None'), enable the module
            if args.mod_enable:
                # Enable module
                try:
                    myModule.enable(args.mod_enable)
                    myExit.cleanExit()
                except Exception as e:
                    print(Fore.YELLOW + ' Error while enabling module: ' + str(e) + Style.RESET_ALL)
                    myExit.cleanExit(1)

        #
        # If --mod-disable param has been set
        #
        if args.mod_disable != "null":
            # If module to disable is set (not 'None'), disable the module
            if args.mod_disable:
                # Disable module
                try:
                    myModule.disable(args.mod_disable)
                    myExit.cleanExit()
                except Exception as e:
                    print(Fore.YELLOW + ' Error while disabling module: ' + str(e) + Style.RESET_ALL)
                    myExit.cleanExit(1)

        #
        # If --mod-configure param has been set
        #
        if args.mod_configure != "null":
            # If module to configure is set (not 'None'), configure the module
            if args.mod_configure:
                # Configure module
                myModule.configure(args.mod_configure)
                myExit.cleanExit()
