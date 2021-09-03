###############################################################################
# File: model-single.py
# Purpose: To perform protein modeling
#
# Description:
# This file runs protein modeling. The alignment algorithm must be run previous
# running this program. This program will dump the output files in a specified 
# directory.
#
# Usage:
#   py model-single.py  -knowns known_id 
#                       -ali_path path_to_.ali_file
#                       -template_path path_to_pdb_template_file
#                       -results_dir path_to_dump_output_files_in
# 
# Modified by Dennis Kovarik
###############################################################################


from modeller import *
from modeller.automodel import *
import os, sys
import shutil


def usage():
    """
    Displays the useage for the program
    """
    msg = "This script runs model-single.py"
    print(msg)
    
    
def parse_args(cmd_args):
    """
    Parses the command line arguments and returns a dictionary of 
    arguements.
    
    :param args: List of command line arguments to parse_args
    """
    args = {}
    i = 1
    while i < len(cmd_args):
        if cmd_args[i] == '-knowns':
            args['-knowns'] = cmd_args[i+1]
            i += 1
        elif cmd_args[i] == '-ali_path':
            args['-ali_path'] = cmd_args[i+1]
            args['ali_filename'] = args['-ali_path'][args['-ali_path'].rfind("\\")+1:]
            i += 1
        elif cmd_args[i] == '-template_path':
            args['-template_path'] = cmd_args[i+1]
            i += 1
        elif cmd_args[i] == '-results_dir':
            args['-results_dir'] = cmd_args[i+1]
            if args['-results_dir'][-1] != "\\":
                args['-results_dir'] = args['-results_dir'] + "\\"
            i += 1
        i += 1
    return args
 
# Parse the command line arguements 
args = parse_args(sys.argv)
# Get the command line arguments
protein_id = args['-knowns']
ali_path = args['-ali_path']
# Create directories to hold results
if not os.path.isdir(args['-results_dir']):
    os.mkdir(args['-results_dir'])
if not os.path.isdir(args['-results_dir'] + protein_id):
    os.mkdir(args['-results_dir'] + protein_id)
# Copy files over
dest = args['-results_dir'] + protein_id + "\\" + args['ali_filename']
if not os.path.isfile(dest):
    shutil.copy(ali_path, dest)
dest = args['-results_dir'] + protein_id + "\\" + args['-template_path'] 
if not os.path.isfile(dest):
    shutil.copy(args['-template_path'], dest)
# Change into the correct directory
os.chdir(args['-results_dir'])
os.chdir(protein_id)
log_file = open("model-single.log", "w")
orig = sys.stdout
sys.stdout = log_file  
# Run the protein modeling
env = Environ()
a = AutoModel(env, alnfile=args['ali_filename'],
              knowns=protein_id, sequence='Bs',
              assess_methods=(assess.DOPE, assess.GA341))
a.starting_model = 1
a.ending_model = 5
a.make()
sys.stdout = orig
