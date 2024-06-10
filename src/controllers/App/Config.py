# coding: utf-8

# Import constants
from constant import *

# Import libraries
from pathlib import Path
from colorama import Fore, Back, Style
import yaml

class Config:
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
    #   Check if the config file exists and if it contains the required parameters
    #
    #-------------------------------------------------------------------------------------------------------------------
    def checkConf(self):
        try:
            # Check if the config file exists
            if not Path(CONF).is_file():
                raise Exception('configuration file "' + CONF + '" is missing')

            # Retrieve configuration
            configuration = self.getConf()

            # Check if main section is set in the config file
            if 'main' not in configuration:
                raise Exception('main section is missing in the configuration file')
            
            # Check if profile is set in the config file
            if 'profile' not in configuration['main']:
                raise Exception('profile param is missing in the configuration file')
            
            if configuration['main']['profile'] == None:
                raise Exception('profile is empty in the configuration file')

            # Check if environment is set in the config file
            if 'environment' not in configuration['main']:
                raise Exception('environment param is missing in the configuration file')

            if configuration['main']['environment'] == None:
                raise Exception('environment is empty in the configuration file')
        
            # Check if mail_alert section is set in the config file
            if 'mail_alert' not in configuration['main']:
                raise Exception('mail_alert section is missing in the configuration file')
            
            # Check if enabled param is set in the mail_alert section
            if 'enabled' not in configuration['main']['mail_alert']:
                raise Exception('enabled param is missing in the mail_alert section')

            if configuration['main']['mail_alert']['enabled'] == None:
                raise Exception('enabled param is empty in the mail_alert section')
            
            # Check if recipient param is set in the mail_alert section
            if 'recipient' not in configuration['main']['mail_alert']:
                raise Exception('recipient param is missing in the mail_alert section')

            # Check if exit_on_package_update_error param is set in the main section
            if 'exit_on_package_update_error' not in configuration['main']:
                raise Exception('exit_on_package_update_error param is missing in the main section')
            
            if configuration['main']['exit_on_package_update_error'] == None:
                raise Exception('exit_on_package_update_error is empty in the main section')
            
            # Check if packages section is set in the config file
            if 'packages' not in configuration:
                raise Exception('packages section is missing in the configuration file')
            
            # Check if exclude section is set in the packages section
            if 'exclude' not in configuration['packages']:
                raise Exception('exclude section is missing in the packages section')
            
            # Check if always param is set in the exclude section
            if 'always' not in configuration['packages']['exclude']:
                raise Exception('always param is missing in the exclude section')
            
            # Check if on_major_update param is set in the exclude section
            if 'on_major_update' not in configuration['packages']['exclude']:
                raise Exception('on_major_update param is missing in the exclude section')
            
            # Check if services section is set in the config file
            if 'services' not in configuration:
                raise Exception('services section is missing in the configuration file')
            
            # Check if restart param is set in the services section
            if 'restart' not in configuration['services']:
                raise Exception('restart param is missing in the services section')
            
            # Check if modules section is set in the config file
            if 'modules' not in configuration:
                raise Exception('modules section is missing in the configuration file')
            
            # Check if enabled param is set in the modules section
            if 'enabled' not in configuration['modules']:
                raise Exception('enabled param is missing in the modules section')

        except Exception as e:
            raise Exception('Fatal configuration file error: ' + str(e) + Style.RESET_ALL)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Generate main config file if not exist
    #
    #-------------------------------------------------------------------------------------------------------------------
    def generateConf(self):
        # Quit if the config file already exists
        if Path(CONF).is_file():
            return

        # Minimal config file
        data = {
            'main': {
                'profile': 'PC',
                'environment': 'prod',

                'mail_alert': {
                    'enabled': False,
                    'recipient': ''
                },
                'exit_on_package_update_error': True,
            },
            'packages': {
                'exclude': {
                    'always': [],
                    'on_major_update': []
                }
            },
            'services': {
                'restart': [],
            },
            'modules': {
                'enabled': [],
            }
        }

        # Write config file
        try:
            with open(CONF, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise Exception('Could not create configuration file "' + CONF + '": ' + str(e))

    
    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Write linupdate configuration to config file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def writeConf(self, configuration):
        try:
            # Write config file
            with open(CONF, 'w') as file:
                yaml.dump(configuration, file, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise Exception('Could not write configuration file "' + CONF + '": ' + str(e))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return linupdate profile from config file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getProfile(self):
        # Open YAML config file:
        with open(CONF) as stream:
            try:
                # Read YAML and return profile
                data = yaml.safe_load(stream)
                return data['main']['profile']

            except yaml.YAMLError as exception:
                print(exception)
            

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Set linupdate profile in config file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setProfile(self, profile):
        # Get current configuration
        configuration = self.getConf()

        # Set profile
        configuration['main']['profile'] = profile

        # Write config file
        self.writeConf(configuration)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return linupdate environment from config file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getEnvironment(self):
        # Open YAML config file:
        with open(CONF, 'r') as stream:
            try:
                # Read YAML and return environment
                data = yaml.safe_load(stream)
                return data['main']['environment']

            except yaml.YAMLError as exception:
                print(exception)
        

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Set linupdate environment in config file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setEnvironment(self, environment):
        # Get current configuration
        configuration = self.getConf()

        # Set environment
        configuration['main']['environment'] = environment

        # Write config file
        self.writeConf(configuration)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return linupdate packages exclude list from config file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getExclude(self):
        # Open YAML config file:
        with open(CONF, 'r') as stream:
            try:
                # Read YAML and return exclude list
                data = yaml.safe_load(stream)
                return data['packages']['exclude']['always']

            except yaml.YAMLError as exception:
                print(exception)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Set linupdate packages exclude list in config file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setExclude(self, exclude: str = None):
        # Get current configuration
        configuration = self.getConf()

        # If no package to exclude, set empty list
        if not exclude:
            configuration['packages']['exclude']['always'] = []
        
        else:
            # For each package to exclude, append it to the list if not already in
            for item in exclude.split(","):
                if item not in configuration['packages']['exclude']['always']:
                    # Append exclude
                    configuration['packages']['exclude']['always'].append(item)

        # Write config file
        self.writeConf(configuration)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return linupdate packages exclude list on major update from config file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getExcludeMajor(self):
        # Open YAML config file:
        with open(CONF, 'r') as stream:
            try:
                # Read YAML and return exclude list
                data = yaml.safe_load(stream)
                return data['packages']['exclude']['on_major_update']

            except yaml.YAMLError as exception:
                print(exception)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Set linupdate packages exclude list on major update in config file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setExcludeMajor(self, exclude: str = None):
        # Get current configuration
        configuration = self.getConf()

        # If no package to exclude, set empty list
        if not exclude:
            configuration['packages']['exclude']['on_major_update'] = []

        else:
            # For each package to exclude, append it to the list if not already in
            for item in exclude.split(","):
                if item not in configuration['packages']['exclude']['on_major_update']:
                    # Append exclude
                    configuration['packages']['exclude']['on_major_update'].append(item)

        # Write config file
        self.writeConf(configuration)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Get services to restart
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getServiceToRestart(self):
        # Open YAML config file:
        with open(CONF, 'r') as stream:
            try:
                # Read YAML and return services to restart
                data = yaml.safe_load(stream)
                return data['services']['restart']

            except yaml.YAMLError as exception:
                print(exception)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Set services to restart
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setServiceToRestart(self, services: str = None):
        # Get current configuration
        configuration = self.getConf()

        # If no service to restart, set empty list
        if not services:
            configuration['services']['restart'] = []

        else:        
            # For each service to restart, append it to the list if not already in
            for item in services.split(","):
                if item not in configuration['services']['restart']:
                    # Append service
                    configuration['services']['restart'].append(item)

        # Write config file
        self.writeConf(configuration)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Append a module to the enabled list
    #
    #-------------------------------------------------------------------------------------------------------------------
    def appendModule(self, module):
        # Get current configuration
        configuration = self.getConf()

        # Add module to enabled list
        configuration['modules']['enabled'].append(module)

        # Write config file
        self.writeConf(configuration)

    
    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Remove a module from the enabled list
    #
    #-------------------------------------------------------------------------------------------------------------------
    def removeModule(self, module):
        # Get current configuration
        configuration = self.getConf()

        # Remove module from enabled list
        configuration['modules']['enabled'].remove(module)

        # Write config file
        self.writeConf(configuration)
