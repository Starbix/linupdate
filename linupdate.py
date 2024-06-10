#!/usr/bin/python
# coding: utf-8

# Import constants
from constant import *

# Import libraries
from colorama import Fore, Back, Style
from pathlib import Path
from datetime import datetime
import socket

# Import classes
from src.controllers.Log import Log
from src.controllers.App.App import App
from src.controllers.App.Config import Config
from src.controllers.Args import Args
from src.controllers.System import System
from src.controllers.Module.Module import Module
from src.controllers.Package.Package import Package
from src.controllers.Exit import Exit


#-------------------------------------------------------------------------------------------------------------------
#
#   Main function
#
#-------------------------------------------------------------------------------------------------------------------
def main():
    try:
        # Instanciate classes
        myExit      = Exit()
        myApp       = App()
        myAppConfig = Config()
        myArgs      = Args()
        mySystem    = System()
        myModule    = Module()
        myPackage   = Package()

        # Get current date and time
        todaydatetime = datetime.now()
        date = todaydatetime.strftime('%Y-%m-%d')
        time = todaydatetime.strftime('%Hh%Mm%Ss')
        logsdir = '/var/log/linupdate'
        logfile = date + '_' + time + '_linupdate_' + socket.gethostname() + '.log'

        # Create logs directory
        Path(logsdir).mkdir(parents=True, exist_ok=True)
        Path(logsdir).chmod(0o750)

        # Pre-parse arguments to check if --from-agent param is passed
        myArgs.preParse()

        # If --from-agent param is passed, then add -agent to the log filename and make it hidden
        if myArgs.from_agent:
            logfile = '.' + date + '_' + time + '_linupdate_' + socket.gethostname() + '-agent.log'

        # Create log file with correct permissions
        Path(logsdir + '/' + logfile).touch()
        Path(logsdir + '/' + logfile).chmod(0o640)

        # Log everything to the log file
        with Log(logsdir + '/' + logfile):
            # Print Logo
            myApp.printLogo()

            # Exit if the user is not root
            if not mySystem.isRoot():
                print(Fore.YELLOW + 'Must be executed with sudo' + Style.RESET_ALL)
                myExit.cleanExit(1)

            # Check if the system is supported
            mySystem.check()

            # Create lock file
            myApp.setLock()

            # Create base directories
            myApp.initialize()

            # Generate config file if not exist
            myAppConfig.generateConf()

            # Check if there are missing parameters
            myAppConfig.checkConf()

            # Parse arguments
            myArgs.parse()

            # Print system & app summary
            myApp.printSummary(myArgs.from_agent)

            # Load modules
            myModule.load()

            # Execute pre-update modules functions
            myModule.pre()

            # Execute packages update
            myPackage.update(myArgs.assume_yes, myArgs.ignore_exclude, myArgs.check_updates, myArgs.dist_upgrade, myArgs.keep_oldconf)

            # Execute post-update modules functions
            myModule.post(myPackage.updateSummary)

            # Restart services
            # TODO

            # Check if reboot is required
            if mySystem.rebootRequired() == True:
                print(' ' + Fore.YELLOW + 'Reboot is required' + Style.RESET_ALL)

            # Send mail
            # TODO

    except Exception as e:
        print(' ' + Fore.YELLOW + str(e) + Style.RESET_ALL)
        myExit.cleanExit(1)

# Run main function
main()
