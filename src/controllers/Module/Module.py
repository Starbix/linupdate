# coding: utf-8

# Import constants
from constant import *

# Import libraries
from colorama import Fore, Back, Style
import os
import importlib

# Import classes
from src.controllers.App.Config import Config
from src.controllers.Exit import Exit

class Module:
    def __init__(self):
        self.configController = Config()
        self.exitController = Exit()
        self.loadedModules = []

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   List available modules
    #
    #-------------------------------------------------------------------------------------------------------------------
    def list(self):
        # List all modules
        print(' Available modules:')
        for module in os.listdir(ROOT + '/src/controllers/Module'):
            # Ignore cache files
            if module == '__pycache__':
                continue
            
            # Ignore non directories 
            if not os.path.isdir(ROOT + '/src/controllers/Module/' + module):
                continue

            print('  - ' + Fore.YELLOW + module.lower() + Style.RESET_ALL)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Enable a module
    #
    #-------------------------------------------------------------------------------------------------------------------
    def enable(self, module):
        # Retrieve configuration
        configuration = self.configController.getConf()

        # Loop through modules
        for mod in module.split(','):
            # Check if module exists
            if not self.exists(mod):
                raise Exception('Module ' + mod + ' does not exist')
            
            # Continue if module is already enabled
            if mod in configuration['modules']['enabled']:
                print(Fore.GREEN + ' Module ' + mod + ' is already enabled' + Style.RESET_ALL)
                continue

            # Enable module
            self.configController.appendModule(mod)

            # Print enabled modules
            print(' Module ' + Fore.YELLOW + mod + Style.RESET_ALL + ' enabled')


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Disable a module
    #
    #-------------------------------------------------------------------------------------------------------------------
    def disable(self, module):
        # Retrieve configuration
        configuration = self.configController.getConf()

        # Loop through modules
        for mod in module.split(','):
            # Check if module exists
            if not self.exists(mod):
                raise Exception('Module ' + mod + ' does not exist')
            
            # Continue if module is already disabled
            if mod not in configuration['modules']['enabled']:
                print(Fore.YELLOW + ' Module ' + mod + ' is already disabled' + Style.RESET_ALL)
                continue
        
            # Disable module
            self.configController.removeModule(mod)

            # Print disabled modules
            print(' Module ' + Fore.YELLOW + mod + Style.RESET_ALL + ' disabled')


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Configure a module
    #
    #-------------------------------------------------------------------------------------------------------------------
    def configure(self, module):
        # Check if module exists
        if not self.exists(module):
            raise Exception('Module ' + module + ' does not exist')
        
        # Convert module name tu uppercase first letter
        moduleName = module.capitalize()

        # Import python module class
        moduleImportPath = importlib.import_module('src.controllers.Module.'+ moduleName + '.' + moduleName)
        moduleClass = getattr(moduleImportPath, moduleName)

        # Instanciate module and call module load method
        myModule = moduleClass()
        myModule.main()


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return True if module exists
    #
    #-------------------------------------------------------------------------------------------------------------------
    def exists(self, module):
        # Check if module class file exists
        if not os.path.exists(ROOT + '/src/controllers/Module/' + module.capitalize() + '/' + module.capitalize() + '.py'):
            return False
        
        return True


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Load enabled modules
    #
    #-------------------------------------------------------------------------------------------------------------------
    def load(self):
        # Retrieve configuration
        configuration = self.configController.getConf()

        # Quit if no modules are enabled
        if not configuration['modules']['enabled']:
            return
        
        print(' Loading modules')
    
        # Loop through modules
        for module in configuration['modules']['enabled']:
            try:
                # Convert module name tu uppercase first letter
                moduleName = module.capitalize()

                # Import python module class
                moduleImportPath = importlib.import_module('src.controllers.Module.'+ moduleName + '.' + moduleName)
                moduleClass = getattr(moduleImportPath, moduleName)

                # Instanciate module and call module load method
                myModule = moduleClass()
                myModule.load()

                print(Fore.GREEN + '  ✔ ' + Style.RESET_ALL + module + ' module loaded ')

                # Add module to the list of loaded modules
                self.loadedModules.append(module)

            except Exception as e:
                raise Exception('Could not load module ' + module + ': ' + str(e) + Style.RESET_ALL)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Execute modules pre-update actions (loaded modules only)
    #
    #-------------------------------------------------------------------------------------------------------------------
    def pre(self):
        for module in self.loadedModules:
            try:
                print('\n Executing ' + Fore.YELLOW + module + Style.RESET_ALL + ' pre-update actions')
                # Convert module name to uppercase first letter
                moduleName = module.capitalize()

                # Import python module class
                moduleImportPath = importlib.import_module('src.controllers.Module.'+ moduleName + '.' + moduleName)
                moduleClass = getattr(moduleImportPath, moduleName)

                # Instanciate module and call module pre method
                myModule = moduleClass()
                myModule.pre()

            except Exception as e:
                raise Exception('Could not execute pre-update actions for module ' + module + ': ' + str(e) + Style.RESET_ALL)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Execute modules post-update actions
    #
    #-------------------------------------------------------------------------------------------------------------------
    def post(self, updateSummary):
        for module in self.loadedModules:
            try:
                print('\n Executing ' + Fore.YELLOW + module + Style.RESET_ALL + ' post-update actions')
                # Convert module name to uppercase first letter
                moduleName = module.capitalize()

                # Import python module class
                moduleImportPath = importlib.import_module('src.controllers.Module.'+ moduleName + '.' + moduleName)
                moduleClass = getattr(moduleImportPath, moduleName)

                # Instanciate module and call module post method
                myModule = moduleClass()
                myModule.post(updateSummary)

            except Exception as e:
                raise Exception('Could not execute post-update actions for module ' + module + ': ' + str(e) + Style.RESET_ALL)
