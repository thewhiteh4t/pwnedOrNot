echo '[!] Updating...'
apt-get update > install.log
echo
echo '[!] Installing Dependencies...'
echo '    Python'
apt-get -y install python3 python3-pip &>> install.log
echo '    NodeJS'
apt-get -y install nodejs &>> install.log
echo '    Requests'
pip3 install requests &>> install.log
echo '    CfScrape'
pip3 install cfscrape &>> install.log
echo
echo '[!] Installed.'
