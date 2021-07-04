# Script in charge of analyze code
# This is just a test, we need to define the correct work flow according the technicians
# run command: sh script.sh filename 2>>

# Work flow
echo "File Selected: $1"
sudo verible/bazel-bin/verilog/tools/lint/verible-verilog-lint utils/$1 >>log.txt

