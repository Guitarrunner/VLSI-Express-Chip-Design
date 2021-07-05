# Script in charge of analyze code
# This is just a test, we need to define the correct work flow according the technicians
# run command: sh script.sh filename

# Work flow
echo "File Selected: $1"
echo "Start of analysis..."
sudo verible/bazel-bin/verilog/tools/lint/verible-verilog-lint /vagrant_data/utils/$1 >log.txt
echo "End of analysis..."
cp log.txt /vagrant_data/