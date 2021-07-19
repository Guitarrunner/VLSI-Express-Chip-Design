# VLSI-Express-Chip-Design
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

The main objective is to unify different chip development technologies (free software) and provide a solution
ready to use (Docker / Container).

## Prerequisites
- Python 3.8.10
- [vagrant] 2.2.16
- [virtualbox] 6.1.22 (Windows/MAC)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.1.16 (Linux) 

## Build
To build, you need [vagrant] and [virtualbox]

```bash
# Build all tools and libraries
vagrant up
```

To run the script, first it is necessary to run the following command, to install the necessary requirements

```bash
# Build all tools and libraries for script
pip3 install -r requirements.txt
```


## How to use
The tool developed has two ways of using it, one through the interface and the other through the terminal

### Via interface
In order to start the interface, you must write the following command:

```bash
# Run Interface
python3 scriptMaster.py -g
```

### Via Terminal
In order to run the analysis, the following command must be used:

```bash
# Run in Terminal
python3 scriptMaster.py fileName.v -typeAnalysis
```
The types of analysis available are:
- -l: check lint's rule
- -f: formatter your code
- -s: check sintax

## Functioning
The program run a script that is responsible for analyzing the code of the selected file. This script uses the [verible] tool, whose main mission is to parse SystemVerilog

After running, a .txt file will be created in which you can see the analysis performed on the document.


[vagrant]:https://www.vagrantup.com/
[virtualbox]: https://www.virtualbox.org/
[verible]: https://github.com/google/verible/blob/master/README.md
[python-vagrant]: https://pypi.org/project/python-vagrant/
[Fabric3]: https://pypi.org/project/Fabric3/
[Tkinter]: https://www.tutorialspoint.com/how-to-install-tkinter-in-python
[Pygments]: https://pygments.org/