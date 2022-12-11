#!/usr/bin/env python3

from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('-e', '--email', required=False,
help='Email Address You Want to Test')
ap.add_argument('-f', '--file', required=False,
help='Load a File with Multiple Email Addresses')
ap.add_argument('-fp', '--filepawned', required=False,
help='Output file for pawned mail addresses')
ap.add_argument('-d', '--domain', required=False,
help='Filter Results by Domain Name')
ap.add_argument('-b', '--breach', required=False,
help='Get Info about breach')
ap.add_argument('-n', '--nodumps', required=False, action='store_true',
help='Only Check Breach Info and Skip Password Dumps')
ap.add_argument('-l', '--list', required=False, action='store_true',
help='Get List of all pwned Domains')
ap.add_argument('-c', '--check', required=False,
help='Check if your Domain is pwned')
arg = ap.parse_args()
addr = arg.email
file = arg.file
filepawned = arg.filepawned
domain = arg.domain
breach_name = arg.breach
nodumps = arg.nodumps
list_domain = arg.list
check_domain = arg.check

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white
Y = '\033[33m' # yellow

version = '1.3.0.1'

key = ''
useragent = ''
start = ''
idle_time = 1.6

import requests
from os import system
from sys import exit
from os import remove
from os import getenv
from os import environ
from os import path
from re import search
from time import time, sleep
from json import loads, dumps
from html2text import html2text

system("color")

if "HOME" in environ:
    home = getenv('HOME')
if "USERPROFILE" in environ:
    home = getenv('USERPROFILE')
conf_path = path.join(home, '.config', 'pwnedornot', 'config.json')

response_codes = {
	200: "OK",
	400: "Bad request — the account does not comply with an acceptable format (i.e. it's an empty string)",
	401: "Unauthorised — either no API key was provided or it wasn't valid",
	403: "Forbidden — no user agent has been specified in the request",
	404: "Not Pwned",
	429: "Too many requests — the rate limit has been exceeded",
	503: "Service unavailable — usually returned by Cloudflare if the underlying service is not available",
}

def banner():
	banner = r'''
                                  ______       _   __      __
    ____ _      ______  ___  ____/ / __ \_____/ | / /___  / /_
   / __ \ | /| / / __ \/ _ \/ __  / / / / ___/  |/ / __ \/ __/
  / /_/ / |/ |/ / / / /  __/ /_/ / /_/ / /  / /|  / /_/ / /_
 / .___/|__/|__/_/ /_/\___/\__,_/\____/_/  /_/ |_/\____/\__/
/_/
'''
	print(G + banner + W)
	print(f'{G}[>]{C} Created by : {W}thewhiteh4t')
	print(f'{G}[>]{C} Version    : {W}{version}\n')

def read_config():
	global key, useragent, idle_time

	with open(conf_path, 'r') as config:
		json_cnf = loads(config.read())
		key = json_cnf['api_key']
		if len(key) > 0:
			print(f'{G}[+] {C}API Key Found...{W}\n')
			useragent = {'User-Agent': 'pwnedOrNot', 'hibp-api-key': key}
		else:
			print(f'{R}[-] {C}API Key Not Found...{W}\n')
			print(f'{G}[+] {C}Get your API Key : {W}https://haveibeenpwned.com/API/Key \n')
			enter_key = input(f'{G}[+]' + C + ' Enter your API Key : ' + W)
			enter_key = enter_key.strip()
			
			with open(conf_path, 'w') as keyfile:
				key_dict = {'api_key': enter_key}
				json_data = dumps(key_dict)
				keyfile.write(json_data)
			print(f'{G}[+] {C}Saved API Key in : {W}{conf_path}\n')

