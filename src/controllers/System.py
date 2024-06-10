# coding: utf-8

import os
import platform
import distro

class System:
    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return true if current user is root or sudo
    #
    #-------------------------------------------------------------------------------------------------------------------
    def isRoot(self):
        if os.geteuid() == 0:
            return True

        return False


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Check if the program is running on a supported Linux distribution
    #
    #-------------------------------------------------------------------------------------------------------------------
    def check(self):
        # Check if the program is running on Linux
        if (platform.system() != 'Linux'):
            raise Exception('This program only works on Linux')
     
        # Check if the program is running on a supported Linux distribution (will raise an exception if not supported)
        self.getOsFamily()
    

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return the OS family
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getOsFamily(self):
        if (distro.name() in ['Debian', 'Ubuntu', 'Kubuntu', 'Xubuntu', 'Linux Mint']):
            return 'Debian'
            
        if (distro.name() in ['Centos', 'CentOS Stream', 'Fedora', 'Alma Linux', 'Rocky Linux']):
            return 'Redhat'
        
        raise Exception('This program does not support your Linux distribution "' + distro.name() + '" yet.')


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return the OS name
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getOsName(self):
        return distro.name()


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return the OS version
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getOsVersion(self):
        return distro.version()


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return the kernel version
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getKernel(self):
        return platform.release()
    

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return the architecture
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getArch(self):
        return platform.machine()


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return the virtualization type
    #
    #-------------------------------------------------------------------------------------------------------------------
    def getVirtualization(self):
        # Detect virtualization type
        if os.path.isfile("/usr/sbin/virt-what"):
            virt = os.popen('/usr/sbin/virt-what').read().replace('\n', ' ')
            if not virt:
                virt = "Bare-metal"

        return virt


    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return True if a reboot is required
    #
    #-------------------------------------------------------------------------------------------------------------------
    def rebootRequired(self):
        if self.getOsFamily() == 'Debian' and os.path.isfile('/var/run/reboot-required'):
            return True
        
        # TODO: verify that it works
        if self.getOsFamily() == 'Redhat' and os.path.isfile('/usr/bin/needs-restarting'):
            if os.system('/usr/bin/needs-restarting -r') == 0:
                return True

        return False
            