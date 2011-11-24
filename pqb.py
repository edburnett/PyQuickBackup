#!/usr/bin/env python3

# pqb.py - PyQuickBackup 0.1
# http://github.com/edburnett/pyquickbackup

import tarfile, re, datetime, shutil, os, subprocess
from sys import exit


class pqb():
    
    def __init__(self):
        
        # set version number
        self.version = "0.1"
        
        # archive filename variable
        self.filename = ""
        
        # setup some empty lists on instantiation, 
        # for use in config file filtering/parsing    
        self.configlist = []
        self.excludes_corrected = []
        self.remotes = []
        self.excludes = []
        self.includes = []

    
    def startup(self):

        # print welcome message
        print("PyQuickBackup " + self.version)
        print("Simple tool for archiving & backing up files.\n")

        # get system's current date/time
        now = datetime.datetime.now()

        # set filename of archive to <year>-<month>-<day>_<hour>-<minute>.tar.bz2
        self.filename = now.strftime("%Y-%m-%d_%I-%M") + ".tar.bz2"



    # method to check if script is being run as root/sudo. 
    # If not, then exit.
    def isroot(self):
        user = os.getuid()
        if user != 0:
            print("- ERROR: Must be run as root/sudo.")
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


    def create_archive(self):
        
        # create filtered keyword; print each file/dir being added to archive
        def filtered(info):
            if info.name in self.excludes_corrected:
                return None
            print(info.name)
            return info
        
        # create the archive
        tar = tarfile.open(self.filename, "w:bz2")
        for name in self.includes:
            tar.add(name, filter=filtered)
        #tar.add('mypackages.list')
        tar.close()

        # copy archive to the location(s) specified under [remotes]
        for dest in self.remotes:
            if self.remotes == None:
                print("- Warning: No remotes configured. Leaving archive in working directory.")
                break
            else:
                print("- Copying archive to specified remote: ", dest)
                try:
                    shutil.copy2(self.filename, dest)
                except IOError:
                    print("- ERROR: Copying to remote failed.")
                    print("- Make sure the specified directory/mountpoint exists and you have write permissions.\n")
                    break


                
    # method to delete the working/temp archive after copying to remote(s)    
    def del_archive(self):
        
        # delete temp archive
        if os.path.exists(self.filename) == True:
            os.remove(self.filename)
            #os.remove('mypackages.list')
            if os.path.exists(self.filename) == False:
                print("- Temp file(s) successfully removed.")
                print("- Backup session complete.\n")




def main():
    
    # create instance of our class
    config = pqb()
    
    # run startup stuff
    config.startup()    
    
    # check if root/sudo
    config.isroot()

    # load config file, exit if not found
    try:
        config.loadconf('pqb.conf')
        print("- Found config file.")
    except IOError:
        print("- ERROR: Failed to load configuration file.")
        print("- Exiting.\n")
        exit()
    
    # parse config file
    config.parseconf()

    # create archive
    config.create_archive()
    
    # close config file
    config.closeconf()

    # delete the temp archive
    config.del_archive()



if __name__ == "__main__":
    main()
