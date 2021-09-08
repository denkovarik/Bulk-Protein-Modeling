# File: ec_scrape_gui.py
#
# Description:
# This program is the GUI version of ec_scrape.py.
# Performs a blast on sequences or parses downloaded BLAST result files. 
# for proteins in a genome annotation. Afterwards it then searches 
# online databases like NCBI protein and UniProt for their EC Number. This
# is the main program file which is the start of the program.
#
# Author: Dennis Kovarik

import PySimpleGUI as sg
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
import shutil
import xlwings as xw
import pandas as pd
from classes.Annot_Reader import *
from classes.PSI_BLAST import PSI_BLAST
from run_psiblast_utils import *
from classes.BLAST_Rslts_Itr import BLAST_Rslts_Itr
from classes.strategy import Outfmt_0_Strat
from Bio.PDB import *
from utils import *
import math


def add_optional_cmd_args(values, tag):
    """
    Addes a set of optional arguements to a list of command line 
    arguements for the program.
    
    :param values: The values entered in the GUI fileds
    :param cmd_args: A list of arguements for the program.
    :param tag: The tag for the cmd args
    :return: A list of the added optional args
    """
    cmd_args = []
    if values[tag].strip() != "":
        cmd_args += [tag]
        cmd_args += [values[tag].strip()]
    return cmd_args


def add_required_cmd_args(values, tag, name):
    """
    Addes a set of required arguements to a list of command line 
    arguements for the program.
    
    :param values: The values entered in the GUI fileds
    :param cmd_args: A list of arguements for the program.
    :param tag: The tag for the cmd args
    :param name: Item named used in popup window.
    :return: A list of the added required args
    """
    if values[tag].strip() == "":
        msg = name + " is Required"
        layout = [[sg.Text(msg)]]
        window = sg.Window(msg, layout, modal=True)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        # Exit  if error occured
        exit()
    cmd_args = [tag]
    cmd_args += [values[tag].strip()]
    return cmd_args


def add_required_filepath_cmd_args(values, tag, name):
    """
    Addes a set of filepath required arguements to a list of command line 
    arguements for the program.
    
    :param values: The values entered in the GUI fileds
    :param cmd_args: A list of arguements for the program.
    :param tag: The tag for the cmd args
    :param name: Item named used in popup window.
    :return: A list of the added required args
    """
    if values[tag].strip() == "":
        msg = name + " is Required"
        layout = [[sg.Text(msg)]]
        window = sg.Window(msg, layout, modal=True)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        # Exit  if error occured
        exit()
    cmd_args = [tag]
    cmd_args += [values[tag].replace("/","\\").strip()]
    return cmd_args
    
    
def add_required_folderpath_cmd_args(values, tag, name):
    """
    Addes a set of dirpath required arguements to a list of command line 
    arguements for the program.
    
    :param values: The values entered in the GUI fileds
    :param cmd_args: A list of arguements for the program.
    :param tag: The tag for the cmd args
    :param name: Item named used in popup window.
    :return: A list of the added required args
    """
    if values[tag].strip() == "":
        msg = name + " is Required"
        layout = [[sg.Text(msg)]]
        window = sg.Window(msg, layout, modal=True)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        # Exit  if error occured
        exit()
    cmd_args = [tag]
    path = values[tag].strip() + '/'
    cmd_args += [path.replace("/","\\")]
    return cmd_args
    
    
def check_multi_seq_fasta_args(values, err):
    """
    Checks the required arguements to compile a multisequence fasta file.
    
    :param values: Input values from the GUI.
    :param err: Boolean value for indicating if an error occured.
    :return: List of values for gui.
    :return: Boolean value indicating if an error occured.
    """
    values['--seq_type'] = 'aa' 
    # Source genome annotation
    if values['--src'].strip() == "":
        sg.popup("Input Genome Annotation is required")
        err = True
    elif values['--src'].split(".")[-1] != "xlsx":
        sg.popup("Input Genome Annotation must be a .xlsx file")
        err = True
    values['--src'] = values['--src'].replace("/","\\").strip()
    # Destination filename
    if values['--dest'] == '':
        sg.popup("Destination file is required")
        err = True
    # Destination folder
    if values['--outDir'] == '':
        sg.popup("Folder for Destination file is required")
        err = True
    dest = values['--outDir'] + '/' + values['--dest']
    values['--dest'] = dest.replace("/","\\")
    # Optional keywords argument
    values['--keywords'] = values['--keywords'].strip()
    return values, err
    
      
