#!/usr/bin/env python3

from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument("-e", "--email", required=False, help="Email address")
ap.add_argument(
    "-f", "--file", required=False, help="input file with multiple email addresses"
)
ap.add_argument(
    "-s", "--save", required=False, help="Output file for pwned email addresses"
)
ap.add_argument("-d", "--domain", required=False, help="Filter results by domain name")
ap.add_argument(
    "-b", "--breach", required=False, help="Get info about a breach by breach name"
)
ap.add_argument(
    "-n",
    "--nodumps",
    required=False,
    action="store_true",
    help="Only Check Breach Info and Skip Password Dumps",
)
ap.add_argument(
    "-l",
    "--list",
    required=False,
    action="store_true",
    help="Get List of all pwned Domains",
)
ap.add_argument("-c", "--check", required=False, help="Check if your Domain is pwned")
ap.add_argument("-k", "--key", required=False, help="API Key")
arg = ap.parse_args()
addr = arg.email
file = arg.file
save = arg.save
domain = arg.domain
breach_name = arg.breach
nodumps = arg.nodumps
list_domain = arg.list
check_domain = arg.check
key = arg.key

R = "\033[31m"  # red
G = "\033[32m"  # green
C = "\033[36m"  # cyan
W = "\033[0m"  # white
Y = "\033[33m"  # yellow

version = "1.3.1"

state = {"api_key": None, "user_agent": None, "start_time": None, "idle_time": 1.6}

from json import dumps, loads
from os import environ, getenv, path, remove
from re import search
from sys import exit
from time import sleep, time

import requests
from html2text import html2text

if "HOME" in environ:
    home = getenv("HOME")
elif "USERPROFILE" in environ:
    home = getenv("USERPROFILE")
conf_path = path.join(home, ".config", "pwnedornot", "config.json")

if "PWNED_API_KEY" in environ:
    state["api_key"] = getenv("PWNED_API_KEY")

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
    banner = r"""
                                  ______       _   __      __
    ____ _      ______  ___  ____/ / __ \_____/ | / /___  / /_
   / __ \ | /| / / __ \/ _ \/ __  / / / / ___/  |/ / __ \/ __/
  / /_/ / |/ |/ / / / /  __/ /_/ / /_/ / /  / /|  / /_/ / /_
 / .___/|__/|__/_/ /_/\___/\__,_/\____/_/  /_/ |_/\____/\__/
/_/
"""
    print(G + banner + W)
    print(f"{C}[>]{W} Created by : thewhiteh4t")
    print(f"{C}[>]{W} Version    : {version}\n")


def read_config():
    with open(conf_path, "r") as config:
        json_cnf = loads(config.read())
        key = json_cnf["api_key"]
        if len(key) > 0:
            print(f"{C}[*]{W} API key found in config.json...\n")
        else:
            print(f"{R}[-]{W} API key not found in config.json...\n")
            print(f"{C}[*]{W} Get your API Key : https://haveibeenpwned.com/API/Key \n")
            enter_key = input(f"{C}[*]{W} Enter your API Key :")
            enter_key = enter_key.strip()

            with open(conf_path, "w") as keyfile:
                key_dict = {"api_key": enter_key}
                json_data = dumps(key_dict)
                keyfile.write(json_data)
            print(f"{G}[+]{W} Saved API key in : {conf_path}\n")
    return key


