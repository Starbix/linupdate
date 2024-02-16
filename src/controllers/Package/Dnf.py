# coding: utf-8

# Import libraries
import os
import subprocess

class Dnf:

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return list of available dnf packages, sorted by name
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getAvailablePackages(self):
        # Get list of packages to update sorted by name
        # e.g. dnf repoquery -q -a --qf="%{name} %{version}-%{release}.%{arch} %{repoid}" --upgrades
        result = subprocess.run(
            ["dnf", "repoquery", "--upgrades", "-q", "-a", "--qf=%{name} %{version}-%{release}.%{arch} %{repoid}"],
            capture_output = True,
            text = True
        )

        # Quit if an error occurred
        if result.returncode != 0:
            print('Error while getting available packages: ' + result.stderr)
            exit(1)

        list = []

        for line in result.stdout.split('\n'):
            if line != '':
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
                    print('Error while retrieving current version of package ' + package[0] + ': ' + result.stderr)
                    exit(1)

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
    def clearCache(self):
        # TODO
        os.system('dnf clean all')
        return
    

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Update dnf cache
    #
    #-------------------------------------------------------------------------------------------------------------------
    def updateCache(self):
        # Useless because dnf update command already updates the cache
        return
