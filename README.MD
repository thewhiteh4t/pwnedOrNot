# pwnedOrNot
## Introduction
pwnedOrNot is a python script which checks if the email account has been compromised in a data breach, if the email account is compromised it proceeds to find **passwords** for the compromised account.

It uses [**haveibeenpwned**](https://haveibeenpwned.com/API/v2) v2 api to test email accounts and searches for the **password** in **Pastebin Dumps**

This script has been tested on **Kali Linux 18.2** and **Ubuntu 18.04**.

## Installation
It's a pure python script and relies on common python modules and does not need installation :
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
