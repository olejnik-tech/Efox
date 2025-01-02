import os
import json
import sys

def load_config(file_path):
    with open(file_path,'r') as config_file:
            config_data=json.load(config_file)
            print('\nloading configuration ...\n-----')
            for line in config_data:
                print(line + ':\t' + config_data.get(line))
            print('-----\n')
            return config_data

def main(config_param):
    print('loading wordlists ...\n-----')
    wordlists_dir=config_param.get('wordlists_dir')
    wordlists = os.listdir(wordlists_dir)
    wordlists.sort()
    for wordlist in wordlists:
        print(wordlist)
    print('-----\n')

    print('loading targets ...\n-----')
    cap_dir = config_param.get('cap_dir')
    targets = os.listdir(cap_dir)
    targets.sort()

    for i in range(len(targets)):
        print(f"[{i}] {targets[i]}")

    print('Enter the number of a target:')
    user_input = input("tuah$ ")
    target=targets[int(user_input)]

    print(f'\nprocessing hashcat for all wordlists for target {target}...')

    target_files=os.listdir(cap_dir+'/'+target)
    cap_files=[filename for filename in target_files if filename.endswith('.hc22000')]
    print('searching for .hc22000 files')

    latest_cap_file=None

    if cap_files:
        latest_cap_file = cap_files[-1]
        print(f"The latest .hc22000 file is: {latest_cap_file}")
    else:
        print(
        "No .hc22000 files found in the directory.")
        sys.exit()

    for wordlist in wordlists:
        #udo hashcat -m 22000 /home/kali/VirtualShared/Targets+"/"+MATĚJKA_handshake+"/"+hash.hc22000 /home/kali/VirtualShared/Wordlists/001_cracked.txt.gz
        command=f'sudo hashcat -m 22000 {cap_dir}/{target}/{latest_cap_file} {wordlists_dir}/{wordlist}'
        print(command)
        os.system(command)
    print('-----\n')

    # sudo hashcat -m 22000 hash wordlist

if __name__=='__main__':
    config=load_config('config.json')
    main(config)