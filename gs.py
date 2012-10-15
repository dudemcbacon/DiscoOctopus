#-------------------------------------------------------------------------------
# Name:        GrooveShark Downloader
# Purpose:
#
# Author:      Brandon Burnett
#
# Created:     13/10/2012
# Copyright:   (c) burnett 2012
# Licence:     DERP!PL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import logging, hmac, json, urllib2
import groovedownload

logging.basicConfig(level=logging.DEBUG)

key = "awesomeind"
secret = "74c8e2156c64197cd88c3b5f98be7cb3"
username="gentoolicious@gmail.com"

def main():
    logging.debug("Entering main")
    gs = groovedownload.GrooveDownload(key, secret)
    print "Token: %s" % gs.session
    password = raw_input("Pass: ")
    token = gs.getToken(username, password)
    print gs.api("authenticateUser", {'username':username,'token': token})


if __name__ == '__main__':
    main()
