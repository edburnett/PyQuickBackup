PyQuickBackup
=============

http://github.com/edburnett/pyquickbackup


What is PyQuickBackup?
----------------------
PyQuickBackup (pqb.py) is just a simple tool for file-level backups on Linux
workstations. It creates a tar archive (with bz2 compression) of any directories 
and files you specify in the configuration file (pqb.conf), then moves/copies the
archive to any number of directories or mount-points (such as an external drive or
USB flash stick).

It was built for Python 3.x but could be easily adapted for Python 2.x with 
a few changes.


How do I use PyQuickBackup?
---------------------------
1. Edit the pqb.conf file to your liking with your favorite text editor, 
specifying any directories you wish to include or exlcude in the appropriate sections.
2. Run it from a root/superuser account, or use sudo:

    $ sudo python3 pqb.py
