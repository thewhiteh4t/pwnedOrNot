#!/usr/bin/env python

from __future__ import print_function
import os
import re
import sys
import json
import time
import argparse
import requests
import cfscrape
import subprocess

RED = "\033[31m"
GREEN = "\033[32m"
CYAN = "\033[36m"
WHITE = "\033[0m"


if sys.version_info[0] >= 3:
    raw_input = input
    unicode = str

# try:
# 	raw_input          # Python 2
# except NameError:
# 	raw_input = input  # Python 3
#
# try:
# 	unicode            # Python 2
# except NameError:
# 	unicode = str      # Python 3

version = "1.1.0"


def print_info(banner, info=""):
    out = GREEN + "[+]" + CYAN + banner + WHITE + info
    print(out)


def print_breach(item):
    print()
    print_info(" Breach      : ", unicode(item["Title"]))
    print_info(" Domain      : ", unicode(item["Domain"]))
    print_info(" Date        : ", unicode(item["BreachDate"]))
    print_info(" Fabricated  : ", unicode(item["IsFabricated"]))
    print_info(" Verified    : ", unicode(item["IsVerified"]))
    print_info(" Retired     : ", unicode(item["IsRetired"]))
    print_info(" Spam        : ", unicode(item["IsSpamList"]))


def update():
    print(GREEN + "[+]" + CYAN + " Checking for updates..." + WHITE + "\n")
    updated_version = requests.get(
        "https://raw.githubusercontent.com/thewhiteh4t/pwnedOrNot/master/version.txt"
    )
    updated_version = updated_version.text.split(" ")[1]
    updated_version = updated_version.strip()
    if updated_version != version:
        print(
            GREEN
            + "[!]"
            + CYAN
            + " A New Version is Available : "
            + WHITE
            + updated_version
        )
        ans = raw_input(GREEN + "[!]" + CYAN + " Update ? [y/n] : " + WHITE)
        if "y" in ans.lower():
            print_info(" Updating...")
            subprocess.check_output(["git", "reset", "--hard", "origin/master"])
            subprocess.check_output(["git", "pull"])
            print(GREEN + "[+]" + CYAN + " Script Updated...Please Execute Again...")
            exit()
    else:
        print(GREEN + "[+]" + CYAN + " Script is up-to-date..." + "\n")


# commandline arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--email", required=False, help="Email account you want to test")
ap.add_argument(
    "-f", "--file", required=False, help="Load a file with multiple email accounts"
)

arg = ap.parse_args()

addr = arg.email
file = arg.file


def banner():
    if sys.platform == "win32":
        os.system("cls")  # Windows
    else:
        os.system("clear")  # UNIX

    banner = r"""
                           ______      _  __     __
   ___ _    _____  ___ ___/ / __ \____/ |/ /__  / /_
  / _ \ |/|/ / _ \/ -_) _  / /_/ / __/    / _ \/ __/
 / .__/__,__/_//_/\__/\_,_/\____/_/ /_/|_/\___/\__/
/_/
"""
    print(GREEN + banner + WHITE)
    print(GREEN + "[>]" + CYAN + " Created by : " + WHITE + "thewhiteh4t")
    print(GREEN + "[>]" + CYAN + " Version    : " + WHITE + version + "\n")