def main():
	global addr, start
	start = time()

	banner()
	read_config()

	if filepawned is not None and path.exists(filepawned):
		remove(filepawned)

	if list_domain is True:
		domains_list()
	elif check_domain:
		domain_check()
	elif breach_name:
		breach_info()
	elif addr is not None and domain is not None:
		filtered_check()
	elif addr is not None and domain is None:
		check()
	elif file is not None and domain is None:
		print(f'{G}[+] {C}Reading Emails Addresses from {W}{file}\n')
		with open(file) as dict:
			for line in dict:
				line = line.strip()
				addr = line
				if addr != '':
					check()
					sleep(idle_time)
	elif file != None and domain != None:
		print(f'{G}[+] {C}Reading Emails Addresses from {W}{file}\n')
		print(f'{G}[+] {C}Domain : {W}{domain}')
		with open(file) as dict:
			for line in dict:
				line = line.strip()
				addr = line
				if addr != '':
					filtered_check()
					sleep(idle_time)
	else:
		print(f'{R}[-] {C}Error : {W}Atleast 1 Argument is Required, Try : {G}python3 pwnedornot.py -h{W}')
		exit()

def check():
	print(f'{G}[+] {C}Checking Breach status for {W}{addr}', end = '')
	rqst = requests.get(
		f'https://haveibeenpwned.com/api/v3/breachedaccount/{addr}',
		headers=useragent,
		params={'truncateResponse': 'false'},
		timeout=10
	)
	sc = rqst.status_code
	for code, desc in response_codes.items():
		if sc == code:
			if sc == 200:
				print(f' {G}[ pwned ]{W}')
				json_out = rqst.content.decode('utf-8', 'ignore')
				simple_out = loads(json_out)
				print(f'\n{G}[+] {C}Total Breaches : {W}{len(simple_out)}')
				for item in simple_out:
					print(f'\n' \
						f'{G}[+] {C}Breach      : {W}{str(item["Title"])} \n' \
						f'{G}[+] {C}Domain      : {W}{str(item["Domain"])} \n' \
						f'{G}[+] {C}Date        : {W}{str(item["BreachDate"])} \n' \
						f'{G}[+] {C}BreachedInfo: {W}{str(item["DataClasses"])} \n' \
						f'{G}[+] {C}Fabricated  : {W}{str(item["IsFabricated"])} \n' \
						f'{G}[+] {C}Verified    : {W}{str(item["IsVerified"])} \n' \
						f'{G}[+] {C}Retired     : {W}{str(item["IsRetired"])} \n' \
						f'{G}[+] {C}Spam        : {W}{str(item["IsSpamList"])}'
					)
				print(f'-----\n')
				if nodumps != True:
					dump()
				if filepawned is not None:
					with open(filepawned, 'a') as fileout:
						fileout.write(''+addr+'\n')	
			elif sc == 404:
				print(f' {R}[ not pwned ]{W}')
				if nodumps != True:
					dump()
			elif sc == 429:
				retry_sleep = float(rqst.headers['Retry-After'])
				print(f' {Y}[ retry in {retry_sleep}s]{W}')
				sleep(retry_sleep)
				check()
			else:
				print(f'\n\n{R}[-] {C}Status {code} : {W}{desc}')

def filtered_check():
	print(f'\n{G}[+] {C}Checking Breach status for {W}{addr}', end='')
	rqst = requests.get(
		f'https://haveibeenpwned.com/api/v3/breachedaccount/{addr}?domain={domain}',
		headers=useragent,
		params={'truncateResponse': 'false'},
		verify=True,
		timeout=10
	)
	sc = rqst.status_code

	for code, desc in response_codes.items():
		if sc == code:
			if sc == 200:
				print(f' {G}[ pwned ]{W}')
				json_out = rqst.content.decode('utf-8', 'ignore')
				simple_out = loads(json_out)

				for item in simple_out:
					print(f'\n' \
						f'{G}[+] {C}Breach      : {W}{str(item["Title"])} \n' \
						f'{G}[+] {C}Domain      : {W}{str(item["Domain"])} \n' \
						f'{G}[+] {C}Date        : {W}{str(item["BreachDate"])} \n' \
						f'{G}[+] {C}BreachedInfo: {W}{str(item["DataClasses"])} \n' \
						f'{G}[+] {C}Fabricated  : {W}{str(item["IsFabricated"])} \n' \
						f'{G}[+] {C}Verified    : {W}{str(item["IsVerified"])} \n' \
						f'{G}[+] {C}Retired     : {W}{str(item["IsRetired"])} \n' \
						f'{G}[+] {C}Spam        : {W}{str(item["IsSpamList"])}'
					)
				if nodumps is not True:
					dump()
			elif sc == 404:
				print(f' {R}[ not pwned ]{W}')
				if nodumps is not True:
					dump()
			elif sc == 429:
				retry_sleep = float(rqst.headers['Retry-After'])
				print(f' {Y}[ retry in {retry_sleep}s]{W}')
				sleep(retry_sleep)
				check()					
			else:
				print(f'\n{R}[-] {C}Status {code} : {W}{desc}')

