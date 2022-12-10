#!/bin/python

import hmac
import hashlib
import base64

jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjpudWxsfQ.Tr0VvdP6rVBGBGuI_luxGCOaz6BbhC6IxRTlKOW8UjM"

h,p,s = jwt.split(".")

def sign(str,key):
	return base64.urlsafe_b64encode(hmac.new(key, str,hashlib.sha256).digest()).decode('utf8').rstrip("=")
	
file  =  open("secret.txt",'r')
lines = file.readlines()

for line in lines:
	key = line.strip()
	if sign(h+"."+p, key) == s:		
		print(key)