def main():
    global addr, file

    print(GREEN + "[+]" + CYAN + " Bypassing Cloudflare Restriction..." + WHITE + "\n")
    useragent = {"User-Agent": "pwnedornot"}
    cookies, user_agent = cfscrape.get_tokens(
        "https://haveibeenpwned.com/api/v2/breachedaccount/test@example.com",
        user_agent="pwnedornot",
    )

    # starts calculating script runtime
    start = time.time()

    # quit function prints total script runtime and exits
    def quit():
        print_info(
            " Completed in ", str(time.time() - start) + CYAN + " seconds." + WHITE
        )
        exit()

    def dump():
        dumplist = []
        # r2 is the query for pastebin accounts if we get a 404, account does not have any dumps
        r2 = requests.get(
            "https://haveibeenpwned.com/api/v2/pasteaccount/{}".format(addr),
            headers=useragent,
            cookies=cookies,
        )
        check2 = r2.status_code

        if check2 != 200:
            print("\n" + RED + "[-]" + CYAN + " No Dumps Found... :(" + WHITE)
            # print ('\n' + G + '[+]' + C + ' Completed in ' + W + str(time.time()-start) + C + ' seconds.' + W)
        else:
            print_info(" Dumps Available...!")
            print_info(" Getting Dumps...this may take a while...")
            json2 = r2.content.decode("utf-8")
            simple2 = json.loads(json2)

            # checking if dump is accessible
            for item in simple2:
                if (item["Source"]) == "Pastebin":
                    link = item["Id"]
                    url = "https://www.pastebin.com/raw/{}".format(link)
                    page = requests.get(url)
                    sc = page.status_code
                    if sc != 404:
                        dumplist.append(url)

                elif (item["Source"]) == "AdHocUrl":
                    url = item["Id"]
                    try:
                        page = requests.get(url)
                        sc = page.status_code
                        if sc != 404:
                            dumplist.append(url)
                    except requests.exceptions.ConnectionError:
                        pass

            print_info("Got ", str(len(dumplist)) + CYAN + " Dumps")
        if str(len(dumplist)) != "0":
            print_info(" Passwords:")
            for entry in dumplist:
                page = requests.get(entry)
                page_dict = page.content.decode("utf-8", "ignore")
                passwd = re.search("{}:(\w+)".format(addr), page_dict)
                if passwd:
                    print(GREEN + "[+] " + WHITE + passwd.group(1))
                elif not passwd:
                    for line in page_dict.splitlines():
                        passwd = re.search("(.*{}.*)".format(addr), line)
                        if passwd:
                            print(GREEN + "[+] " + WHITE + passwd.group(0))

    def check():
        print_info(" Looking for Breaches...")
        # sleep 2 seconds to avoid rate limit
        time.sleep(2)
        # r1 is the query for the account user enters
        r1 = requests.get(
            "https://haveibeenpwned.com/api/v2/breachedaccount/{}".format(addr),
            headers=useragent,
            cookies=cookies,
            verify=True,
        )
        # check1 is the status code for the account if we get a 404, account is not breached
        check1 = r1.status_code

        if check1 == 404:
            print("\n" + RED + "[-]" + CYAN + " No Breaches Found... :( \n" + WHITE)
            print_info("Looking for Dumps...")
            dump()

        else:
            print(
                "\n"
                + GREEN
                + "[!]"
                + CYAN
                + " Account pwned...Listing Breaches..."
                + WHITE
            )
            json1 = r1.content.decode("utf8")
            simple1 = json.loads(json1)

            for item in simple1:
                print_breach(item)
            dump()

    def filecheck():
        time.sleep(2)
        r3 = requests.get(
            "https://haveibeenpwned.com/api/v2/breachedaccount/{}".format(addr),
            headers=useragent,
            cookies=cookies,
            verify=True,
        )
        check3 = r3.status_code

        if check3 == 404:
            print("\n" + RED + "[-]" + CYAN + " Account not pwned... :(" + WHITE)
        else:
            print(
                "\n"
                + GREEN
                + "[!]"
                + CYAN
                + " Account pwned...Listing Breaches..."
                + WHITE
            )
            json1 = r3.content.decode("utf8")
            simple1 = json.loads(json1)

            for item in simple1:
                print_breach(item)
        dump()

    if not addr and not file:
        addr = raw_input(GREEN + "[+]" + CYAN + " Enter Email Address : " + WHITE)
        check()
    elif arg.email:
        print(
            "\n"
            + GREEN
            + "[+]"
            + CYAN
            + " Checking Breach status for "
            + WHITE
            + "{}".format(addr)
        )
        check()
    elif file:
        print(
            GREEN
            + "[+]"
            + CYAN
            + " Reading Emails Accounts from "
            + WHITE
            + "{}".format(file)
        )
        with open(file) as dict:
            for line in dict:
                line = line.strip()
                addr = line
                if addr != "":
                    print()
                    print_info(" Checking Breach status for ", addr)
                    check()
    quit()


try:
    banner()
    update()
    main()
except KeyboardInterrupt:
    print("\n" + RED + "[!]" + CYAN + " Keyboard Interrupt." + WHITE)
    exit()
