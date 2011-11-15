#!/usr/bin/env python

# PyQuickBackup
# Simple tool for archiving & backing up files, created primarily as an exercise
# for Python 3.x


# import some shit
from tarfile import *
from sys import exit



# show useless info
def welcome_help():
    
    print("PyQuickBackup 0.1")
    print("Simple tool for archiving & backing up files.\n")
    print("Run with --help for command-line options.\n\n")



# parse the config file, create a few lists
def config_parse():

    configlist = []     # start with empty lists
    includes = []
    excludes = []

    try:
        # open config file
        configfile = open('pyquickbackup.conf', 'r')
        
        # remove comments, empty lines from config and append to list, stripping newline chars
        for line in configfile:
            if re.compile('^#').search(line) is not None:
                continue
            if not line.strip():
                continue
            else:
                configlist.append(line.rstrip())
        

        # get index of include/exclude section designators
        in_i = configlist.index('[includes]')                   
        ex_i = configlist.index('[excludes]')                   

        # create lists for includes and excludes
        includes = configlist[in_i:ex_i]
        excludes = configlist[ex_i:]

        # remove the actual include/exclude section designators
        includes.remove('[includes]')
        excludes.remove('[excludes]')



    # throw error and exit if no config file is found
    except (IOError, UnboundLocalError):
        print("- Config file not found!")
        print("- Set up pyquickbackup.conf before running.\n")
        exit()
    
    
# compresses and creates tar archive
def create_archive():

    pass





def main():

    welcome_help()
    config_parse()
    create_archive()


if __name__ == "__main__":
    main()



