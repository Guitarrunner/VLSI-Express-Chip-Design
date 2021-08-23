# VLSI-Express-Chip-Design
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

The main objective is to unify different chip development technologies (free software) and provide a solution
ready to use (Docker / Container).
 
## Requisites  
The necessary requirements to run the program are   
- Python 3.8.10
- [Git] 
- [vagrant] 2.2.16
- [virtualbox] 6.1.22 (Windows/MAC) | 6.1.16 (Linux) 

## Installation
To build the program, you need [vagrant] and [virtualbox]

### Step one
```bash
# Build all tools and libraries 
vagrant up 
```
The approximate time of the command is around 40 minutes.

### Step two
```bash
# Build all tools and libraries for script
pip3 install -r requirements.txt
```
Note: For those people who are new to tools like git, we recommend looking at the installation [infographic], which shows the steps in a more detailed way.


## How to use
The tool has four modes of use: one through the interface and three through the interface

### Via interface
In order to start the interface, you must write the following command:

```bash
# Run Interface
python scriptMaster.py -g
```

### Via Terminal
As mentioned previously, there are three modes of use through the terminal, which are:

* Script mode

```bash
# Run in Terminal
python scriptMaster.py <filePath(*.v)>  <flowAnalisis>
```

**Note:** In the case of not knowing the path of the file, just write the flow of the analysis, the tool will open a small interface so that you can choose the file, without having to worry about the path

**Note:** The term <flowanalisis> includes both the type of analysis and the flags in case the user needs to include them.

* Interactive mode

```bash
# Run in Terminal
python scriptMaster.py -i
```

In this mode, n quantity of analyzes can be executed, without the need to close the vagrant session.

* Terminal mode

```bash
# Run in Terminal
python scriptMaster.py -t
```
This mode creates an ssh connection with vagrant, resulting in a private terminal.\
**Note:** inside the virtual machine, a script with the same format as the script mode was installed, for greater convenience

## Analysis types
The program run a script that is responsible for analyzing the code of the selected file. This script uses the [verible] tool, whose main mission is to parse SystemVerilog.

The types of analysis available are:
- -l: style linter
- -f: formatter
- -s: parser
- -d: lexical diff
- -p: verible project tool
- -c: code obfuscator
- -e: source code indexer

For more information on the analysis and the flags for each analysis, you can consult [verible].

## Examples
* Analysis only
```bash
# Run in Terminal
python scriptMaster.py /home/racso/Example1.v -s -l -f
```




[Git]:https://git-scm.com/downloads
[vagrant]:https://www.vagrantup.com/
[virtualbox]: https://www.virtualbox.org/
[verible]: https://github.com/google/verible/blob/master/README.md
[python-vagrant]: https://pypi.org/project/python-vagrant/
[Fabric3]: https://pypi.org/project/Fabric3/
[Tkinter]: https://www.tutorialspoint.com/how-to-install-tkinter-in-python
[Pygments]: https://pygments.org/
[infographic]: https://github.com/Guitarrunner/VLSI-Express-Chip-Design/blob/main/Installation%20manual_compressed.pdf