# VLSI-Express-Chip-Design
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

The main objective is to unify different chip development technologies (free software) and provide a solution
ready to use (Docker / Container).

## Build
To build, you need [vagrant] and [virtualbox]

```bash
# Build all tools and libraries
vagrant up
```

## How to use
First of all, it must be borne in mind that the file to be executed must be in the utils folder found in the repository.

Inside the repository caprpet a terminal must be opened. Before running any command, it must be verified if the virtual machine is suspended, in that case the following command is run.

```bash
# In the case virtualbox is suspend
vagrant reload
```
In the event that the virtual machine is not suspended, the following command must be executed to establish the connection.

```bash
# Vagrant conection
vagrant ssh
```

The next step is to run the script that is responsible for analyzing the code of the selected file. This script uses the [verible] tool, whose main mission is to parse SystemVerilog

```bash
# Run Script (Remenber that)
sh script.sh filename.v
```
After running, a .txt file will be created in which you can see the analysis performed on the document.

## Notas
- pip install python-vagrant
- pip3 install fabric

[vagrant]:https://www.vagrantup.com/
[virtualbox]: https://www.virtualbox.org/
[verible]: https://github.com/google/verible/blob/master/README.md
