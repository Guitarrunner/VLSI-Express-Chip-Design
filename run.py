# Run command: python3 run.py filename.v 
# NOTE: Remember that the file needs to be in the utils directory

# Imports
import vagrant
from fabric.api import *
import sys
import os

# Global Variables
options = ["-l","-f","-s","-d","-p","-o","-e"]
command = ""

# Functions
@task
def mytask():
    with hide('warnings'):
        run(command)
        run("cp log.txt /vagrant_data/")
    print("\nExit Vagrant\n")

# Script

# Validations
if not(os.path.exists('./utils/'+sys.argv[1])):
    print("[ERROR] The indicated file cannot be found.")
else:
    if sys.argv[2] not in options:
        print("[ERROR] The type of analysis entered does not correspond to a valid one.")
    else:

        # Command Preparation
        fileName = sys.argv[1]
        analysisType = sys.argv[2]
        
        switcher = {
            "-l": "sudo verible/bazel-bin/verilog/tools/lint/verible-verilog-lint",
            "-f": "sudo verible/bazel-bin/verilog/tools/formatter/verible-verilog-format",
            "-s": "sudo verible/bazel-bin/verilog/tools/syntax/verible-verilog-syntax",
            "-d": "sudo verible/bazel-bin/verilog/tools/diff/verible-verilog-diff",
            "-p": "sudo verible/bazel-bin/verilog/tools/proyect/verible-verilog-project",
            "-o": "sudo verible/bazel-bin/verilog/tools/obfuscator/verible-verilog-obfuscate",
            "-e": "sudo verible/bazel-bin/verilog/tools/kythe/verible-verilog-kythe-extractor"
        }

        filePath = " /vagrant_data/utils/" + fileName
        toLog = " > log.txt" 

        command = switcher.get(analysisType) + filePath + toLog

        # Vagrant connection
        print("Starting Vagrant\n")
        v = vagrant.Vagrant()
        v.up()
        env.hosts = [v.user_hostname_port()]
        env.key_filename = v.keyfile()
        env.warn_only = True
        execute(mytask)