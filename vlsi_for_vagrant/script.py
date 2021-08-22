# Run command: (TERMINAL) python3 script.py filePath(*.v) typeAnalysis

# Imports
import os
import sys
import io
import datetime
from io import IncrementalNewlineDecoder
from struct import pack
from six import u
from pathlib import Path

# Global Variables for terminal arguments
options = ["-l","-f","-s","-d","-p","-o","-e","-g", "-i","-t"]

# Possible flags for each proccess
validation = {
                "-l":   ["Style Linter",[  
                                        ["cs",  ["--flagfile","--fromenv","--tryfromenv","--undefok","--rules"]],
                                        ["path",["--rules_config", "--waiver_files", "--autofix_output_file"]],
                                        ["set", ["--ruleset"]],
                                        ["des", ["--autofix"]],
                                        ["tf",  ["--show_diagnostic_context","--generate_markdown","--verilog_trace_parser","--parse_fatal","--lint_fatal","--rules_config_search","--check_syntax"]],
                                        ["ru",  ["--help_rules"]],
                                        ["h",   ["--helpfull"]]
                                        ]],

                "-f":   ["Formatter",   [
                                        ["cs",  ["--flagfile","--fromenv","--tryfromenv","--undefok"]],
                                        ["tf",  ["--verilog_trace_parser","--expand_coverpoints","--failsafe_success","--inplace","--show_equally_optimal_wrappings","--show_inter_token_info","--show_token_partition_tree","--try_wrap_long_lines","--verbose","--verify_convergence"]],
                                        ["al",  ["--assignment_statement_alignment","--case_items_alignment","--class_member_variables_alignment","formal_parameters_alignment","--named_parameter_alignment","--named_port_alignment","--net_variable_alignment","--port_declarations_alignment","--struct_union_members_alignment"]],
                                        ["id",  ["--formal_parameters_indentation","--named_parameter_indentation","--named_port_indentation","--port_declarations_indentation"]],
                                        ["n",   ["--lines","--max_search_states","--show_largest_token_partitions"]],
                                        ["h",   ["--helpfull"]]
                                        ]],

                "-s":   ["Parser",      [
                                        ["cs",  ["--flagfile","--fromenv","--tryfromenv","--undefok"]],
                                        ["tf",  ["--verilog_trace_parser","--export_json","--printrawtokens","--printtokens","--printtree","--show_diagnostic_context","--verifytree"]],
                                        ["n",   ["--error_limit"]],
                                        ["h",   ["--helpfull"]]
                                        ]],
                "-p":   ["Project",     [
                                        ["path",["--file_list_path ","--file_list_root"]],
                                        ["cs",["--include_dir_paths"]]
                                        ]],
                "-d":   ["Diff",        [
                                        ["m","--mode"]
                                        ]],
                "-o":   ["Obfuscator",  [
                                        ["tf",  ["--decode","--preserve_interface"]],
                                        ["path",["--load_map","--save_map"]]
                                        ]],
                "-e":   ["Extractor",   [
                                        ["tf",["--printextraction"]],
                                        ["jp",["--print_kythe_facts"]],
                                        ["cs",["--include_dir_paths"]],
                                        ["path",["--file_list_path","--file_list_root"]]
                                        ]]
            }

# Functions
def createCommand(analysisType,fileName):
    switcher = {
                "-l": ["Style Linter","sudo verible/bazel-bin/verilog/tools/lint/verible-verilog-lint"],
                "-f": ["Formatter","sudo verible/bazel-bin/verilog/tools/formatter/verible-verilog-format"],
                "-s": ["Parser","sudo verible/bazel-bin/verilog/tools/syntax/verible-verilog-syntax"],
                "-d": ["Lexical Diff","sudo verible/bazel-bin/verilog/tools/diff/verible-verilog-diff"],
                "-p": ["Verible project tool","sudo verible/bazel-bin/verilog/tools/proyect/verible-verilog-project"],
                "-o": ["Code Obfuscator","sudo verible/bazel-bin/verilog/tools/obfuscator/verible-verilog-obfuscate"],
                "-e": ["Source Code Indexer","sudo verible/bazel-bin/verilog/tools/kythe/verible-verilog-kythe-extractor"]
            }

    filePath = " " + fileName
    commands = []

    # Command flow
    for analysis in analysisType:
        tool = switcher.get(analysis[0])

        flags = ""
        if len(analysis) > 1:
            for flag in analysis[1:]:
                flags += " " + flag

        commands.append([tool[0],tool[1] + flags + filePath + " >> log.txt; cp log.txt /vagrant_data/"])

    return commands

def runCommand(commands):
    # Info Log
    print("[INFO] Starting Vagrant\n")
    f = open('info.txt','a')
    f.write(str(datetime.datetime.now()) + " Starting Vagrant\n")
    f.close()


    # Run work flow
    os.system("echo -n > log.txt; cp log.txt /vagrant_data/")
    for command in commands:
        if(Path("log.txt").stat().st_size != 0):
            break
        else:
            os.system(command[1])            
            if(Path("log.txt").stat().st_size != 0):
                print("\n[ERROR] The analysis failed at "+ command[0]+", check the log.txt for errors")
                break
    print("\n[INFO] Analysis Completed")
    print("\n[INFO] Exiting Vagrant\n")
    # Info Log
    f = open('info.txt','a')
    f.write(str(datetime.datetime.now()) + " Exiting Vagrant\n")
    f.close()


