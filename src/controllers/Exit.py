# coding: utf-8

# Import constants
from constant import *

# Import classes
from src.controllers.App.Config import Config
from src.controllers.Mail import Mail

class Exit:
    def __init__(self):
        self.my_config = Config()
        self.my_mail = Mail()

    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Clean and exit
    #
    #-------------------------------------------------------------------------------------------------------------------
    def cleanExit(self, exit_code = 0, logfile: str = None):
        # TODO
        # Clean files

        # Clear apt / yum cache
        # xxxx.clear_cache()


        # Send email

        # Get mail settings
        mail_enabled = self.my_config.getMailEnabled()
        mail_recipient = self.my_config.getMailRecipient()

        # TODO
        # Check if mail is enabled and recipient is set
        # if (mail_enabled and mail_recipient):
        #     # Define mail subject depending on exit code
        #     if exit_code == 0:
        #         subject = '[ OK ] Packages update successful'

        #     if exit_code == 1:
        #         subject = '[ ERROR ] Packages update failed'

        #     print(' Sending update mail report:', end=' ')

        #     try:
        #         self.my_mail.send(subject, 'Linupdate has finished updating packages', mail_recipient, logfile)
        #         print('done')
        #     except Exception as e:
        #         print('error: ' + str(e))

        exit(exit_code)
