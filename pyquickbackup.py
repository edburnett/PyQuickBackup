#!/usr/bin/env python

# PyQuickBackup
# Simple tool for archiving & backing up files
# for Python 3.x


from tarfile import *
import re



def welcome_help():
    
    print("PyQuickBackup 0.1")
    print("Simple tool for archiving & backing up files.\n")
    print("Run with --help for command-line options.\n\n")


def config_parse():

    configlist = []     # start with an empty list

    try:
        configfile = open('pyquickbackup.conf', 'r')            # opens the config file, if it exists
        
        for line in configfile:
            if re.compile('^#').search(line) is not None:       # ignore comments
                continue
            if not line.strip():                                # ignore empty lines
                continue
            else:
                configlist.append(line.rstrip())                # add remaining lines to configlist list

        print(configlist)



    except (IOError, UnboundLocalError):                        # if .conf file not found, throw error
        print("- Config file not found!")
        print("- Set up pyquickbackup.conf before running.\n")
    
    



def main():

    welcome_help()
    config_parse()


if __name__ == "__main__":
    main()



