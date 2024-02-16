# coding: utf-8

# Import libraries
import json

class Utils:
    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Return True if the string is a valid JSON
    #
    #-------------------------------------------------------------------------------------------------------------------
    def isJson(self, jsonString):
        try:
            json.loads(jsonString)
        except json.decoder.JSONDecodeError:
            return False
        except ValueError as e:
            return False
        
        return True
