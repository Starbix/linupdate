# coding: utf-8

# Import libraries
import subprocess
import re
from colorama import Fore, Style

# Import classes
from src.controllers.App.Config import Config

class Service:
    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Restart services
    #
    #-------------------------------------------------------------------------------------------------------------------
    def restart(self, update_summary: list):
        # Retrieve services to restart
        services = Config().getServiceToRestart()

        # Retrieve updated packages list from update summary
        updated_packages = update_summary['update']['success']['packages']

        # Restart services
        for service in services:
            # Check if there is a condition to restart the service (got a : in the service name)
            if ':' in service:
                # Split service name and package name
                service, package = service.split(':')

                # Check if the package is in the list of updated packages
                regex = '(?:% s)' % '|'.join(updated_packages)

                # If the package is not in the list of updated packages, skip the service
                if not re.match(regex, package):
                    continue

            print('Restarting ' + Fore.YELLOW + service + Style.RESET_ALL + ' service:', end=' ')

            # Check if service is active
            result = subprocess.run(
                ["systemctl", "is-active", service],
                capture_output = True,
                text = True
            )

            # If service is unknown or inactive, skip it
            if result.returncode != 0:
                print('service does not exist or is not active')
                continue               

            # Restart service
            result = subprocess.run(
                ["systemctl", "restart", service, "--quiet"],
                capture_output = True,
                text = True
            )

            # If service failed to restart, print error message
            if result.returncode != 0:
                print(Fore.RED + 'failed with error: ' + Style.RESET_ALL + result.stderr)
                continue

            print(Fore.GREEN + 'done' + Style.RESET_ALL)