def main():
    global addr
    start = time()
    state["start_time"] = start

    banner()
    if not key and not state.get("api_key"):
        state["api_key"] = read_config()

    api_key = state.get("api_key")
    useragent = {"User-Agent": "pwnedOrNot", "hibp-api-key": api_key}
    state["user_agent"] = useragent
    idle_time = state.get("idle_time")

    if save and path.exists(save):
        remove(save)

    if list_domain:
        domains_list()
    elif check_domain:
        domain_check()
    elif breach_name:
        breach_info()
    elif addr and domain:
        filtered_check()
    elif addr and not domain:
        check()
    elif file and not domain:
        print(f"{C}[*]{W} Reading Emails Addresses from {file}\n")
        with open(file) as dict:
            for line in dict:
                line = line.strip()
                addr = line
                if addr != "":
                    check()
                    sleep(idle_time)
    elif file and domain:
        print(f"{C}[*]{W} Reading Emails Addresses from {file}\n")
        print(f"{C}[*]{W} Domain : {domain}")
        with open(file) as dict:
            for line in dict:
                line = line.strip()
                addr = line
                if addr != "":
                    filtered_check()
                    sleep(idle_time)
    else:
        print(
            f"{R}[-]{W} Error : {W}Atleast 1 Argument is Required, Try : {G}python3 pwnedornot.py -h{W}"
        )
        exit()


def check():
    print(f"{G}[+]{W} Checking Breach status for {C}{addr}{W}", end="")
    rqst = requests.get(
        f"https://haveibeenpwned.com/api/v3/breachedaccount/{addr}",
        headers=state.get("user_agent"),
        params={"truncateResponse": "false"},
        timeout=10,
    )
    sc = rqst.status_code
    for code, desc in response_codes.items():
        if sc == code:
            if sc == 200:
                print(f" {Y}[ pwned ]{W}")
                json_out = rqst.content.decode("utf-8", "ignore")
                simple_out = loads(json_out)
                print(f"\n{C}[*]{W} Total Breaches : {len(simple_out)}")
                for item in simple_out:
                    print(
                        f"\n"
                        f"{G}Breach       : {W}{str(item['Title'])} \n"
                        f"{G}Domain       : {W}{str(item['Domain'])} \n"
                        f"{G}Date         : {W}{str(item['BreachDate'])} \n"
                        f"{G}BreachedInfo : {W}{', '.join(item['DataClasses'])} \n"
                        f"{G}Fabricated   : {W}{str(item['IsFabricated'])} \n"
                        f"{G}Verified     : {W}{str(item['IsVerified'])} \n"
                        f"{G}Retired      : {W}{str(item['IsRetired'])} \n"
                        f"{G}Spam         : {W}{str(item['IsSpamList'])}"
                    )

                if not nodumps:
                    dump()
                if save is not None:
                    with open(save, "a") as fileout:
                        fileout.write("" + addr + "\n")
            elif sc == 404:
                print(f" {Y}[ not pwned ]{W}")
                if not nodumps:
                    dump()
            elif sc == 429:
                retry_sleep = float(rqst.headers["Retry-After"])
                print(f" {Y}[ retry in {retry_sleep}s]{W}")
                sleep(retry_sleep)
                check()
            else:
                print(f"\n\n{R}[-]{W} Status {code} : {desc}")


def filtered_check():
    print(f"\n{C}[*]{W} Checking Breach status for {C}{addr}{W}", end="")
    rqst = requests.get(
        f"https://haveibeenpwned.com/api/v3/breachedaccount/{addr}?domain={domain}",
        headers=state.get("user_agent"),
        params={"truncateResponse": "false"},
        verify=True,
        timeout=10,
    )
    sc = rqst.status_code

    for code, desc in response_codes.items():
        if sc == code:
            if sc == 200:
                print(f" {Y}[ pwned ]{W}")
                json_out = rqst.content.decode("utf-8", "ignore")
                simple_out = loads(json_out)

                for item in simple_out:
                    print(
                        f"\n"
                        f"{G}Breach      : {W}{str(item['Title'])} \n"
                        f"{G}Domain      : {W}{str(item['Domain'])} \n"
                        f"{G}Date        : {W}{str(item['BreachDate'])} \n"
                        f"{G}BreachedInfo: {W}{str(item['DataClasses'])} \n"
                        f"{G}Fabricated  : {W}{str(item['IsFabricated'])} \n"
                        f"{G}Verified    : {W}{str(item['IsVerified'])} \n"
                        f"{G}Retired     : {W}{str(item['IsRetired'])} \n"
                        f"{G}Spam        : {W}{str(item['IsSpamList'])}"
                    )
                if nodumps is not True:
                    dump()
            elif sc == 404:
                print(f" {Y}[ not pwned ]{W}")
                if nodumps is not True:
                    dump()
            elif sc == 429:
                retry_sleep = float(rqst.headers["Retry-After"])
                print(f" {Y}[ retry in {retry_sleep}s]{W}")
                sleep(retry_sleep)
                check()
            else:
                print(f"\n{R}[-]{W} Status {code} : {desc}")


