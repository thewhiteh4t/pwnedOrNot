echo '[!] Updating...'
apt-get update > install.log
echo
echo '[!] Installing Dependencies...'
echo '    Python'
apt-get -y install python &>> install.log
echo '    NodeJS'
apt-get -y install nodejs &>> install.log
echo '    Requests'
pip install requests &>> install.log
echo '    CfScrape'
pip install cfscrape &>> install.log
echo
echo '[!] Creating Symlink...'
echo
ln -s $PWD/pwnedornot.py /usr/local/bin/pwnedornot
chmod 777 /usr/local/bin/pwnedornot
echo '[!] Installed...Launch by Typing pwnedornot'
