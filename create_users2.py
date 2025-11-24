#!/usr/bin/python3

# INET4031
# Alex Vladimirov
# 11/05/25
# Updated: 11/23/25
# Script that creates user accounts on Linux from an input file
# Now supports interactive dry-run prompt and reads input file internally

import os  # Allows running system commands like adduser and passwd
import re  # Provides regular expressions for pattern matching

def main():
    # Ask user if they want to run in dry-run mode
    dry_run_input = input("Do you want to run in dry-run mode? (Y/N): ").strip().upper()
    while dry_run_input not in ('Y', 'N'):
        dry_run_input = input("Please enter Y or N: ").strip().upper()
    dry_run = dry_run_input == 'Y'

    # Specify the input file internally
    input_file = "create-users.input"

    # Open and read the file line by line
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Skip lines starting with '#' because they are comments in the input file
            match = re.match("^#", line)

            # Split line into fields separated by ':'
            fields = line.split(':')

            # Skip lines that are comments or do not have exactly 5 fields
            if match or len(fields) != 5:
                if dry_run:
                    if match:
                        print(f"[DRY-RUN] Skipping comment line: {line}")
                    else:
                        print(f"[DRY-RUN] Error: Not enough fields in line: {line}")
                continue

            # Extract user details
            username = fields[0]
            password = fields[1]
            gecos = "%s %s,,," % (fields[3], fields[2])

            # Split comma-separated groups
            groups = fields[4].split(',')

            # Notify which account is being created
            print(f"==> Creating account for {username}...")
            cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
            if dry_run:
                print(f"[DRY-RUN] Command would run: {cmd}")
            else:
                os.system(cmd)

            # Notify that password is being set
            print(f"==> Setting the password for {username}...")
            cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
            if dry_run:
                print(f"[DRY-RUN] Command would run: {cmd}")
            else:
                os.system(cmd)

            # Assign user to each group (skip '-' which means no group)
            for group in groups:
                if group != '-':
                    print(f"==> Assigning {username} to the {group} group...")
                    cmd = "/usr/sbin/adduser %s %s" % (username, group)
                    if dry_run:
                        print(f"[DRY-RUN] Command would run: {cmd}")
                    else:
                        os.system(cmd)

if __name__ == "__main__":
    main()
