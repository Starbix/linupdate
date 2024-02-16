# coding: utf-8

# Import constants
from constant import *

# Import libraries
from pathlib import Path
from colorama import Fore, Back, Style
import yaml
import ipaddress

# Import classes
from src.controllers.System import System
from src.controllers.App.Config import Config as appConfig
from src.controllers.HttpRequest import HttpRequest
from src.controllers.App.Utils import Utils

class Config:
    def __init__(self):
        self.conf = MODULES_CONF_DIR + '/reposerver.yml'
        self.systemController = System()
        self.appConfigController = appConfig()
        self.httpRequestController = HttpRequest()
        self.utilsController = Utils()

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Generate reposerver config file if not exist
    #
    #-------------------------------------------------------------------------------------------------------------------
    def generateConf(self):
        # Quit if the config file already exists
        if Path(self.conf).is_file():
            return
        
        print(' Generating Reposerver module configuration file')

        # Minimal config file
        data = {
            '#': 'Reposerver configuration',
            'reposerver': {
                'url': '',
                'ip': '',
                'package_type': [],
            },
            '#': 'This host configuration',
            'client': {
                'id': '',
                'token': '',
                'get_profile_pkg_conf_from_reposerver': True,
                'get_profile_repos_from_reposerver': True,
                'profile': {
                    'repos': {
                        'clear_before_update': True
                    }
                }
            },
            '#': 'Agent configuration',
            'agent': {
                'enabled': False,
                'listen': {
                    'enabled': True,
                    'interface': 'auto'
                }
            }
        }

        # Write config file
        with open(self.conf, 'w') as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return current reposerver URL
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getUrl(self):
        # Get current configuration
        configuration = self.getConf()

        # Check if url exists in configuration and is not empty
        if 'url' not in configuration['reposerver']:
            raise Exception(' Reposerver URL not found in configuration file')
        
        if configuration['reposerver']['url'] == '':
            raise Exception(' No Reposerver URL set. Please set a URL with --url <url> option')

        # Return URL
        return configuration['reposerver']['url']
        

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Set reposerver URL
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setUrl(self, url):
        # Check that url is valid (start with http(s)://)
        if not url.startswith('http://') and not url.startswith('https://'):
            raise Exception('Reposerver URL must start with http:// or https://')

        # Get current configuration
        configuration = self.getConf()

        # Set url
        configuration['reposerver']['url'] = url

        # Write config file
        self.writeConf(configuration)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return reposerver configuration
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getConf(self):
        # Open YAML config file
        with open(self.conf, 'r') as stream:
            try:
                # Read YAML and return profile
                return yaml.safe_load(stream)

            except yaml.YAMLError as exception:
                print(exception)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Write reposerver configuration to config file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def writeConf(self, configuration):
        # Write config file
        with open(self.conf, 'w') as file:
            yaml.dump(configuration, file, default_flow_style=False, sort_keys=False)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Check if the config file exists and if it contains the required parameters
    #
    #-------------------------------------------------------------------------------------------------------------------
    def checkConf(self):
        if not Path(self.conf).is_file():
            raise Exception('Reposerver module configuration file not found')
        
        # Retrieve configuration
        configuration = self.getConf()

        # Check if reposerver section exists
        if 'reposerver' not in configuration:
            raise Exception('Reposerver section not found in configuration file')
        
        # Check if url exists
        if 'url' not in configuration['reposerver']:
            raise Exception('Reposerver URL not found in configuration file')
        
        # Check if ip exists
        if 'ip' not in configuration['reposerver']:
            raise Exception('Reposerver IP not found in configuration file')
        
        # Check if package_type exists
        if 'package_type' not in configuration['reposerver']:
            raise Exception('Reposerver package_type not found in configuration file')

        # Check if client section exists
        if 'client' not in configuration:
            raise Exception('Client section not found in configuration file')
        
        # Check if id exists
        if 'id' not in configuration['client']:
            raise Exception('Client Id not found in configuration file')
        
        # Check if token exists
        if 'token' not in configuration['client']:
            raise Exception('Client token not found in configuration file')
        
        # Check if get_profile_pkg_conf_from_reposerver exists and is set (True or False)
        if 'get_profile_pkg_conf_from_reposerver' not in configuration['client']:
            raise Exception('Client get_profile_pkg_conf_from_reposerver not found in configuration file')
        
        if configuration['client']['get_profile_pkg_conf_from_reposerver'] not in [True, False]:
            raise Exception('Client get_profile_pkg_conf_from_reposerver must be set to True or False')

        # Check if get_profile_repos_from_reposerver exists and is set (True or False)
        if 'get_profile_repos_from_reposerver' not in configuration['client']:
            raise Exception('Client get_profile_repos_from_reposerver not found in configuration file')
        
        if configuration['client']['get_profile_repos_from_reposerver'] not in [True, False]:
            raise Exception('Client get_profile_repos_from_reposerver must be set to True or False')
        
        # Check if profile section exists
        if 'profile' not in configuration['client']:
            raise Exception('Client profile section not found in configuration file')
        
        # Check if repos section exists
        if 'repos' not in configuration['client']['profile']:
            raise Exception('Client profile repos section not found in configuration file')
        
        # Check if clear_before_update exists and is set (True or False)
        if 'clear_before_update' not in configuration['client']['profile']['repos']:
            raise Exception('Client profile repos clear_before_update not found in configuration file')
        
        if configuration['client']['profile']['repos']['clear_before_update'] not in [True, False]:
            raise Exception('Client profile repos clear_before_update must be set to True or False')
        
        # Check if agent section exists
        if 'agent' not in configuration:
            raise Exception('Agent section not found in configuration file')
        
        # Check if enabled exists and is set (True or False)
        if 'enabled' not in configuration['agent']:
            raise Exception('Agent enabled not found in configuration file')
        
        if configuration['agent']['enabled'] not in [True, False]:
            raise Exception('Agent enabled must be set to True or False')
        
        # Check if listen section exists
        if 'listen' not in configuration['agent']:
            raise Exception('Agent listen section not found in configuration file')
        
        # Check if enabled exists and is set (True or False)
        if 'enabled' not in configuration['agent']['listen']:
            raise Exception('Agent listen enabled not found in configuration file')
        
        if configuration['agent']['listen']['enabled'] not in [True, False]:
            raise Exception('Agent listen enabled must be set to True or False')
        
        # Check if interface exists
        if 'interface' not in configuration['agent']['listen']:
            raise Exception('Agent listen interface not found in configuration file')
            

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Enable or disable configuration update from reposerver
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setAllowConfUpdate(self, value: bool):
        # Get current configuration
        configuration = self.getConf()

        # Set allow_conf_update
        configuration['client']['get_profile_pkg_conf_from_reposerver'] = value

        # Write config file
        self.writeConf(configuration)

        print(' Allow configuration update from reposerver set to ' + str(value))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Enable or disable repositories configuration update from reposerver
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setAllowReposUpdate(self, value: bool):
        # Get current configuration
        configuration = self.getConf()

        # Set allow_repos_update
        configuration['client']['get_profile_repos_from_reposerver'] = value

        # Write config file
        self.writeConf(configuration)

        print(' Allow repositories update from reposerver set to ' + str(value))


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Get authentication id
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getId(self):
        # Get current configuration
        configuration = self.getConf()

        # Return Id
        return configuration['client']['id']


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Set authentication id
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setId(self, id: str):
        # Get current configuration
        configuration = self.getConf()

        # Set Id
        configuration['client']['id'] = id

        # Write config file
        self.writeConf(configuration)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Get authentication token
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getToken(self):
        # Get current configuration
        configuration = self.getConf()

        # Return Token
        return configuration['client']['token']


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Set authentication token
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setToken(self, token: str):
        # Get current configuration
        configuration = self.getConf()

        # Set Token
        configuration['client']['token'] = token

        # Write config file
        self.writeConf(configuration)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Get global configuration from reposerver
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getReposerverConf(self):
        print('  ▪ Getting reposerver configuration:', end=' ')

        # Get reposerver URL
        url = self.getUrl()

        # Get auth Id and token
        id = self.getId()
        token = self.getToken()
        
        # Do not print message if aknowledge request has been sent successfully
        # self.httpRequestController.quiet = True
        results = self.httpRequestController.get(url + '/api/v2/profile/server-settings', id, token)

        # Parse results

        # Check if IP has been send by the server
        if 'Ip' not in results[0]:
            raise Exception('Reposerver did not send its IP address')

        # Check if package type has been send by the server
        if 'Package_type' not in results[0]:
            raise Exception('Reposerver did not send its package type')

        # Set server IP
        self.setServerIp(results[0]['Ip'])

        # Set server package type
        self.setServerPackageType(results[0]['Package_type'])

        print('[' + Fore.GREEN + ' OK ' + Style.RESET_ALL + ']')


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Get profile packages configuration (excludes) from reposerver
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getProfilePackagesConf(self):
        # Get current configuration
        configuration = self.getConf()

        # Get reposerver URL
        url = self.getUrl()

        # Get current profile, auth Id and token
        profile = self.appConfigController.getProfile()
        id = self.getId()
        token = self.getToken()

        print('  ▪ Getting ' + Fore.YELLOW + profile + Style.RESET_ALL + ' profile packages configuration:', end=' ')

        # Check if getting profile packages configuration from reposerver is enabled
        if configuration['client']['get_profile_pkg_conf_from_reposerver'] == False:
            print(Fore.YELLOW + 'Disabled' + Style.RESET_ALL)
            return

        # Check if profile is not empty
        if not profile:
            raise Exception('No profile set. Please set a profile with --profile <profile> option')
        
        # Check if Id and token are not empty
        if not id or not token:
            raise Exception('No auth Id or token found in configuration')

        # Retrieve configuration from reposerver
        results = self.httpRequestController.get(url + '/api/v2/profile/' + profile + '/excludes', id, token, 2)

        # Parse results

        # Packages to exclude no matter the version
        if results[0]['Package_exclude'] != "null":
            # First, clear the exclude list
            self.appConfigController.setExclude()

            # Then, set the new exclude list
            self.appConfigController.setExclude(results[0]['Package_exclude'])

        # Packages to exclude on major version
        if results[0]['Package_exclude_major'] != "null":
            # First, clear the exclude major list
            self.appConfigController.setExcludeMajor()

            # Then, set the new exclude major list
            self.appConfigController.setExcludeMajor(results[0]['Package_exclude_major'])

        # Service to restart after an update
        if results[0]['Service_restart'] != "null":
            # First clear the services to restart
            self.appConfigController.setServiceToRestart()
            
            # Then set the new services to restart
            self.appConfigController.setServiceToRestart(results[0]['Service_restart'])

        print('[' + Fore.GREEN + ' OK ' + Style.RESET_ALL + ']')


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Get profile repositories configuration from reposerver
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getProfileRepos(self):
        # Get current configuration
        configuration = self.getConf()

        # Get reposerver URL
        url = self.getUrl()

        # Get current profile, auth Id and token
        profile = self.appConfigController.getProfile()
        env = self.appConfigController.getEnvironment()
        id = self.getId()
        token = self.getToken()

        print('  ▪ Getting ' + Fore.YELLOW + profile + Style.RESET_ALL + ' profile repositories:', end=' ')

        # Check if getting profile packages configuration from reposerver is enabled
        if configuration['client']['get_profile_repos_from_reposerver'] == False:
            print(Fore.YELLOW + 'Disabled' + Style.RESET_ALL)
            return

        # Check if profile is not empty
        if not profile:
            raise Exception('No profile set. Please set a profile with --profile <profile> option')
        
        # Check if environment is not empty
        if not env:
            raise Exception('No environment set. Please set an environment with --env <environment> option')
        
        # Check if Id and token are not empty
        if not id or not token:
            raise Exception('No auth Id or token found in configuration')

        # Retrieve configuration from reposerver
        results = self.httpRequestController.get(url + '/api/v2/profile/' + profile + '/repos', id, token, 2)

        # Parse results

        # Quit if no results
        if not results:
            print(Fore.YELLOW + 'No repositories configured ' + Style.RESET_ALL)
            return
        
        # Clear current repositories if enabled
        if configuration['client']['profile']['repos']['clear_before_update']:
            # Debian
            if self.systemController.getOsFamily() == 'Debian':
                # Clear /etc/apt/sources.list
                with open('/etc/apt/sources.list', 'w') as file:
                    file.write('')
                
                # Delete all files in /etc/apt/sources.list.d
                for file in Path('/etc/apt/sources.list.d/').glob('*.list'):
                    file.unlink()

            # Redhat
            if self.systemController.getOsFamily() == 'Redhat':
                # Delete all files in /etc/yum.repos.d
                for file in Path('/etc/yum.repos.d/').glob('*.repo'):
                    file.unlink()

        # Create each repo file
        for result in results:
            # Depending on the OS family, the repo files are stored in different directories

            # Debian
            if self.systemController.getOsFamily() == 'Debian':
                reposRoot = '/etc/apt/sources.list.d'

            # Redhat
            if self.systemController.getOsFamily() == 'Redhat':
                reposRoot = '/etc/yum.repos.d'

            # Insert description at the top of the file, then content
            # Replace __ENV__ with current environment on the fly
            with open(reposRoot + '/' + result['filename'], 'w') as file:
                # Insert description
                file.write('# ' + result['description'] + '\n' + result['content'].replace('__ENV__', env) + '\n')

            # Set permissions
            Path(reposRoot + '/' + result['filename']).chmod(0o660)
                
            # Reload cache
            # if self.systemController.getOsFamily() == 'Debian':
                # TODO : utiliser le controller Apt pour vider le cache


            # if self.systemController.getOsFamily() == 'Redhat':
                # TODO

        print('[' + Fore.GREEN + ' OK ' + Style.RESET_ALL + ']')


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Set reposerver IP in configuration file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setServerIp(self, ip):
        # Check that IP is valid
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise Exception('Invalid Reposerver IP address ' + ip)

        # Get current configuration
        configuration = self.getConf()

        # Set server ip
        configuration['reposerver']['ip'] = ip

        # Write config file
        self.writeConf(configuration)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Set reposerver package type in configuration file
    #
    #-------------------------------------------------------------------------------------------------------------------
    def setServerPackageType(self, packageType):
        # Get current configuration
        configuration = self.getConf()

        # First clear the package type list
        configuration['reposerver']['package_type'] = []

        # For each package type, append it to the list if not already in
        for item in packageType.split(","):
            if item not in configuration['reposerver']['package_type']:
                # Append package type
                configuration['reposerver']['package_type'].append(item)

        # Write config file
        self.writeConf(configuration)