def inputValidation(parameters):

    commands = []
    aux_commands = []

    while(parameters!=[]):

        # Validate type of analisis
        if parameters[0].find("--") != 0:
            if parameters[0] in options:
                pass
            else:
                print("[ERROR] The type of analysis " + parameters[0] + " does not correspond to a valid one.")
                return -1

        if len(parameters) < 2 and parameters[0] in options:
            if aux_commands != []:
                commands.append(aux_commands)
                commands.append([parameters[0]])
                parameters = parameters[1:]
                break
            else:
                commands.append([parameters[0]])
                parameters = parameters[1:]
                break

        elif len(parameters) < 2:
            aux_commands.append(parameters[0])
            commands.append(aux_commands)
            parameters = parameters[1:]
            break

        elif parameters[0] in options and aux_commands != []:
            commands.append(aux_commands)
            aux_commands = [parameters[0]]
            parameters = parameters[1:]

        else:
            aux_commands.append(parameters[0])
            parameters = parameters[1:]

    #print(commands)
    for cmd in commands:
        # Verification of the flags corresponding to the analyzes
        if len(cmd) > 1:
            typeValidation = validation.get(cmd[0])
            m = typeValidation[1]
            result = -1
            validationType = ""
            for flag in cmd[1:]:
                aux_flag = flag.split("=",1)
                for i in m:
                    if aux_flag[0] in i[1]:
                        result = 0
                        validationType = i[0]
            
                if result != 0:
                    print("[ERROR] The " + flag + " flag is not valid for " + typeValidation[0])
                    return -1
                
                # Checking the flags arguments
                if validationType == "cs":
                    if aux_flag[0] != "--flagfile":
                        argFlags = aux_flag[1].split(",")
                        for arg in argFlags:
                            aux_arg = arg.split("=")
                            result = -1
                            for i in m:
                                if aux_arg[0] in i[1]:
                                    result = 0
                            if result != 0:
                                print("[ERROR] The argument " + arg + " is not valid for the flag" + aux_flag[0])
                                return -1

                elif validationType == "path":
                    path = aux_flag[1]
                    if os.path.exists(path) != True:
                        print("[ERROR] Directory " + path +" does not exist")
                        return -1
                    
                elif validationType == "h":
                    pass
                
                elif validationType == "n":
                    try:
                        num = int(aux_flag[1])
                    except:
                        print("[ERROR] Argument " + aux_flag[1] +" is not valid")
                        return -1

                elif validationType == "set" or "des" or "tf" or "ru" or "al" or "id" or "m":
                    multipleOption = {
                                    "set":  ["default","all","none"],
                                    "des":  ["yes","no","interactive"],
                                    "tf":   ["true","false"],
                                    "ru":   ["all"],
                                    "al":   ["align","flush-left","preserve","infer"],
                                    "id":   ["indent","wrap"],
                                    "m":    ["format","obfuscate"],
                                    "jp":   ["json","proto"]
                                    }

                    if aux_flag[1] in multipleOption.get(validationType):
                        pass
                    else:
                        print("[ERROR] Argument " + aux_flag[1] +" is not valid")
                        return -1
    return commands

def dataTreatment():
    # Data treatment
        txt = Path('log.txt').read_text()
        txt1=txt.split('\n')
        txt1=txt1[:-1]

        for i in range(len(txt1)):
            cutter_twopoint = txt1[i].find(":")
            txt1[i]=txt1[i][cutter_twopoint+1:]
            cutter_twopoint = txt1[i].find(": ")
            cutter_parenthesis = 0
            if txt1[i].find(" [") != -1:
                cutter_parenthesis =  txt1[i].find(" [")
            if txt1[i].find(" (syntax-error)")!=-1:
                cutter_parenthesis = txt1[i].find(" (syntax-error)")
            
            temp = txt1[i][cutter_twopoint+1:cutter_parenthesis]
            txt1[i]= [txt1[i][:cutter_twopoint],temp]

        # Summary of errors
        errorList = []
        for i in range(len(txt1)):
            if txt1[i][1] not in errorList:
                errorList.append(txt1[i][1])

        summary = []
        for error in errorList:
            tmp = 0
            for i in range(len(txt1)):
                if txt1[i][1] == error:
                    tmp += 1
            summary.append([tmp,error])

        open("summary.txt","w").close()
        f = open("summary.txt","a")
        for i in range(len(summary)):
            f.write(summary[i][1] + "' is being violated " + str(summary[i][0]) + " times\n")
        f.close()

        #print("[INFO] Summary created")

        #Overwrite data in log.txt
        errorsCount = 0
        open("log.txt","w").close()
        f = open("log.txt","a")
        for i in range(len(txt1)):
            f.write(txt1[i][0] + txt1[i][1] + "\n")
            errorsCount += 1
        f.close()

        #print("[INFO] Log.txt updated")

        # Errors count
        if errorsCount != 0:
            print("[WARNING] "+ str(errorsCount)+" errors found\n")

def workflow(filePath,parameters):
    analysisType = inputValidation(parameters)
    if analysisType != -1:
        
        # Command Preparation
        commands = createCommand(analysisType,filePath)
        runCommand(commands)
        dataTreatment()

# Script
open("info.txt","w").close()
# Validations from terminal
inputFile = sys.argv[1]

# Path or filename
if(os.path.isfile(inputFile)):
  # Workflow
  parameters = []
  for i in range(2,len(sys.argv)):
    parameters.append(sys.argv[i])
    workflow(inputFile,parameters)
else:
  print("[ERROR] The file '" + inputFile + "' cannot be found.")
