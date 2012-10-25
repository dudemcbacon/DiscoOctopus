#-------------------------------------------------------------------------------
# Name:        GroveDownload
# Purpose:
#
# Author:      Brandon Burnett
#
# Created:     10/13/2012
# Copyright:   (c) Brandon Burnett 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import logging, hmac, json, md5, urllib2

class GrooveDownload:
    def __init__(self, key, secret):
        # Set up globals and start GrooveShark session.
        self.api_url = 'https://api.grooveshark.com/ws3.php?sig='
        self.key = key
        self.secret = secret
        self.session = ''
        self.Username = ''
        self.IsPremium = ''
        self.UserID = ''
        self.emailAddress = ''
        self.IsAnywhere = ''

        # Start GrooveShark Session
        response = self.api('startSession')
        if response['result']['success'] == True:
            self.session = response['result']['sessionID']
        else:
            raise GrooveException(json.dumps(response['errors']))

    def api(self, method, parameters={}):
        # Generic wrapper for GrooveShark API
        apiPOST = {'method': method }
        apiPOST['parameters'] = parameters
        apiPOST['header'] = {'wsKey':self.key}

        # startSession does not include a session ID
        if method != "startSession":
            if self.session != '':
                apiPOST['header']['sessionID'] = self.session
            else:
                raise GrooveException('Start a session first, bozo!')
        json_str = json.dumps(apiPOST)
        signature = self.__generateSignature(json_str)
        request = urllib2.Request(self.api_url + signature, json_str)
        return json.loads(urllib2.urlopen(request).read())


    def __generateSignature(self, json_str):
        # Generates signature hashses required for submitting requests to GS
        signature = hmac.new(self.secret,msg=json_str)
        return signature.hexdigest()

    def getToken(self, username, password):
        pass_hash = md5.new(password).hexdigest()
        return md5.new(username.lower() + pass_hash).hexdigest()

    def authenticateUser(self, username, token):
        response = self.api("authenticateUser", {'username':username,'token': token})
        if response['result']['success'] == True:
            self.Username = response['result']['Username']
            self.IsPremium = response['result']['IsPremium']
            self.UserID = response['result']['UserID']
            self.emailAddress = response['result']['emailAddress']
            self.IsAnywhere = response['result']['IsAnywhere']
            return True
        else:
            raise GrooveException(json.dumps(response['errors']))

    def getUserPlaylists(self, limit=0):
        response = self.api('getUserPlaylists', {'limit':limit})
        try:
            return response['result']['playlists']
        except:
            raise GrooveException(json.dumps(response['errors']))

    def getPlaylist(self, playlistID, limit=0):
        response = self.api('getPlaylist', {'playlistID': playlistID, 'limit':limit})
        try:
           return response['result']
        except:
           raise GrooveException(json.dumps(response['errors']))
           

class GrooveException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr("WHOA THERE! PROBLEM AHOY: %s" % self.message)