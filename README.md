<h1 align="center">pwnedOrNot</h1>
<h4 align="center">
Find Passwords for Compromised Email Accounts
</h4>
<p align="center">
<img src="https://img.shields.io/badge/HaveIBeenPwned-v2-blue.svg?style=plastic">
<img src="https://img.shields.io/badge/Python-3-brightgreen.svg?style=plastic">
<img src="https://img.shields.io/badge/Python-2-brightgreen.svg?style=plastic">
<img src="https://img.shields.io/badge/Termux-✔-red.svg?style=plastic">
<img src="https://img.shields.io/badge/NetHunter-✔-red.svg?style=plastic">
</p>

pwnedOrNot uses [**haveibeenpwned**](https://haveibeenpwned.com/API/v2) v2 api to test email accounts and tries to find the **password** in **Pastebin Dumps**.

## Features
[**haveibeenpwned**](https://haveibeenpwned.com/API/v2) offers a lot of information about the compromised email, some useful information is displayed by this script:
* Name of Breach
* Domain Name
* Date of Breach
* Fabrication status
* Verification Status
* Retirement status
* Spam Status

And with all this information **pwnedOrNot** can easily find passwords for compromised emails if the dump is accessible and it contains the password

#### Tested on
* **Kali Linux 18.2**
* **Ubuntu 18.04**
* **Kali Nethunter**
* **Termux**

## Installation
**Ubuntu and Kali**

```bash
chmod 777 install.sh
./install.sh
```

**Termux**
```bash
# Python 2
pkg install python2
pkg install git
pip2 install requests
pip2 install cfscrape

# Python 3
pkg install python
pip install requests
pip install cfscrape
```

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
