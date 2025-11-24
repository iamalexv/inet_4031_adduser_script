#!/usr/bin/python3

# INET4031
# Alex Vladimirov
# 11/05/25
# 11/05/25

# script that creates user accounts on linux from an input file
import os # a way to run system commands like adduser and passwd
import re # gives regular expressions for pattern matching
import sys # stdin 

def main():
    for line in sys.stdin:

        # skip lines starting with a # because they are comments in the input file
        match = re.match("^#",line)

        # when outputed it seperates the data using a : 
        fields = line.strip().split(':')

        # skips a line if it is a comment or does not have exactly 5 fields in the input file 
        if match or len(fields) != 5:
            continue

        # takes the user details from the input file 
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])

        # splits up the comma seperated list into a individual data point
        groups = fields[4].split(',')

        # to notify what account is being created
        print("==> Creating account for %s..." % (username))
        # preping system command to create a user without setting a password yet
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)

        print(cmd) # for debugging purposes
        os.system(cmd) # sets the users password

        # shows that the users password has been set
        print("==> Setting the password for %s..." % (username))
        # preping the system command to create a user without setting a password yet
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

        print (cmd) # for debugging purposes
        os.system(cmd) # sets the users password

        for group in groups:
            # only assign the user to a group if it is not '-' which means that there is no group assignment
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                print(cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()
