# coding: utf-8

# Import constants
from constant import *

# Import libraries
from datetime import datetime
from pathlib import Path
from colorama import Fore, Back, Style
import sys, socket, yaml, getpass, subprocess

# Import classes
from src.controllers.App.Config import Config
from src.controllers.System import System

class App:
    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return current version of the application
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getVersion(self):
        file = open(ROOT + '/version', 'r')
        version = file.read()

        return version


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return linupdate configuration from config file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getConf(self):
        # Open YAML config file:
        with open(CONF) as stream:
            try:
                # Read YAML and return profile
                data = yaml.safe_load(stream)
                return data

            except yaml.YAMLError as exception:
                print(exception)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Get linupdate daemon agent status
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getAgentStatus(self):
        result = subprocess.run(
            ["systemctl", "is-active", "linupdate"],
            capture_output = True,
            text = True
        )

        if result.returncode != 0:
            return 'stopped'
        
        return 'running'


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Create lock file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setLock(self):
        Path('/tmp/linupdate.lock').touch()

    
    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Remove lock file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def removeLock(self):
        Path('/tmp/linupdate.lock').unlink()


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Create base directories
    #
    #-------------------------------------------------------------------------------------------------------------------
    def initialize(self):
        Path(ROOT).mkdir(parents=True, exist_ok=True)
        Path(ETC_DIR).mkdir(parents=True, exist_ok=True)
        Path(MODULES_CONF_DIR).mkdir(parents=True, exist_ok=True)
        Path(SERVICE_DIR).mkdir(parents=True, exist_ok=True)
        Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)

        # Set permissions
        Path(ROOT).chmod(0o750)
        Path(SRC_DIR).chmod(0o750)
        Path(ETC_DIR).chmod(0o750)
        Path(MODULES_CONF_DIR).chmod(0o750)
        Path(SERVICE_DIR).chmod(0o750)
        Path(LOGS_DIR).chmod(0o750)

        # Check if the .src directory is empty
        if not len(list(Path(SRC_DIR).rglob('*'))):
            print(Fore.YELLOW + 'Linupdate core files are missing. You might reinstall linupdate.' + Style.RESET_ALL)
            exit(1)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Print app logo
    #
    #-------------------------------------------------------------------------------------------------------------------
    def printLogo(self):
        space = ' '
        # print(Fore.YELLOW)
        print(space + '                             __                                        ')
        print(space + '.__  .__            ____  __( o`-               .___       __          ')
        print(space + '|  | |__| ____  __ _\   \/  /  \__ ________   __| _/____ _/  |_  ____  ')
        print(space + '|  | |  |/    \|  |  \     /|  |  |  \____ \ / __ |\__  \\   ___/ __ \ ')
        print(space + '|  |_|  |   |  |  |  /     \ ^^|  |  |  |_> / /_/ | / __ \|  | \  ___/ ')
        print(space + '|____|__|___|  |____/___/\  \  |____/|   __/\____ |(____  |__|  \___  >')
        print(space + '             \/           \_/        |__|        \/     \/          \/ \n')

        print(' Package updater for linux distributions\n')


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Print system and app summary
    #
    #-------------------------------------------------------------------------------------------------------------------
    def printSummary(self, fromAgent: bool = False):
        myAppConfig = Config()
        mySystem = System()

        # Define execution method
        if fromAgent:
            exec_method = 'automatic (agent)'
        else:
            if not sys.stdin.isatty():
                exec_method = 'automatic (no tty)'
            else:
                exec_method = 'manual (tty)'

        print(' Hostname:            ' + Fore.YELLOW + socket.gethostname() + Style.RESET_ALL)
        print(' OS:                  ' + Fore.YELLOW + mySystem.getOsName() + ' ' + mySystem.getOsVersion() + Style.RESET_ALL)
        print(' Kernel:              ' + Fore.YELLOW + mySystem.getKernel() + Style.RESET_ALL)
        print(' Virtualization:      ' + Fore.YELLOW + mySystem.getVirtualization() + Style.RESET_ALL)
        print(' Profile:             ' + Fore.YELLOW + myAppConfig.getProfile() + Style.RESET_ALL)
        print(' Environment:         ' + Fore.YELLOW + myAppConfig.getEnvironment() + Style.RESET_ALL)
        print(' Execution date:      ' + Fore.YELLOW + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + Style.RESET_ALL)
        print(' Execution method:    ' + Fore.YELLOW + exec_method + Style.RESET_ALL)
        print(' Executed by user:    ' + Fore.YELLOW + getpass.getuser() + Style.RESET_ALL + '\n')
