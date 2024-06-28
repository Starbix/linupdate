# coding: utf-8

# Import libraries
import os
import subprocess
import time
import re
from dateutil import parser as dateutil_parser

class Dnf:

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return list of installed apt packages, sorted by name
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getInstalledPackages(self):
        list = []

        # Get list of installed packages
        # e.g. dnf repoquery -q -a --qf="%{name} %{version}-%{release}.%{arch} %{repoid}" --upgrades
        result = subprocess.run(
            ["dnf", "repoquery", "--installed", "-a", "--qf=%{name} %{epoch}:%{version}-%{release}.%{arch}"],
            capture_output = True,
            text = True
        )

        # Quit if an error occurred
        if result.returncode != 0:
            raise Exception('could not get installed packages: ' + result.stderr)

        try:
            # Split all lines and parse them
            for line in result.stdout.split('\n'):
                if line == '':
                    continue

                # Split package name and version
                # e.g: zlib-devel 0:1.2.11-41.el9.x86_64
                package = line.split()

                name = package[0]
                version = package[1]

                # Remove epoch if it is equal to 0
                if version.startswith('0:'):
                    version = version[2:]

                list.append({
                    'name': name,
                    'version': version
                })

            # Sort the list by package name
            list.sort(key=lambda x: x['name'])

        except Exception as e:
            raise Exception('could not get installed packages: ' + str(e))

        return list


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return list of available dnf packages, sorted by name
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getAvailablePackages(self):
        list = []

        # Get list of packages to update sorted by name
        # e.g. dnf repoquery -q -a --qf="%{name} %{version}-%{release}.%{arch} %{repoid}" --upgrades
        result = subprocess.run(
            ["dnf", "repoquery", "--upgrades", "-q", "-a", "--qf=%{name} %{version}-%{release}.%{arch} %{repoid}"],
            capture_output = True,
            text = True
        )

        # Quit if an error occurred
        if result.returncode != 0:
            raise Exception('could not retrieve available packages list: ' + result.stderr)

        # Split all lines and parse them
        for line in result.stdout.split('\n'):
            if line == '':
                continue

            package = line.split(' ')

            # Retrieve current version with dnf
            # e.g. rpm -q --qf="%{version}-%{release}.%{arch}" <package>
            result = subprocess.run(
                ["rpm", "-q", "--qf=%{version}-%{release}.%{arch}", package[0]],
                capture_output = True,
                text = True
            )

            # Quit if an error occurred
            if result.returncode != 0:
                raise Exception('could not retrieve current version of package ' + package[0] + ': ' + result.stderr)

            current_version = result.stdout.strip()

            list.append({
                'name': package[0],
                'current_version': current_version,
                'available_version': package[1],
                'repository': package[2]
            })

        return list


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Clear dnf cache
    #
    #-------------------------------------------------------------------------------------------------------------------
    def clear_cache(self):
        # Check if dnf lock is present
        self.check_lock

        result = subprocess.run(
            ["dnf", "clean", "all"],
            capture_output = True,
            text = True,
        )

        # Quit if an error occurred
        if result.returncode != 0:
            raise Exception('Error while clearing dnf cache: ' + result.stderr)
    

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Update dnf cache
    #
    #-------------------------------------------------------------------------------------------------------------------
    def updateCache(self):
        # Useless because dnf update command already updates the cache
        return


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Wait for DNF lock to be released
    #
    #-------------------------------------------------------------------------------------------------------------------
    def check_lock(self):
        if os.path.isfile('/var/run/dnf.pid'):
            print(' Waiting for dnf lock...', end=' ')

            while os.path.isfile('/var/run/dnf.pid'):
                time.sleep(2)


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return dnf history Ids sorted by modification time
    #
    #-------------------------------------------------------------------------------------------------------------------
    def get_history(self, order):
        # Get history IDs
        result = subprocess.run(
            ["dnf history list | tail -n +3 | awk '{print $1}'"],
            capture_output = True,
            text = True,
            shell = True
        )

        # Quit if an error occurred
        if result.returncode != 0:
            raise Exception('could nt retrieve dnf history: ' + result.stderr)

        # Retrieve history IDs
        ids = result.stdout.splitlines()

        # If order is oldest, then sort by date in ascending order
        if order == 'oldest':
            ids.reverse()

        return ids


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Parse all dnf history IDs and return a list of events (JSON)
    #
    #-------------------------------------------------------------------------------------------------------------------
    def parse_history(self, ids: list, entries_limit: int):
        # Initialize a limit counter which will be incremented until it reaches the entries_limit
        limit_counter = 0

        # Initialize a list of events
        events = []

        # Parse each ids
        for id in ids:
            installed_packages_json = []
            installed_dependencies_json = []
            upgraded_packages_json = []
            removed_packages_json = []
            downgraded_packages_json = []
            reinstalled_packages_json = []

            # Quit if the limit of entries to send has been reached
            if limit_counter > entries_limit:
                break

            # Retrieve informations from dnf history
            # Force the locale to en_US.UTF-8 to avoid parsing issues
            result = subprocess.run(
                ["dnf", "history", "info", id],
                capture_output = True,
                text = True,
                env = {'LC_ALL': 'en_US.UTF-8'}
            )

            # Quit if an error occurred
            if result.returncode != 0:
                raise Exception('could not retrieve dnf history for id ' + id + ': ' + result.stderr)

            # Retrieve event
            event = result.stdout

            # Remove '**' is present in the event string
            event = event.replace('**', '')
            
            # Skip if cannot retrieve event date and time
            if not re.search(r'^Begin time(.+)', event, re.MULTILINE):
                raise Exception('error parsing dnf event id #' + id + ': could not retrieve event date and time')

            # Skip if cannot retrieve command line
            if not re.search(r'^Command Line(.+)', event, re.MULTILINE):
                raise Exception('error parsing dnf event id #' + id + ': could not retrieve command line')

            # Skip if cannot retrieve packages altered
            if not re.search(r'Packages Altered.*', event, re.DOTALL):
                raise Exception('error parsing dnf event id #' + id + ': could not find any packages altered in the event')

            # Retrieve event date and time
            date_time = re.search(r'^Begin time(.+)', event, re.MULTILINE).group(0).strip()
            # Remove extra spaces and 'Begin time : ' string
            date_time = str(date_time.replace('  ', '').replace('Begin time : ', ''))

            # Retrieve command line
            command = re.search(r'^Command Line(.+)', event, re.MULTILINE).group(0).strip()
            command = str(command.replace('  ', '').replace('Command Line :', '')).strip()

            # Retrieve packages altered
            packages_altered = re.search(r'Packages Altered.*', event, re.DOTALL).group(0).strip()
            packages_altered = re.sub(r' +', ' ', packages_altered)

            # Parsing and formatting

            # Convert date to %Y-%m-%d format
            date_time_parsed = dateutil_parser.parse(date_time)
            date = date_time_parsed.strftime('%Y-%m-%d')
            time = date_time_parsed.strftime('%H:%M:%S')

            # Skip if there is no lines containing 'Install', 'Dep-Install', 'Upgraded', 'Upgrade', 'Obsoleting', 'Erase', 'Removed', 'Downgrade', 'Reinstall'
            # Note: on CentOS7, it was 'Update' and 'Updated' instead of 'Upgrade' and 'Upgraded'
            if not re.search(r'^ +(Install|Dep-Install|Upgraded|Upgrade|Obsoleting|Erase|Removed|Downgrade|Reinstall) .*', packages_altered, re.MULTILINE):
                raise Exception('error parsing dnf event id #' + id + ': could not find any operation lines in the event')

            # For each lines of packages_altered
            for line in packages_altered.split('\n'):
                package_and_version = ''
                package_name = ''
                package_version = ''
                repository = ''
                operation= ''

                # If line starts with Install
                if re.search(r'^ +Install .*', line):
                    package_and_version = re.search(r'^ +Install (.+)', line).group(0).strip().replace('Install ', '')
                    operation = 'install'

                # If line starts with Dep-Install
                elif re.search(r'^ +Dep-Install .*', line):
                    package_and_version = re.search(r'^ +Dep-Install (.+)', line).group(0).strip().replace('Dep-Install ', '')
                    operation = 'dep-install'

                # If line starts with Upgrade
                elif re.search(r'^ +Upgrade .*', line):
                    package_and_version = re.search(r'^ +Upgrade (.+)', line).group(0).strip().replace('Upgrade ', '')
                    operation = 'upgrade'

                # If line starts with Update
                # elif re.search(r'^ +Update .*', line):
                #     package_and_version = re.search(r'^ +Update (.+)', line).group(0).strip().replace('Update ', '')

                # If line starts with Obsoleting
                elif re.search(r'^ +Obsoleting .*', line):
                    package_and_version = re.search(r'^ +Obsoleting (.+)', line).group(0).strip().replace('Obsoleting ', '')
                    operation = 'obsoleting'

                # If line starts with Erase
                # elif re.search(r'^ +Erase .*', line):
                #     package_and_version = re.search(r'^ +Erase (.+)', line).group(0).strip().replace('Erase ', '')
                #     operation = 'erase'

                # If line starts with Removed
                elif re.search(r'^ +Removed .*', line):
                    package_and_version = re.search(r'^ +Removed (.+)', line).group(0).strip().replace('Removed ', '')
                    operation = 'remove'

                # If line starts with Downgrade
                elif re.search(r'^ +Downgrade .*', line):
                    package_and_version = re.search(r'^ +Downgrade (.+)', line).group(0).strip().replace('Downgrade ', '')
                    operation = 'downgrade'

                # If line starts with Reinstall
                elif re.search(r'^ +Reinstall .*', line):
                    package_and_version = re.search(r'^ +Reinstall (.+)', line).group(0).strip().replace('Reinstall ', '')
                    operation = 'reinstall'

                else:
                    continue

                # Remove extra spaces
                package_and_version = package_and_version.strip()

                # Skip if package_and_version is empty
                if package_and_version == '':
                    raise Exception('error parsing dnf event id #' + id + ': cannot retrieve package and version for line:\n' + line)

                # Skip if string starts with '@'
                if package_and_version.startswith('@'):
                    continue

                # Retrieve package name, version and repository from package_and_version
                package_name = re.sub(r'-[0-9].*', '', package_and_version).strip()
                package_version_and_repository = re.sub(r'^-', '', package_and_version.replace(package_name, '')).strip()

                # Retrieve repository and package version
                package_version = package_version_and_repository.split()[0].strip()
                repository = package_version_and_repository.split()[1].strip()

                # Raise exception if package_name or package_version is empty
                if package_name == '':
                    raise Exception('error parsing dnf event id #' + id + ': cannot retrieve package name for line:\n' + line)

                if package_version == '':
                    raise Exception('error parsing dnf event id #' + id + ': cannot retrieve package version for line:\n' + line)
                
                # Add package to the corresponding list
                if operation == 'install':
                    installed_packages_json.append({
                        'name': package_name,
                        'version': package_version,
                        'repo': repository
                    })

                if operation == 'dep-install':
                    installed_dependencies_json.append({
                        'name': package_name,
                        'version': package_version,
                        'repo': repository
                    })

                if operation == 'upgrade':
                    upgraded_packages_json.append({
                        'name': package_name,
                        'version': package_version,
                        'repo': repository
                    })

                if operation == 'remove':
                    removed_packages_json.append({
                        'name': package_name,
                        'version': package_version,
                    })

                if operation == 'downgrade':
                    downgraded_packages_json.append({
                        'name': package_name,
                        'version': package_version,
                    })

                if operation == 'reinstall':
                    reinstalled_packages_json.append({
                        'name': package_name,
                        'version': package_version,
                        'repo': repository
                    })

                # TODO
                # if operation == 'obsoleting':

            # Create the event JSON object
            event = {
                'date_start': date,
                'time_start': time,
                'date_end': '',
                'time_end': '',
                'command': command,
            }

            if installed_packages_json != '':
                event['installed'] = installed_packages_json

            if installed_dependencies_json != '':
                event['dep_installed'] = installed_dependencies_json

            if upgraded_packages_json != '':
                event['upgraded'] = upgraded_packages_json

            if removed_packages_json != '':
                event['removed'] = removed_packages_json

            if downgraded_packages_json != '':
                event['downgraded'] = downgraded_packages_json

            if reinstalled_packages_json != '':
                event['reinstalled'] = reinstalled_packages_json

            # Add the event to the list of events
            events.append(event)

            limit_counter += 1

        return events
