echo
echo "> This script will install dependencies and configuration file"
echo
echo "> If you encounter any error please fix them before using the tool"
echo
echo "[!] Installing Requests..."
echo "--------------------------"
pip3 install requests
pip3 install html2text
echo "--------------------------"

echo "[!] Creating Directory : $HOME/.config/pwnedornot"
mkdir -p $HOME/.config/pwnedornot

echo "[!] Copying config.json..."
cp config.json $HOME/.config/pwnedornot/config.json

echo "[+] DONE"