def dump():
	dumplist = []
	print(f'\n{G}[+] {C}Looking for Dumps...{W}', end = '')
	rqst = requests.get(
		f'https://haveibeenpwned.com/api/v3/pasteaccount/{addr}',
		headers=useragent,
		timeout=10
	)
	sc = rqst.status_code

	if sc == 429:
		retry_sleep = float(rqst.headers['Retry-After'])
		print(f' {Y}[ retry in {retry_sleep}s]{W}')
		sleep(retry_sleep)
		dump()
	elif sc != 200:
		print(f' {R}[ No Dumps Found ]{W}')
	else:
		print(f' {G}[ Dumps Found ]{W}\n')
		json_out = rqst.content.decode('utf-8', 'ignore')
		simple_out = loads(json_out)

		for item in simple_out:
			if (item['Source']) == 'Pastebin':
				link = item['Id']
				try:
					url = 'https://www.pastebin.com/raw/{}'.format(link)
					page = requests.get(url, timeout=10)
					sc = page.status_code
					if sc == 200:
						dumplist.append(url)
						print(f'{G}[+] {C}Dumps Found : {W}{len(dumplist)}', end='\r')
					if len(dumplist) == 0:
							print(f'{R}[-] {C}Dumps are not Accessible...{W}')
				except requests.exceptions.ConnectionError:
					pass
			elif (item['Source']) == 'AdHocUrl':
				url = item['Id']
				try:
					page = requests.get(url, timeout=10)
					sc = page.status_code
					if sc == 200:
						dumplist.append(url)
						print(f'{G}[+] {C}Dumps Found : {W}{len(dumplist)}', end='\r')
					if len(dumplist) == 0:
							print(f'{R}[-] {C}Dumps are not Accessible...{W}')
				except Exception:
					pass

	if len(dumplist) != 0:
		print(f'\n\n{G}[+] {C}Passwords : {W}\n')
		for entry in dumplist:
			sleep(1.1)
			try:
				page = requests.get(entry, timeout=10)
				dict = page.content.decode('utf-8', 'ignore')
				passwd = search('{}:(\w+)'.format(addr), dict)
				if passwd:
					print(f'{G}[+] {W}{passwd.group(1)}')
				elif not passwd:
					for line in dict.splitlines():
						passwd = search('(.*{}.*)'.format(addr), line)
						if passwd:
							print(f'{G}[+] {W}{passwd.group(0)}')
			except requests.exceptions.ConnectionError:
				pass

