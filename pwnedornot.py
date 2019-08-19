#!/usr/bin/env python3

import os
import re
import sys
import json
import time
import argparse
import requests

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

version = '1.2.8'

key = ''
useragent = ''
start = ''

def banner():
	if sys.platform == 'win32':
		os.system('cls')
	else:
		os.system('clear')

	banner = r'''
                                  ______       _   __      __
    ____ _      ______  ___  ____/ / __ \_____/ | / /___  / /_
   / __ \ | /| / / __ \/ _ \/ __  / / / / ___/  |/ / __ \/ __/
  / /_/ / |/ |/ / / / /  __/ /_/ / /_/ / /  / /|  / /_/ / /_
 / .___/|__/|__/_/ /_/\___/\__,_/\____/_/  /_/ |_/\____/\__/
/_/
	'''
	print(G + banner + W)
	print(G + '[>]' + C + ' Created by : ' + W + 'thewhiteh4t')
	print(G + '[>]' + C + ' Version    : ' + W + version + '\n')

def api_key():
	global key, useragent
	try:
		with open('key.txt', 'r') as keyfile:
			key = keyfile.readline()
			key = key.strip()
			print(G + '[+]' + C + ' API Key Found...' + W + '\n')
			useragent = {'User-Agent': 'pwnedOrNot', 'hibp-api-key': key}
	except FileNotFoundError:
		print(R + '[-]' + C + ' API Key Not Found...' + W + '\n')
		print(G + '[+]' + C + ' Get your API Key : ' + W + 'https://haveibeenpwned.com/API/Key' + '\n')
		enter_key = input(G + '[+]' + C + ' Enter your API Key : ' + W)
		enter_key = enter_key.strip()
		with open('key.txt', 'w') as keyfile:
			keyfile.write(enter_key)
		key_path = os.getcwd() + '/key.txt'
		print(G + '[+]' + C + ' Saved API Key in : ' + W + key_path + '\n')

def main():
	global addr, start
	start = time.time()

	if list_domain is True:
		domains_list()
	elif check_domain:
		domain_check()
	elif addr is not None and domain is not None:
		filtered_check()
	elif addr is not None and domain is None:
		check()
	elif file is not None and domain is None:
		print (G + '[+]' + C + ' Reading Emails Addresses from ' + W + '{}'.format(file) + '\n')
		with open(file) as dict:
			for line in dict:
				line = line.strip()
				addr = line
				if addr != '':
					check()
					time.sleep(1.6)
	elif file != None and domain != None:
		print(G + '[+]' + C + ' Reading Emails Addresses from ' + W + '{}'.format(file) + '\n')
		print(G + '[+]' + C + ' Domain : ' + W + domain)
		with open(file) as dict:
			for line in dict:
				line = line.strip()
				addr = line
				if addr != '':
					filtered_check()
					time.sleep(1.6)
	else:
		print('\n' + R + '[-]' + C + ' Error : Atleast 1 Argument is Required, Try : python3 pwnedornot.py -h' + W)
		exit()

def check():
	print(G + '[+]' + C + ' Checking Breach status for ' + W + '{}'.format(addr), end = '')
	rqst = requests.get('https://haveibeenpwned.com/api/v3/breachedaccount/{}'.format(addr), headers=useragent, params={'truncateResponse': 'false'}, timeout=10)
	sc = rqst.status_code
	
	if sc == 200:
		print(G + ' [ pwned ]' + W)
		json_out = rqst.content.decode('utf-8', 'ignore')
		simple_out = json.loads(json_out)
		for item in simple_out:
			print( '\n'
				+ G + '[+]' + C + ' Breach      : ' + W + str(item['Title']) + '\n'
				+ G + '[+]' + C + ' Domain      : ' + W + str(item['Domain']) + '\n'
				+ G + '[+]' + C + ' Date        : ' + W + str(item['BreachDate']) + '\n'
				+ G + '[+]' + C + ' Fabricated  : ' + W + str(item['IsFabricated']) + '\n'
				+ G + '[+]' + C + ' Verified    : ' + W + str(item['IsVerified']) + '\n'
				+ G + '[+]' + C + ' Retired     : ' + W + str(item['IsRetired']) + '\n'
				+ G + '[+]' + C + ' Spam        : ' + W + str(item['IsSpamList']))
		if nodumps is not True:
			dump()
	elif sc == 404:
		print(R + ' [ Not Breached ]' + W)
		if nodumps is not True:
			dump()
	elif sc == 503:
		print('\n')
		print(R + '[-]' + C + ' Error 503 : ' + W + 'Request Blocked by Cloudflare DDoS Protection')
	elif sc == 403:
		print('\n')
		print(R + '[-]' + C + ' Error 403 : ' + W + 'Request Blocked by haveibeenpwned API')
		print('\n-------------------------------------------------')
		print('Email This Complete Response at troy@troyhunt.com')
		print('-------------------------------------------------\n')
		print(rqst.text)
	else:
		print('\n')
		print(R + '[-]' + C + ' An Unknown Error Occurred')
		print(rqst.text)

