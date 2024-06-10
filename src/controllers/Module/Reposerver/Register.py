# coding: utf-8

# Import constants
from constant import *

# Import libraries
from colorama import Fore, Back, Style
import ipaddress
import socket

# Import classes
from src.controllers.Module.Reposerver.Config import Config
from src.controllers.HttpRequest import HttpRequest

class Register:
    def __init__(self):
        self.configController = Config()
        self.httpRequestController = HttpRequest()

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Register to reposerver
    #
    #-------------------------------------------------------------------------------------------------------------------
    def register(self, api_key: str, ip: str):
        # Get Reposerver URL
        url = self.configController.getUrl()

        # Check if URL is not null
        if url == '':
            raise Exception(Fore.YELLOW + 'You must configure the target Reposerver URL [--url <url>]' + Style.RESET_ALL)

        print('  ▪ Registering to ' + Fore.YELLOW + url + Style.RESET_ALL + ':')

        # Check if API key is not null
        if api_key == 'null':
            raise Exception(Fore.YELLOW + 'You must specify an API key from a Repomanager user account [--register --api-key <api-key>]' + Style.RESET_ALL)

        # If no IP has been specified (null), then retrieve the public IP of the host
        if ip == 'null':
            try:
                ip = self.httpRequestController.get('https://api.ipify.org', '', '', 2).text
            except Exception as e:
                raise Exception(Fore.YELLOW + 'Failed to retrieve public IP from https://api.ipify.org (resource might be temporarily unavailable): ' + str(e) + Style.RESET_ALL)

        # Check that the IP is valid
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise Exception(Fore.YELLOW + 'Invalid IP address ' + ip + Style.RESET_ALL)

        # Register to server using API key and IP (POST)
        data = {
            'ip': ip,
            'hostname': socket.gethostname()
        }

        results = self.httpRequestController.postToken(url + '/api/v2/host/registering', api_key, data)

        # If registration is successful, the server will return an Id and a token, set Id and token in configuration
        self.configController.setId(results['id'])
        self.configController.setToken(results['token'])


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Unregister from reposerver
    #
    #-------------------------------------------------------------------------------------------------------------------
    def unregister(self):
        # Get Reposerver URL
        url = self.configController.getUrl()

        # Check if URL is not null
        if url == '':
            raise Exception(Fore.YELLOW + 'You must configure the target Reposerver URL [--url <url>]' + Style.RESET_ALL)

        print('  ▪ Unregistering from ' + Fore.YELLOW + url + Style.RESET_ALL + ':')

        # Get Id and token from configuration
        id = self.configController.getId()
        token = self.configController.getToken()

        # Check if Id and token are not null
        if id == '':
            raise Exception(Fore.YELLOW + 'No auth Id found in configuration' + Style.RESET_ALL)
        
        if token == '':
            raise Exception(Fore.YELLOW + 'No auth token found in configuration' + Style.RESET_ALL)
        
        # Unregister from server using Id and token (DELETE)
        self.httpRequestController.delete(url + '/api/v2/host/registering', id, token)
