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
    def parse(self):
        # Default values
        Args.verbosity = False
        Args.assume_yes = False
        Args.check_updates = False
        Args.ignore_exclude = False
        Args.dist_upgrade = False
        Args.keep_oldconf = True

        myApp       = App()
        myAppConfig = Config()
        myModule    = Module()
        myExit      = Exit()

        try:
            # Parse arguments
            parser = argparse.ArgumentParser()

            # Define valid arguments

            # Version
            parser.add_argument("-V", "--version", action="store_true", default="null", help="Show version")
            # Verbosity
            parser.add_argument("-v", "--verbosity", action="store_true", default="null", help="Increase verbosity")
            # Force / assume-yes
            parser.add_argument("-y", "--assume-yes", action="store_true", default="null", help="Answer yes to all questions")
            # Check updates
            parser.add_argument("-cu", "--check-updates", action="store_true", default="null", help="Only check for updates and exit")
            # Ignore exclude
            parser.add_argument("-ie", "--ignore-exclude", action="store_true", default="null", help="Ignore all package exclusions")

            # Profile
            parser.add_argument("-p", "--profile", action="store", nargs='?', default="null", help="Print current profile or set profile")
            # Environment
            parser.add_argument("-e", "--env", action="store", nargs='?', default="null", help="Print current environment or set environment")
            
            # Dist upgrade
            parser.add_argument("-du", "--dist-upgrade", action="store_true", default="null", help="Perform a distribution upgrade (Debian based OS only)")
            # Keep oldconf
            parser.add_argument("--keep-oldconf", action="store_true", default="null", help="Keep old configuration files during package update (Debian based OS only)")

            # Get excluded packages
            parser.add_argument("--get-exclude", action="store", nargs='?', default="null", help="Get the list of packages to exclude from update")
            # Get excluded packages on major update
            parser.add_argument("--get-exclude-major", action="store", nargs='?', default="null", help="Get the list of packages to exclude from update (if package has a major version update)")
            # Get services to restart after package update
            parser.add_argument("--get-service-restart", action="store", nargs='?', default="null", help="Get the list of services to restart after package update")
            # Exclude
            parser.add_argument("--exclude", action="store", nargs='?', default="null", help="Set packages to exclude from update")
            # Exclude on major update
            parser.add_argument("--exclude-major", action="store", nargs='?', default="null", help="Set packages to exclude from update (if package has a major version update)")
            # Services to restart after package update
            parser.add_argument("--service-restart", action="store", nargs='?', default="null", help="Set services to restart after package update")

            # List modules
            parser.add_argument("--mod-list", action="store_true", default="null", help="List available modules")
            # Module enable
            parser.add_argument("--mod-enable", action="store", nargs='?', default="null", help="Enable module")
            # Module disable
            parser.add_argument("--mod-disable", action="store", nargs='?', default="null", help="Disable module")
            # Module configure
            parser.add_argument("--mod-configure", action="store", nargs='?', default="null", help="Configure module")

            # Parse arguments
            args, unknown = parser.parse_known_args()

            # If unknown arguments are passed
            # if unknown:
            #     raise Exception('unknown argument(s): ' + str(unknown))

        except Exception as e:
            raise Exception('Error while parsing arguments: ' + str(e))

        try:
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
                    
                    myExit.cleanExit()

                except Exception as e:
                    raise Exception('could not switch profile: ' + str(e))

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

                    myExit.cleanExit()

                except Exception as e:
                    raise Exception('could not switch environment: ' + str(e))


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
                packages = myAppConfig.getExclude()

                print(' Currently excluded packages: ' + Fore.YELLOW)

                for package in packages:
                    print('  ▪ ' + package)
                
                # If no package is excluded
                if not packages:
                    print('  ▪ None')

                print(Style.RESET_ALL)

                myExit.cleanExit()

            #
            # If --get-exclude-major param has been set
            #
            if args.get_exclude_major != "null":
                packages = myAppConfig.getExcludeMajor()

                print(' Currently excluded packages on major update: ' + Fore.YELLOW)

                for package in packages:
                    print('  ▪ ' + package)

                # If no package is excluded
                if not packages:
                    print('  ▪ None')

                print(Style.RESET_ALL)

                myExit.cleanExit()

            #
            # If --get-service-restart param has been set
            #
            if args.get_service_restart != "null":
                services = myAppConfig.getServiceToRestart()

                print(' Services to restart after package update: ' + Fore.YELLOW)

                for service in services:
                    print('  ▪ ' + service)

                # If no service is set to restart
                if not services:
                    print('  ▪ None')

                print(Style.RESET_ALL)

                myExit.cleanExit()

            #
            # If --exclude param has been set
            #
            if args.exclude != "null":
                try:
                    # Exclude packages
                    myAppConfig.setExclude(args.exclude)

                    # Print excluded packages
                    packages = myAppConfig.getExclude()

                    print(' Excluding packages: ' + Fore.YELLOW)
                    
                    for package in packages:
                        print('  ▪ ' + package)

                    # If no package is excluded
                    if not packages:
                        print('  ▪ None')

                    print(Style.RESET_ALL)

                    myExit.cleanExit()
                except Exception as e:
                    raise Exception('Could not exclude packages: ' + str(e))

            #
            # If --exclude-major param has been set
            #
            if args.exclude_major != "null":
                try:
                    # Exclude packages on major update
                    myAppConfig.setExcludeMajor(args.exclude_major)

                    # Print excluded packages
                    packages = myAppConfig.getExcludeMajor()

                    print(' Excluding packages on major update: ' + Fore.YELLOW)

                    for package in packages:
                        print('  ▪ ' + package)

                    # If no package is excluded
                    if not packages:
                        print('  ▪ None')

                    print(Style.RESET_ALL)

                    myExit.cleanExit()
                except Exception as e:
                    raise Exception('Could not exclude packages on major update: ' + str(e))

            #
            # If --service-restart param has been set
            #
            if args.service_restart != "null":
                try:
                    # Set services to restart after package update
                    myAppConfig.setServiceToRestart(args.service_restart)

                    # Print services to restart
                    services = myAppConfig.getServiceToRestart()

                    print(' Setting services to restart after package update: ' + Fore.YELLOW)

                    for service in services:
                        print('  ▪ ' + service)

                    # If no service is set to restart
                    if not services:
                        print('  ▪ None')

                    print(Style.RESET_ALL)

                    myExit.cleanExit()
                except Exception as e:
                    raise Exception('Could not set services to restart after package update: ' + str(e))
            
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
                        raise Exception('Could not enable module: ' + str(e))

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
                        raise Exception('Could not disable module: ' + str(e))

            #
            # If --mod-configure param has been set
            #
            if args.mod_configure != "null":
                # If module to configure is set (not 'None'), configure the module
                if args.mod_configure:
                    try:
                        # Configure module
                        myModule.configure(args.mod_configure)
                        myExit.cleanExit()
                    except Exception as e:
                        raise Exception('Could not configure ' + args.mod_configure + ' module: ' + str(e))

        except Exception as e:
            raise Exception(str(e))