def filtered_check():
	print('\n' + G + '[+]' + C + ' Checking Breach status for ' + W + '{}'.format(addr), end='')
	rqst = requests.get('https://haveibeenpwned.com/api/v3/breachedaccount/{}?domain={}'.format(addr, domain), headers=useragent, params={'truncateResponse': 'false'}, verify=True, timeout=10)
	sc = rqst.status_code

	if sc == 200:
		print(G + ' [ pwned ]' + W)
		json_out = rqst.content.decode('utf-8', 'ignore')
		simple_out = json.loads(json_out)

		for item in simple_out:
			print( '\n'
				+ G + '[+]' + C + ' Breach      : ' + W + str(item['Title']) + '\n'
				+ G + '[+]' + C + ' Domain      : ' + W + str(item['Domain']) + '\n'
				+ G + '[+]' + C + ' Date        : ' + W + str(item['BreachDate']) + '\n'
				+ G + '[+]' + C + ' Fabricated  : ' + W + str(item['IsFabricated']) + '\n'
				+ G + '[+]' + C + ' Verified    : ' + W + str(item['IsVerified']) + '\n'
				+ G + '[+]' + C + ' Retired     : ' + W + str(item['IsRetired']) + '\n'
				+ G + '[+]' + C + ' Spam        : ' + W + str(item['IsSpamList']))
		if nodumps is not True:
			dump()
	elif sc == 404:
		print(R + ' [ Not Breached ]' + W)
		if nodumps is not True:
			dump()
	elif sc == 503:
		print('\n')
		print(R + '[-]' + C + ' Error 503 : ' + W + 'Request Blocked by Cloudflare DDoS Protection')
	elif sc == 403:
		print('\n')
		print(R + '[-]' + C + ' Error 403 : ' + W + 'Request Blocked by Cloudflare')
	else:
		print('\n')
		print(R + '[-]' + C + ' An Unknown Error Occurred')
		print(rqst.text)

def dump():
	dumplist = []
	print('\n' + G + '[+]' + C + ' Looking for Dumps...' + W, end = '')
	rqst = requests.get('https://haveibeenpwned.com/api/v3/pasteaccount/{}'.format(addr), headers=useragent, timeout=10)
	sc = rqst.status_code

	if sc != 200:
		print(R + ' [ No Dumps Found ]' + W)
	else:
		print(G + ' [ Dumps Found ]' + W + '\n')
		json_out = rqst.content.decode('utf-8', 'ignore')
		simple_out = json.loads(json_out)

		for item in simple_out:
			if (item['Source']) == 'Pastebin':
				link = item['Id']
				try:
					url = 'https://www.pastebin.com/raw/{}'.format(link)
					page = requests.get(url, timeout=10)
					sc = page.status_code
					if sc == 200:
						dumplist.append(url)
						print(G + '[+]' + C + ' Dumps Found : ' + W + str(len(dumplist)), end='\r')
					if len(dumplist) == 0:
							print(R + '[-]' + C + ' Dumps are not Accessible...' + W)
				except requests.exceptions.ConnectionError:
					pass
			elif (item['Source']) == 'AdHocUrl':
				url = item['Id']
				try:
					page = requests.get(url, timeout=10)
					sc = page.status_code
					if sc == 200:
						dumplist.append(url)
						print(G + '[+]' + C + ' Dumps Found : ' + W + str(len(dumplist)), end='\r')
					if len(dumplist) == 0:
							print(R + '[-]' + C + ' Dumps are not Accessible...' + W)
				except requests.exceptions.ConnectionError:
					pass

	if len(dumplist) != 0:
		print('\n\n' + G + '[+]' + C + ' Passwords:' + W + '\n')
		for entry in dumplist:
			time.sleep(1.1)
			try:
				page = requests.get(entry, timeout=10)
				dict = page.content.decode('utf-8', 'ignore')
				passwd = re.search('{}:(\w+)'.format(addr), dict)
				if passwd:
					print(G + '[+] ' + W + passwd.group(1))
				elif not passwd:
					for line in dict.splitlines():
						passwd = re.search('(.*{}.*)'.format(addr), line)
						if passwd:
							print(G + '[+] ' + W + passwd.group(0))
			except requests.exceptions.ConnectionError:
				pass

