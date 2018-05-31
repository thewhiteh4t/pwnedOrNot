# pwnedOrNot
## Introduction
pwnedOrNot is a python script which checks if the email account has been compromised in a data breach, if the email account is compromised it proceeds to find **passwords** for the compromised account.

It uses [**haveibeenpwned**](https://haveibeenpwned.com/API/v2) v2 api to test email accounts and searches for the **password** in **Pastebin Dumps**

This script has been tested on
* **Kali Linux 18.2**
* **Ubuntu 18.04**
* **Kali Nethunter**
* **Termux**

**Works with both Python2 and Python3**

## Installation
**Ubuntu and Kali**

```bash
# Python 2
pip install cfscrape
apt-get install nodejs

# Python 3
apt-get install python3-pip
pip3 install requests
pip3 install cfscrape
```

**Termux**
```bash
# Python 2
pkg install python2
pkg install git
pip2 install requests
pip2 install cfscrape

# Python 3
pkg install python2
pip install requests
pip install cfscrape
```

Other common standard python modules pwnedornot uses:
* os
* re
* time
* json
* requests

## Usage
```bash
git clone https://github.com/thewhiteh4t/pwnedOrNot.git
cd pwnedOrNot/
python pwnedornot.py
```

```bash
python pwnedornot.py -h
usage: pwnedornot.py [-h] [-e EMAIL] [-f FILE]

optional arguments:
  -h, --help              show this help message and exit
  -e EMAIL, --email EMAIL Email account you want to test
  -f FILE, --file FILE    Load a file with multiple email accounts
```

## Features
[**haveibeenpwned**](https://haveibeenpwned.com/API/v2) offers a lot of information about the compromised email, some useful information is displayed by this script:
* Name of Breach
* Domain Name
* Date of Breach
* Fabrication status
* Verification Status
* Retirement status
* Spam Status
* Source of Dump
* ID of Dump

And with all this information **pwnedOrNot** can easily find passwords for compromised emails if the dump is accessible and it contains the password
## Screenshots
![example](https://github.com/thewhiteh4t/pwnedOrNot/blob/master/pwned1.png)
![example](https://github.com/thewhiteh4t/pwnedOrNot/blob/master/pwned2.png)

Also works on Kali Nethunter

![example](https://github.com/thewhiteh4t/pwnedOrNot/blob/master/nethunter1.png)
![example](https://github.com/thewhiteh4t/pwnedOrNot/blob/master/nethunter2.png)
