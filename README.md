<p align="center"><img src="https://i.imgur.com/ojjMbWX.jpg"></p>

<h4 align="center">OSINT Tool for Finding Passwords of Compromised Email Accounts</h4>

<p align="center">
  <a href="https://twitter.com/thewhiteh4t"><b>Twitter</b></a>
  <span> - </span>
  <a href="https://t.me/thewhiteh4t"><b>Telegram</b></a>
  <span> - </span>
  <a href="https://thewhiteh4t.github.io"><b>Blog</b></a>
</p>

| Available | in | |
|-|-|-|
| [BlackArch Linux](https://blackarch.org/) | [SecBSD](https://secbsd.org/) | [Tsurugi Linux](https://tsurugi-linux.org/) |
| ![](https://i.imgur.com/1wJVDV5.png) | ![](https://i.imgur.com/z36xL8c.png) | ![Tsurugi Linux](https://i.imgur.com/S1ylcp7.jpg) |

---

pwnedOrNot works in two phases. In the **first** phase it tests the given email address using [**`HaveIBeenPwned v3 API`**](https://haveibeenpwned.com/API/v3) to find if the account have been breached in the past and in the **second** phase it searches the **password** in available **public dumps**.

**`An API Key is required to use the tool. You can purchase a key from HIBP website linked below`**

https://haveibeenpwned.com/API/v3

---

## Featured

<a href="https://jakecreps.com/2019/05/08/osint-collection-tools-for-pastebin/">**> OSINT Collection Tools for Pastebin - Jake Creps**</a>

<a href="https://eforensicsmag.com/download/open-source-forensic-tools/">**> eForensics Magazine May 2020**</a>

---

## Changelog

https://github.com/thewhiteh4t/pwnedOrNot/wiki/Changelog

---

## Features

[**haveibeenpwned**](https://haveibeenpwned.com/API/v3) offers a lot of information about the compromised email, pwnedOrNot displays most useful information such as :

* Name of Breach
* Domain Name
* Date of Breach
* Fabrication status
* Verification Status
* Retirement status
* Spam Status

### About Passwords

The chances of finding passwords depends upon the following factors :

* If public dumps are available for the email address
* If the public dumps are accessible
  * Sometimes the dumps are removed
* If the public dump contains password
  * Sometimes a dump contains only email addresses

#### Tested on
* **Kali Linux**
* **BlackArch Linux**
* **Kali Nethunter**
* **Termux**

> Windows users are suggested to use Kali Linux WSL2 or a VM

## Installation
**Ubuntu / Kali Linux / Nethunter / Termux**

```bash
git clone https://github.com/thewhiteh4t/pwnedOrNot.git
cd pwnedOrNot
chmod +x install.sh
./install.sh
```

**BlackArch Linux**

```bash
pacman -S pwnedornot
```

**Docker**

```bash
git clone https://github.com/thewhiteh4t/pwnedOrNot.git
docker build -t pon .
docker run -it pon
```

## Updates
```bash
cd pwnedOrNot
git pull
```

## Usage
```bash
python3 pwnedornot.py -h

usage: pwnedornot.py [-h] [-e EMAIL] [-f FILE] [-d DOMAIN] [-n] [-l]
                     [-c CHECK]

optional arguments:
  -h, --help                  show this help message and exit
  -e EMAIL, --email EMAIL     Email Address You Want to Test
  -f FILE, --file FILE        Load a File with Multiple Email Addresses
  -d DOMAIN, --domain DOMAIN  Filter Results by Domain Name
  -n, --nodumps               Only Check Breach Info and Skip Password Dumps
  -l, --list                  Get List of all pwned Domains
  -c CHECK, --check CHECK     Check if your Domain is pwned

# Examples

# Check Single Email
python3 pwnedornot.py -e <email>
#OR
python3 pwnedornot.py --email <email>

# Check Multiple Emails from File
python3 pwnedornot.py -f <file name>
#OR
python3 pwnedornot.py --file <file name>

# Filter Result for a Domain Name [Ex : adobe.com]
python3 pwnedornot.py -e <email> -d <domain name>
#OR
python3 pwnedornot.py -f <file name> --domain <domain name>

# Get only Breach Info, Skip Password Dumps
python3 pwnedornot.py -e <email> -n
#OR
python3 pwnedornot.py -f <file name> --nodumps

# Get List of all Breached Domains
python3 pwnedornot.py -l
#OR
python3 pwnedornot.py --list

# Check if a Domain is Pwned
python3 pwnedornot.py -c <domain name>
#OR
python3 pwnedornot.py --check <domain name>
```

## Demo [ YouTube ]
[![Youtube](https://i.imgur.com/aSM6dKc.png)](https://www.youtube.com/watch?v=R_Y_QzVmERA)
