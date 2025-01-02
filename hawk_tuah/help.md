# Handshake


# Brute-force
- .cap file convert to hashcat supported file on https://hashcat.net/cap2hashcat/
- todo: find how to do it locally
- check https://hashcat.net/wiki/doku.php?id=cracking_wpawpa2 for process
- process with $ 
```bash
hashcat -m 22000 hash.hc22000 cracked.txt.gz
```
## wordlists
- https://github.com/kkrypt0nn/wordlists

# Useful Commands

# For Craft
```bash
sudo hashcat -m 22000 hash rockyou.zip
```
```bash
sudo hashcat -m 22000 ~/VirtualShared/Targets/Moninav_handshake/hash.hc22000 rockyou.zip
```
~/VirtualShared/Targets/Moninav_handshake/hash.hc22000


sudo hashcat -m 22000 ~/VirtualShared/Targets/Moninav_handshake/hash.hc22000 rockyou.zip
# Disclaimer
These scripts are for educational purposes only. I am not responsible of any of your actions you may do with the help of these scripts.


# TODO
dongle does not always work
bad copy of mac address
exception with adapter (probably when not recognized USB yet)
SSID folder - couldn't see the wifi
todo ssid filter
naming of handshake/cracked