def check_protein_modeling_args(values, err):
    """
    Checks the required arguements to run protein modeling.
    
    :param values: Input values from the GUI.
    :param err: Boolean value for indicating if an error occured.
    :return: List of values for gui.
    :return: Boolean value indicating if an error occured.
    """
    # Source genome annotation
    if values['-query_parallel'].strip() == "":
        sg.popup("Input fasta file is required")
        err = True
    values['-query_parallel'] = values['-query_parallel'].replace("/","\\").strip()
    # Destination folder
    if values['-db'] == '':
        sg.popup("Path to pdbaa database is required")
        err = True
    dest = values['-db'] + '/' + "pdbaa"
    values['-db'] = dest.replace("/","\\")
    return values, err
            
        
def cmpl_mult_seq_fasta(df, rows, seq_col, loc_col):
    """
    Parses a genome annotation excel file sequences to add to a multisequence 
    fasta file.
    
    :param df: The Pandas dataframe to process
    :param rows: A set of rows to progress from df
    :param seq_col: Column containing the aa sequence.
    :param loc_col: Column containing the ids for proteins
    :return: String of the fasta file to write
    """
    ids = {}
    seq = ""
    fasta = ""
    # Compile the fasta sequences
    for row in rows:
        seq = df[seq_col][row]
        seq_id = ""
        # Check is the sequence ID is unique or not
        if df[loc_col][row] in ids.keys():  
            # If not unique, then make it unique
            c = ids[df[loc_col][row]]['count']
            seq_id = df[loc_col][row] + "(" + str(c) + ")"
            ids[df[loc_col][row]]['count'] += 1
        else:
            seq_id = df[loc_col][row]
            ids[df[loc_col][row]] = {
                                        "id" : df[loc_col][row],
                                        "count" : 1
                                    }
        # Add to fasta file as a string
        try:
            if type(seq) == type("str"):
                fasta += ">" + str(seq_id) + "\n" + str(seq) + "\n\n"                
        except Exception as e:
            print(e)
    return fasta
    
    
def multi_seq_fasta():
    """
    Used to specify parameters for the compilation of a multisequence fasta file.
    """
    layout =    [
                    [sg.Text('Compile Multisequence Fasta File', size=(35, 1), \
                    justification='center', font=("Helvetica", 25), \
                    relief=sg.RELIEF_RIDGE)], 
                    [sg.Text("")],
                    [sg.Text('Select RAST Genome Annotation'), \
                    sg.InputText(key='--src'), sg.FileBrowse()],
                    [sg.Text('Keywords')] + [sg.Input(key='--keywords')],
                    [sg.Text("Include Rows with EC Numbers Present?"), \
                    sg.InputOptionMenu(["Yes","No"], default_value="Yes", key="-include_ec-")],
                    [sg.Text('Output Fasta Filename')] \
                        + [sg.Input(key='--dest')],
                    [sg.Text('Destinatin Folder for Output Fasta File'), \
                        sg.InputText(key='--outDir'), \
                        sg.FolderBrowse()],
                    [sg.Button("Go", key="compile_fasta")],
                ]
    window = sg.Window("Compile Multisequence Fasta File", layout, \
             resizable=True, finalize=True, modal=True)
    choice = None
    args = {}
    while True:
        err = False
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'compile_fasta':
            values, err = check_multi_seq_fasta_args(values, err)
            if not err:
                layout = [
                    [sg.Text('Compile Multisequence Fasta File', size=(35, 1), \
                    justification='center', font=("Helvetica", 25), \
                    relief=sg.RELIEF_RIDGE)], 
                    [sg.Text("")],
                    ]
                    
                filepath = values['--src']
                filename = filepath.split("\\")[-1]
                col_labels = read_header(filepath)
                menu_cols = tuple(col_labels)
                layout += [sg.Text("Selected Genome Annotation: " + filename \
                    + "\n", justification='left', font=("Helvetica", 12))], \
                    [sg.Text("Select Column Containing the Amino Acid Sequences"), \
                    sg.InputOptionMenu(menu_cols, key="protein col")], [sg.Text("")], 
                layout += [sg.Text("Select Column to Use for Identifying the Proteins"), \
                    sg.InputOptionMenu(menu_cols, key="id col")], [sg.Text("")],
                layout += [sg.Button("Go", key="Go")],
                
                window.close()
                window = sg.Window("Compile Multisequence Fasta File", layout, \
                        resizable=True, finalize=True, modal=True)
                while True:
                    event, values_2 = window.read()
                    if event == sg.WIN_CLOSED:
                        break
                    elif event == 'Go':
                        use_ec = False
                        if values["-include_ec-"] == "Yes":
                            use_ec = True
                        args =  {
                            '--src'                     : values['--src'],
                            '--dest'                    : values['--src'],
                            '--keywords'                : values['--keywords'],
                            '--visible'                 : False,
                            '--load_job'                : None,
                            '--email'                   : None, 
                            '--sheet'                   : 0,
                            '--min_pct_idnt'            : None,
                            '--min_qry_cvr'             : None,
                            '--max_blast_hits'          : None,
                            '--max_uniprot_hits'        : None,
                            '--from_downloaded_blast'   : False,
                            '--BLAST_rslts_path'        : None,
                            '--has_ec'                  : True
                        }  
                        # Read the excel file
                        df = pd.read_excel(args['--src']) 
                        kw = Annot_Reader.parse_keywords(args['--keywords'])
                        window.close()
                        rows = Annot_Reader.compile_rows(df, kw, True)
                        fasta = cmpl_mult_seq_fasta(df, rows, \
                            values_2['protein col'], values_2['id col'])
                        f = open(values['--dest'], 'w')
                        f.write(fasta.strip())
                        f.close()
                        sg.popup("Multi-sequence Fasta File has been Compilied")
                        window.close()
    window.close()
    
    
