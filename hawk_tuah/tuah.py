import os
import json
import sys
import time
import subprocess

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

    print('# don\'t forget to get correct .hc22000 file from https://hashcat.net/cap2hashcat/\n')

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

    with open('tuah_output.txt', 'a') as output_file:

        for wordlist in wordlists:
            cap_file=f'{cap_dir}/{target}/{latest_cap_file}'
            wordlist=f'{wordlists_dir}/{wordlist}'
            command=(
                'sudo hashcat '
                f'--potfile-disable -m 22000 {cap_file} {wordlist} | '
                f'tee -a plain_output.txt'
            )
            print(f'========== STARTING HASHCAT ==========\n{command}')
            subprocess.run(command, shell=True)
            time.sleep(5)
            get_filtered_results()
    print('-----\n')

def get_filtered_results():
    plain_output = 'plain_output.txt'
    filtered_output = 'tuah_output.txt'

    status_cracked='Status...........: Cracked'
    other_lines=[
        'Guess.Base.......:',
        'Status...........:'
                 ]
    with open(plain_output, 'r') as infile:
        lines = infile.readlines()

    with open(filtered_output, 'a') as outfile:
        for i, line in enumerate(lines):
            # other lines to print
            if contains_any(line, other_lines):
                outfile.write(lines[i])
            # cracked status has password 5 lines above
            if status_cracked in line:
                target_line_index = i - 4
                if target_line_index < len(lines):
                    outfile.write(lines[target_line_index])

    with open(plain_output, 'w'):
        pass

def contains_any(target_string, substrings):
    return any(substring in target_string for substring in substrings)

if __name__=='__main__':
    config=load_config('config.json')
    main(config)