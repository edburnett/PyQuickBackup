#!/usr/bin/env python3

# pqb.py - PyQuickBackup 0.1
# http://github.com/edburnett/pyquickbackup

import tarfile, re, datetime, shutil, os, subprocess
from sys import exit


class config_loader():
    
    def __init__(self):
    
        self.configlist = []
        #self.includes = []
        #self.excludes = []
        #self.remotes = []
        self.excludes_corrected = []
    

    # load the config file
    def loadconf(self, configfilename):
        self.configfile = open(configfilename, 'r')

    # close the config file
    def closeconf(self):
        self.configfile.close()
    
    # parse the config file
    def parseconf(self):
        print("- Parsing config file.")

        # strip comments, empty lines, newlines
        for line in self.configfile:
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
        remotes = self.configlist[re_i:in_i]
        includes = self.configlist[in_i:ex_i]
        excludes = self.configlist[ex_i:]

        # now discard the actual config section designators
        remotes.remove('[remotes]')
        includes.remove('[includes]')
        excludes.remove('[excludes]')

        # strip the first "/" character from the excluded dir(s)
        for x in excludes:
            if (x[0] == "/") and (x[-1] == "/"):
                item = x[1:]
                item = item[:-1]
                self.excludes_corrected.append(item)
            elif x[0] == "/":
                item = x[1:]
                self.excludes_corrected.append(item)





def main():

    config = config_loader()

    try:
        config.loadconf('pqb.conf')
        print("- Found config file.")
    except IOError:
        print("- Failed to load configuration file.")
        print("- Exiting.\n")
        exit()
    
    config.parseconf()
    config.closeconf()


if __name__ == "__main__":
    main()
