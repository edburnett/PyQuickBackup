#!/usr/bin/env python3

# pqb.py - PyQuickBackup 0.1
# http://github.com/edburnett/pyquickbackup

import tarfile, re, datetime, shutil, os, subprocess
from sys import exit


class pqb():
    
    def __init__(self):
        # setup some empty lists on instantiation, 
        # for use in config file filtering/parsing    
        self.configlist = []
        self.excludes_corrected = []
        self.remotes = []
        self.excludes = []
        self.includes = []


    # method to check if script is being run as root/sudo. 
    # If not, then exit.
    def isroot(self):
        user = os.getuid()
        if user != 0:
            print("- Must be run as root/sudo.")
            print("- Exiting.\n")
            exit()
    

    # method to load the config file
    def loadconf(self, configfilename):
        self.configfile = open(configfilename, 'r')


    # method to close the config file
    def closeconf(self):
        self.configfile.close()


    # method to parse the config file
    def parseconf(self):
        print("- Parsing config file.")

        # strip comments, empty lines, newlines
        for line in self.configfile:
            # ignore any comment lines beginning with "#"
            if re.compile('^#').search(line) is not None:
                continue
            if not line.strip():
                continue
            else:
                # append to self.configlist list
                self.configlist.append(line.rstrip())


        # get index of include/exclude section designators
        re_i = self.configlist.index('[remotes]')
        in_i = self.configlist.index('[includes]')
        ex_i = self.configlist.index('[excludes]')

        # create lists for remotes, includes, and excludes
        self.remotes = self.configlist[re_i:in_i]
        self.includes = self.configlist[in_i:ex_i]
        self.excludes = self.configlist[ex_i:]

        # now discard the actual config section designators
        self.remotes.remove('[remotes]')
        self.includes.remove('[includes]')
        self.excludes.remove('[excludes]')

        # strip the first "/" character from the excluded dir(s) - makes tarfile module behave
        for x in self.excludes:
            if (x[0] == "/") and (x[-1] == "/"):
                item = x[1:]
                item = item[:-1]
                self.excludes_corrected.append(item)
            elif x[0] == "/":
                item = x[1:]
                self.excludes_corrected.append(item)




def main():
    
    # create instance of our class
    config = pqb()
    
    # check if root/sudo
    config.isroot()

    # load config file, exit if not found
    try:
        config.loadconf('pqb.conf')
        print("- Found config file.")
    except IOError:
        print("- Failed to load configuration file.")
        print("- Exiting.\n")
        exit()
    
    # parse config file
    config.parseconf()
    
    # close config file
    config.closeconf()



if __name__ == "__main__":
    main()
