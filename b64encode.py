#!/usr/bin/python
# script to encode password for gmail
# you should use md5 rather than this 
import base64
zap=raw_input("Enter password to encode: ")
smtppass=base64.b64encode(zap)
print smtppass
