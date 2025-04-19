import subprocess
import sys

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    SEPARATOR = '\033[90m' + '─' * 50 + '\033[0m'

banner = f"""{Colors.OKCYAN}
 ▗▄▄▖ ▗▄▄▖ ▗▄▄▖
▐▌   ▐▌   ▐▌   
▝▀▚▖▐▌    ▝▀▚▖
▗▄▄▞▘▝▚▄▄▖▗▄▄▞
{Colors.ENDC}"""

IP_ADDRESS = ""
PROTOCOLS = [
    'ldap', 'mssql', 'wmi', 'ftp', 'vnc', 
    'nfs', 'smb', 'winrm', 'rdp', 'ssh'
]

users = [
    ["username", "password"],
]

def process_output_line(line):
    """Clean output lines by removing ports and [+] markers"""
    if '+' not in line:
        return None
    
    cleaned = line.replace("[+]", "").strip()
    parts = cleaned.split()
    
    filtered = [part for part in parts if not part.isdigit() or not (1024 <= int(part) <= 65535)]
    
    return ' '.join(filtered)

def run_check(username, password, protocol):
    command = [
        "proxychains",
        "-f", "PATH_TO_YOUR_PROXYCHAINS_CONFIG",
        "-q",
        "nxc",
        protocol,
        IP_ADDRESS,
        "-u", username,
        "-p", password
    ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        output_lines = []
        if result.stdout:
            output_lines = filter(None, [
                process_output_line(line) 
                for line in result.stdout.split('\n')
            ])
        
        return list(output_lines), result.stderr, result.returncode
    
    except Exception as e:
        return [], str(e), -1

def main():
    print(banner)
    print(f'{Colors.OKGREEN}Simple Creds Scanner - by ash{Colors.ENDC}\n')

    if len(sys.argv) > 1 and (sys.argv[1] in ['-h', '--help']):
        print(f'{Colors.HEADER}╭{"─"*24}┬{"─"*24}╮')
        print(f'│{Colors.BOLD}CMDS:{Colors.ENDC}{Colors.HEADER}{" "*20}│ {"Usage":23} │')
        print(f'├{"─"*24}┼{"─"*24}┤')
        print(f'│ {Colors.WARNING}-h/--help{Colors.ENDC}{Colors.HEADER}    │ Show help message      │')
        print(f'│ {Colors.WARNING}-ip <IP>{Colors.ENDC}{Colors.HEADER}      │ Specify target IP/CIDR │')
        print(f'╰{"─"*24}┴{"─"*24}╯{Colors.ENDC}')
        return

    global IP_ADDRESS
    if len(sys.argv) > 2 and sys.argv[1] == '-ip':
        IP_ADDRESS = sys.argv[2]

    print(f'{Colors.SEPARATOR}')
    print(f'{Colors.OKBLUE}Starting scan for: {Colors.BOLD}{IP_ADDRESS}{Colors.ENDC}\n')

    for user in users:
        username, password = user
        print(f'{Colors.OKGREEN}➤ User: {Colors.BOLD}{username}{Colors.ENDC}')
        
        for protocol in PROTOCOLS:
            output, error, code = run_check(username, password, protocol)
            
            print(f'\n{Colors.OKCYAN}  Protocol: {Colors.BOLD}{protocol.upper()}{Colors.ENDC}')
            if output:
                for line in output:
                    print(f'  {Colors.OKGREEN}✓{Colors.ENDC} {line}')
            else:
                print(f'  {Colors.FAIL}✗ No successful connections{Colors.ENDC}')
            
            if error:
                print(f'  {Colors.FAIL}⚠ Error: {error.strip()}{Colors.ENDC}')

        print(f'\n{Colors.SEPARATOR}')

if __name__ == "__main__":
    main()