def domains_list():
	domains = []
	print(G + '[+]' + C + ' Fetching List of Breached Domains...' + W + '\n')
	rqst = requests.get('https://haveibeenpwned.com/api/v3/breaches', headers=useragent, timeout=10)
	sc = rqst.status_code
	
	if sc == 200:
		json_out = rqst.content.decode('utf-8', 'ignore')
		simple_out = json.loads(json_out)
		for item in simple_out:
			domain_name = item['Domain']
			if len(domain_name) != 0:
				print (G + '[+] ' + W + str(domain_name))
				domains.append(domain_name)
		print('\n' + G + '[+]' + C + ' Total : ' + W + str(len(domains)))
	elif sc == 503:
		print(R + '[-]' + C + ' Error 503 : ' + W + 'Request Blocked by Cloudflare DDoS Protection')
	elif sc == 403:
		print(R + '[-]' + C + ' Error 403 : ' + W + 'Request Blocked by Cloudflare')
	else:
		print(R + '[-]' + C + ' An Unknown Error Occurred')
		print(rqst.text)

def domain_check():
	print(G + '[+]' + C + ' Domain Name : ' + W + check_domain, end = '')
	rqst = requests.get('https://haveibeenpwned.com/api/v3/breaches?domain={}'.format(check_domain), headers=useragent, timeout=10)
	sc = rqst.status_code
	if sc == 200:
		json_out = rqst.content.decode('utf-8', 'ignore')
		simple_out = json.loads(json_out)
		if len(simple_out) != 0:
			print(G + ' [ pwned ]' + W)
			for item in simple_out:
				print( '\n'
					+ G + '[+]' + C + ' Breach      : ' + W + str(item['Title']) + '\n'
					+ G + '[+]' + C + ' Domain      : ' + W + str(item['Domain']) + '\n'
					+ G + '[+]' + C + ' Date        : ' + W + str(item['BreachDate']) + '\n'
					+ G + '[+]' + C + ' Pwn Count   : ' + W + str(item['PwnCount']) + '\n'
 					+ G + '[+]' + C + ' Fabricated  : ' + W + str(item['IsFabricated']) + '\n'
					+ G + '[+]' + C + ' Verified    : ' + W + str(item['IsVerified']) + '\n'
					+ G + '[+]' + C + ' Retired     : ' + W + str(item['IsRetired']) + '\n'
					+ G + '[+]' + C + ' Spam        : ' + W + str(item['IsSpamList']) + '\n'
					+ G + '[+]' + C + ' Data Types  : ' + W + str(item['DataClasses']))
		else:
			print(R + ' [ Not Breached ]' + W)
	elif sc == 503:
		print('\n')
		print(R + '[-]' + C + ' Error 503 : ' + W + 'Request Blocked by Cloudflare DDoS Protection')
	elif sc == 403:
		print('\n')
		print(R + '[-]' + C + ' Error 403 : ' + W + 'Request Blocked by Cloudflare')
	else:
		print('\n')
		print(R + '[-]' + C + ' An Unknown Error Occurred')
		print(rqst.text)

def quit():
	global start
	print('\n' + G + '[+]' + C + ' Completed in ' + W + str(time.time()-start) + C + ' seconds.' + W)
	exit()

try:
	banner()

	ap = argparse.ArgumentParser()
	ap.add_argument('-e', '--email', required=False,
	help='Email Address You Want to Test')
	ap.add_argument('-f', '--file', required=False,
	help='Load a File with Multiple Email Addresses')
	ap.add_argument('-d', '--domain', required=False,
	help='Filter Results by Domain Name')
	ap.add_argument('-n', '--nodumps', required=False, action='store_true',
	help='Only Check Breach Info and Skip Password Dumps')
	ap.add_argument('-l', '--list', required=False, action='store_true',
	help='Get List of all pwned Domains')
	ap.add_argument('-c', '--check', required=False,
	help='Check if your Domain is pwned')
	arg = ap.parse_args()
	addr = arg.email
	file = arg.file
	domain = arg.domain
	nodumps = arg.nodumps
	list_domain = arg.list
	check_domain = arg.check

	api_key()
	main()
	quit()
except KeyboardInterrupt:
	print('\n' + R + '[!]' + C + ' Keyboard Interrupt.' + W)
	exit()
