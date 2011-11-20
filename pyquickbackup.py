#!/usr/bin/env python

# PyQuickBackup
# Simple tool for archiving & backing up files, created primarily as an exercise
# for Python 3.x


# import some shit
import tarfile, re, datetime, shutil, os, subprocess
from sys import exit
#from os import remove, path



# show useless info
def welcome_help():
    
    print("PyQuickBackup 0.1")
    print("Simple tool for archiving & backing up files.\n")
    # print("Run with --help for command-line options.\n\n")



# parse the config file, create a few lists
def config_parse():

    configlist = []     # start with empty lists
    global includes
    includes = []
    global excludes
    excludes = []
    global remotes
    remotes = []
    global excludes_corrected
    excludes_corrected = []

    try:
        # open config file
        configfile = open('pyquickbackup.conf', 'r')
        
        # strip comments, empty lines, newlines from config file and append to 'configlist' list
        for line in configfile:
            if re.compile('^#').search(line) is not None:
                continue
            if not line.strip():
                continue
            else:
                configlist.append(line.rstrip())
        

        # get index of include/exclude section designators
        re_i = configlist.index('[remotes]')
        in_i = configlist.index('[includes]')                   
        ex_i = configlist.index('[excludes]')                   

        # create lists for remotes, includes, and excludes
        remotes = configlist[re_i:in_i]
        includes = configlist[in_i:ex_i]
        excludes = configlist[ex_i:]

        # now discard the actual configuration section designators
        remotes.remove('[remotes]')
        includes.remove('[includes]')
        excludes.remove('[excludes]')

        #strip the first / character from the excluded dir(s)
        for x in excludes:
            if (x[0] == "/") and (x[-1] == "/"):
                item = x[1:]
                item = item[:-1]
                excludes_corrected.append(item)
            elif x[0] == "/":
                item = x[1:]
                excludes_corrected.append(item)

    # throw error and exit if no config file is found
    except (IOError, UnboundLocalError):
        print("- Config file not found!")
        print("- Set up pyquickbackup.conf before running.\n")
        exit()
    
    
# compresses and creates tar archive, then moves to remote(s)
def create_archive():
    
    
    # run pacman to get list of installed packages (archlinux-specific)
    subprocess.call("pacman " + "-Qe > mypackages.list", shell=True)
    
    
    # create object for getting current date/time
    now = datetime.datetime.now()

    # create filename for archive based on date and time
    filename = now.strftime("%y-%m-%d_%I.%M") + ".tar.bz2"

    # create filtered keyword; print each filename backed up
    def filtered(info):
        if info.name in excludes_corrected:
            return None
        print(info.name)
        return info

    
    # create archive
    tar = tarfile.open(filename, "w:bz2")
    for name in includes:
        tar.add(name, filter=filtered)
    tar.add('mypackages.list')      # add the pacman package list created above
    tar.close()

    # copy archive to location(s) specified under [remotes]
    for dest in remotes:
        if remotes == None:
            print("No remotes to copy to.")
            break
        else:
            print("Copying archive to specified remote: ", dest)
            shutil.copy2(filename, dest)


    # finally, delete the temp files
    if os.path.exists(filename) == True:
        os.remove(filename)                 # remove the archive
        os.remove('mypackages.list')        # remove the pacman packages list
        if os.path.exists(filename) == False:
            print("Temp. File(s) successfully removed.")




def main():

    welcome_help()
    config_parse()
    create_archive()


if __name__ == "__main__":
    main()



