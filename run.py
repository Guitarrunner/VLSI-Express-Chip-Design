# Run command: python3 run.py filename.v 
# NOTE: Remenber that the file needs to be in the utils directory

# Imports
import vagrant
from fabric.api import *
import sys
import os

# Functions
@task
def mytask():
    scriptLine = 'sh script.sh '
    fileName = sys.argv[1]
    run(scriptLine+fileName)
    print("Exit Vagrant\n")
    print("-------------------- Analysis Result --------------------")
    os.system('cat log.txt')

# Script
print("Starting Vagrant\n")
v = vagrant.Vagrant()
v.up()
env.hosts = [v.user_hostname_port()]
env.key_filename = v.keyfile()
env.warn_only = True
execute(mytask)