def protein_modeling(args):
    """
    Runs the protein modeling
    
    :param args: List of arguements
    """
    # Mark the Start Time
    start_time = time.time()
    # Create and init PSI_BLAST object
    psiblast = PSI_BLAST("ncbi-blast-2.12.0+/bin/psiblast.exe", args)
    # Compile command line arguments
    queries = PSI_BLAST.parse_fasta(psiblast.args['script_args']['-query_parallel'])
    # Run the PSI BLAST Algorithm
    blast_rslt_dir = 'blast_rslts\\'
    blast_working_dir = 'temp_blast\\'
    run_psi_blast(psiblast, queries, blast_rslt_dir, blast_working_dir) 
    pdb_dir = "pdb\\"
    align_dir = "align\\"
    # Run protein alignment
    align_files, templates = protein_alignment_gui(queries, blast_rslt_dir, pdb_dir, align_dir)
    # Delete pdb files
    shutil.rmtree(pdb_dir)
    # Delete blast results files
    shutil.rmtree(blast_rslt_dir)
    print("\n")
    # Run protein modeling
    protein_model_rslt_dir = 'protein_models'
    protein_modeling_gui(align_files, align_dir, protein_model_rslt_dir)
    print("\n")

    # Delete alignment files
    shutil.rmtree(align_dir)
    # Remove templates
    for temp in templates:
        if os.path.isfile(temp):
            os.remove(temp)

    tot_seconds = time.time() - start_time
    minutes = int(tot_seconds / 60.0)
    seconds = int(tot_seconds % 60.0)
    minute_str = "minutes"
    second_str = "seconds"
    if minutes == 1:
        minute_str = "minute"
    if seconds == 1:
        second_str = "second"
    print("---Runtime: " + str(minutes) + " " + minute_str + " and " \
        + str(seconds)  + " " + second_str + " ---")
    sg.popup("Protein Modeling is Complete!")
    
    
def protein_modeling_setup():
    """
    Runs gui version of the protein modeling.
    """
    layout =    [
                    [sg.Text('Protein Modeling', size=(35, 1), \
                    justification='center', font=("Helvetica", 25), \
                    relief=sg.RELIEF_RIDGE)], 
                    [sg.Text("")],
                    [sg.Text('Select FASTA File Containing Protein Sequences to Model'), \
                    sg.InputText(key='-query_parallel'), sg.FileBrowse()],
                    [sg.Text('Select Folder Containing the pdbaa Database'), \
                        sg.InputText(key='-db'), \
                        sg.FolderBrowse()],
                    [sg.Button("Go", key="-model_proteins-")],
                ]
    window = sg.Window("Protein Modeling", layout, \
             resizable=True, finalize=True, modal=True)
    choice = None
    args = {}
    while True:
        err = False
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-model_proteins-':
            values, err = check_protein_modeling_args(values, err)
            if not err:
                args = ['trash']
                for key in values.keys():
                    args += [key]
                    args += [values[key]]
                window.close()
                protein_modeling(args)
                
    window.close()
    
    
def main():
    """
    This is the main window which is the start of the program.
    """
    # Define the layout of the main window
    layout =    [
                    [sg.Text('Bulk Protein Modeling', size=(20, 1), \
                    justification='center', font=("Helvetica", 25), \
                    relief=sg.RELIEF_RIDGE)], 
                    [sg.Button("Protein Modeling", \
                               key="protein_modeling")],
                    [sg.Button("Compile Multisequence Fasta File", \
                               key="multi_seq_fasta")],
                ]
    window = sg.Window('Bulk Protein Modeling', layout, resizable=True, finalize=True)
    # Loop for the main window
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == 'Configure':
            if window.TKroot.state() == 'zoomed':
                status.update(value='Window zoomed and maximized !')
            else:
                status.update(value='Window normal')
        elif event == "multi_seq_fasta":
            window.close()
            multi_seq_fasta()
        elif event == "protein_modeling":
            window.close()
            protein_modeling_setup()
        
    window.close()
    
    
if __name__ == "__main__":
    main()