def breach_info():
	print(f'{G}[+] {C}Breach Name : {W}{breach_name}', end = '')
	rqst = requests.get(
		f'https://haveibeenpwned.com/api/v3/breach/{breach_name}',
		headers=useragent,
		timeout=10
	)
	sc = rqst.status_code

	for code, desc in response_codes.items():
		if sc == code:
			if sc == 200:
				json_out = rqst.content.decode('utf-8', 'ignore')
				simple_out = loads(json_out)
				if len(simple_out) != 0:
					print(f' {G}[ pwned ]{W}')
					print(f'\n' \
					f'{G}[+] {C}Breach      : {W}{str(simple_out["Title"])}\n' \
					f'{G}[+] {C}Domain      : {W}{str(simple_out["Domain"])}\n' \
					f'{G}[+] {C}Date        : {W}{str(simple_out["BreachDate"])}\n' \
					f'{G}[+] {C}Pwn Count   : {W}{str(simple_out["PwnCount"])}\n' \
					f'{G}[+] {C}Fabricated  : {W}{str(simple_out["IsFabricated"])}\n' \
					f'{G}[+] {C}Verified    : {W}{str(simple_out["IsVerified"])}\n' \
					f'{G}[+] {C}Retired     : {W}{str(simple_out["IsRetired"])}\n' \
					f'{G}[+] {C}Spam        : {W}{str(simple_out["IsSpamList"])}\n' \
					f'{G}[+] {C}Data Types  : {W}{str(simple_out["DataClasses"])}'
					)
				else:
					print(f' {R}[ Not Breached ]{W}')
			elif sc == 429:
				retry_sleep = float(rqst.headers['Retry-After'])
				print(f' {Y}[ retry in {retry_sleep}s]{W}')
				sleep(retry_sleep)
				breach_info()
			elif sc == 404:
				print(f' {R}[ Not Breached ]{W}')
			else:
				print(f'\n{R}[-] {C}Status {code} : {W}{desc}')

def domains_list():
	domains = []
	print(f'{G}[+] {C}Fetching List of Breached Domains...{W}\n')
	rqst = requests.get(
		'https://haveibeenpwned.com/api/v3/breaches',
		headers=useragent,
		timeout=10
	)
	sc = rqst.status_code
	
	for code, desc in response_codes.items():
		if sc == code:
			if sc == 200:
				json_out = rqst.content.decode('utf-8', 'ignore')
				simple_out = loads(json_out)
				for item in simple_out:
					domain_name = item['Domain']
					if len(domain_name) != 0:
						print(G + '[+] ' + W + str(domain_name))
						domains.append(domain_name)
				print(f'\n{G}[+] {C}Total : {W}{len(domains)}')
			else:
				print(f'\n{R}[-] {C}Status {code} : {W}{desc}')

def domain_check():
	print(f'{G}[+] {C}Domain Name : {W}{check_domain}', end = '')
	rqst = requests.get(
		f'https://haveibeenpwned.com/api/v3/breaches?domain={check_domain}',
		headers=useragent,
		timeout=10
	)
	sc = rqst.status_code

	for code, desc in response_codes.items():
		if sc == code:
			if sc == 200:
				json_out = rqst.content.decode('utf-8', 'ignore')
				simple_out = loads(json_out)

				if len(simple_out) != 0:
					print(f' {G}[ pwned ]{W}')
					for item in simple_out:
						print(f'\n' \
							f'{G}[+] {C}Breach      : {W}{str(item["Title"])}\n' \
							f'{G}[+] {C}Domain      : {W}{str(item["Domain"])}\n' \
							f'{G}[+] {C}Date        : {W}{str(item["BreachDate"])}\n' \
							f'{G}[+] {C}Pwn Count   : {W}{str(item["PwnCount"])}\n' \
 							f'{G}[+] {C}Fabricated  : {W}{str(item["IsFabricated"])}\n' \
							f'{G}[+] {C}Verified    : {W}{str(item["IsVerified"])}\n' \
							f'{G}[+] {C}Retired     : {W}{str(item["IsRetired"])}\n' \
							f'{G}[+] {C}Spam        : {W}{str(item["IsSpamList"])}\n' \
							f'{G}[+] {C}Data Types  : {W}{str(item["DataClasses"])}' \
							f'{G}[+] {C}Description : {W}{html2text(str(item["Description"]))}'
						)
				else:
					print(f' {R}[ Not Breached ]{W}')
			elif sc == 404:
				print(f' {R}[ Not Breached ]{W}')
			else:
				print(f'\n{R}[-] {C}Status {code} : {W}{desc}')

def quit():
	print(f'\n{G}[+] {C}Completed in {W}{str(time()-start)} {C}seconds.{W}')
	exit()

try:
	if __name__ == "__main__":
		main()
		quit()
	else:
		pass
except KeyboardInterrupt:
	print(f'\n{R}[!] {C}Keyboard Interrupt.{W}')
	exit()