def dump():
    dumplist = []
    print(f"\n{C}[+]{W} Looking for Dumps...", end="")
    rqst = requests.get(
        f"https://haveibeenpwned.com/api/v3/pasteaccount/{addr}",
        headers=state.get("user_agent"),
        timeout=10,
    )
    sc = rqst.status_code

    if sc == 429:
        retry_sleep = float(rqst.headers["Retry-After"])
        print(f" {Y}[ retry in {retry_sleep}s]{W}")
        sleep(retry_sleep)
        dump()
    elif sc == 401:
        print()
        json_out = rqst.content.decode("utf-8", "ignore")
        simple_out = loads(json_out)["message"]
        print(f"\n{R}[-]{W} Error : {simple_out}")
    elif sc != 200:
        print(f" {Y}[ No Dumps Found ]{W}")
    else:
        print(f" {Y}[ Dumps Found ]{W}\n")
        json_out = rqst.content.decode("utf-8", "ignore")
        simple_out = loads(json_out)

        for item in simple_out:
            if (item["Source"]) == "Pastebin":
                link = item["Id"]
                try:
                    url = "https://www.pastebin.com/raw/{}".format(link)
                    page = requests.get(url, timeout=10)
                    sc = page.status_code
                    if sc == 200:
                        dumplist.append(url)
                        print(f"{C}[+]{W} Dumps Found : {len(dumplist)}", end="\r")
                    if len(dumplist) == 0:
                        print(f"{R}[-]{W} Dumps are not Accessible...")
                except requests.exceptions.ConnectionError:
                    pass
            elif (item["Source"]) == "AdHocUrl":
                url = item["Id"]
                try:
                    page = requests.get(url, timeout=10)
                    sc = page.status_code
                    if sc == 200:
                        dumplist.append(url)
                        print(f"{G}[+]{W} Dumps Found : {len(dumplist)}", end="\r")
                    if len(dumplist) == 0:
                        print(f"{R}[-]{W} Dumps are not Accessible...")
                except Exception:
                    pass

    if len(dumplist) != 0:
        print(f"\n\n{G}[+]{W} Passwords : {W}\n")
        for entry in dumplist:
            sleep(1.1)
            try:
                page = requests.get(entry, timeout=10)
                dict = page.content.decode("utf-8", "ignore")
                passwd = search(r"{}:(\w+)".format(addr), dict)
                if passwd:
                    print(passwd.group(1))
                elif not passwd:
                    for line in dict.splitlines():
                        passwd = search("(.*{}.*)".format(addr), line)
                        if passwd:
                            print(passwd.group(0))
            except requests.exceptions.ConnectionError:
                pass


