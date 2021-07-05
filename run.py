# Run command: python3 run.py

# Imports
import vagrant
from fabric.api import *
import sys

# Functions
@task
def mytask():
    scriptLine = 'sh script.sh '
    fileName = sys.argv[1]
    run(scriptLine+fileName)

# Script
v = vagrant.Vagrant()
v.up()
env.hosts = [v.user_hostname_port()]
env.key_filename = v.keyfile()
env.warn_only = True
execute(mytask)