def breach_info():
    print(f"{C}[*]{W} Breach Name : {C}{breach_name}{W}", end="")
    rqst = requests.get(
        f"https://haveibeenpwned.com/api/v3/breach/{breach_name}",
        headers=state.get("user_agent"),
        timeout=10,
    )
    sc = rqst.status_code

    for code, desc in response_codes.items():
        if sc == code:
            if sc == 200:
                json_out = rqst.content.decode("utf-8", "ignore")
                simple_out = loads(json_out)
                if len(simple_out) != 0:
                    print(f" {Y}[ pwned ]{W}")
                    print(
                        f"\n"
                        f"Breach      : {W}{str(simple_out['Title'])}\n"
                        f"Domain      : {W}{str(simple_out['Domain'])}\n"
                        f"Date        : {W}{str(simple_out['BreachDate'])}\n"
                        f"Pwn Count   : {W}{str(simple_out['PwnCount'])}\n"
                        f"Fabricated  : {W}{str(simple_out['IsFabricated'])}\n"
                        f"Verified    : {W}{str(simple_out['IsVerified'])}\n"
                        f"Retired     : {W}{str(simple_out['IsRetired'])}\n"
                        f"Spam        : {W}{str(simple_out['IsSpamList'])}\n"
                        f"Data Types  : {W}{str(simple_out['DataClasses'])}"
                    )
                else:
                    print(f" {Y}[ Not Breached ]{W}")
            elif sc == 429:
                retry_sleep = float(rqst.headers["Retry-After"])
                print(f" {Y}[ retry in {retry_sleep}s]{W}")
                sleep(retry_sleep)
                breach_info()
            elif sc == 404:
                print(f" {Y}[ Not Breached ]{W}")
            else:
                print(f"\n{R}[-]{W} Status {code} : {desc}")


def domains_list():
    domains = []
    print(f"{C}[*]{W} Fetching List of Breached Domains...\n")
    rqst = requests.get(
        "https://haveibeenpwned.com/api/v3/breaches",
        headers=state.get("user_agent"),
        timeout=10,
    )
    sc = rqst.status_code

    for code, desc in response_codes.items():
        if sc == code:
            if sc == 200:
                json_out = rqst.content.decode("utf-8", "ignore")
                simple_out = loads(json_out)
                for item in simple_out:
                    domain_name = item["Domain"]
                    if len(domain_name) != 0:
                        print(domain_name)
                        domains.append(domain_name)
                print(f"\n{C}[*]{W} Total : {len(domains)}")
            else:
                print(f"\n{R}[-]{W} Status {code} : {desc}")


def domain_check():
    print(f"{C}[*]{W} Domain Name : {C}{check_domain}{W}", end="")
    rqst = requests.get(
        f"https://haveibeenpwned.com/api/v3/breaches?domain={check_domain}",
        headers=state.get("user_agent"),
        timeout=10,
    )
    sc = rqst.status_code

    for code, desc in response_codes.items():
        if sc == code:
            if sc == 200:
                json_out = rqst.content.decode("utf-8", "ignore")
                simple_out = loads(json_out)

                if len(simple_out) != 0:
                    print(f" {Y}[ pwned ]{W}")
                    for item in simple_out:
                        print(
                            f"\n"
                            f"{G}Breach      : {W}{str(item['Title'])}\n"
                            f"{G}Domain      : {W}{str(item['Domain'])}\n"
                            f"{G}Date        : {W}{str(item['BreachDate'])}\n"
                            f"{G}Pwn Count   : {W}{str(item['PwnCount'])}\n"
                            f"{G}Fabricated  : {W}{str(item['IsFabricated'])}\n"
                            f"{G}Verified    : {W}{str(item['IsVerified'])}\n"
                            f"{G}Retired     : {W}{str(item['IsRetired'])}\n"
                            f"{G}Spam        : {W}{str(item['IsSpamList'])}\n"
                            f"{G}Data Types  : {W}{str(item['DataClasses'])}"
                            f"{G}Description : {W}{html2text(str(item['Description']))}"
                        )
                else:
                    print(f" {Y}[ Not Breached ]{W}")
            elif sc == 404:
                print(f" {Y}[ Not Breached ]{W}")
            else:
                print(f"\n{R}[-]{W} Status {code} : {desc}")


def quit():
    print(f"\n{C}[*]{W} Completed in {(time() - state.get('start_time')):.2f} seconds.")
    exit()


try:
    if __name__ == "__main__":
        main()
        quit()
    else:
        pass
except KeyboardInterrupt:
    print(f"\n{Y}[!]{W} Keyboard Interrupt.")
    exit()
