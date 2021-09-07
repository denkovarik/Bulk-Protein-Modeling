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


def build_cmd_args_dwnl_BLAST(values, event):
    """
    Builds a list of command line arguements needed for the program
    
    :param values: The values entered into the GUI fields
    :param event: The events that happened in the GUI.
    :return: A list of command line arguements needed for the program.
    """
    cmd_args = ['ec_scrape_gui.py']
    # Source file
    tag = '--src'
    name = 'Source RAST Genome Annotation '
    cmd_args += add_required_filepath_cmd_args(values, tag, name)
    # Destination file
    if values['--dest'] == '':
        layout = [[sg.Text("Destination file is required", font=32)]]
        window = sg.Window("Destination file is required", layout, \
                 modal=True)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        exit()
    if values['--dest'].split('.')[-1] != 'xlsx':
        layout = [[sg.Text("Destination file must be a .xlsx file", font=32)]]
        window = sg.Window("Destination file must be a .xlsx file", layout, \
                 modal=True)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        exit()
    dest = values['--dest']
    cmd_args += ['--dest']
    cmd_args += [dest.replace("/","\\")]
    # Email
    tag = '--email'
    name = "Email "
    cmd_args += add_required_cmd_args(values, tag, name)
    # Optional keywords argument
    tag = '--keywords'
    cmd_args += add_optional_cmd_args(values, tag)
    # Optional Min Query Cover Arg
    tag = '--min_qry_cvr'
    cmd_args += add_optional_cmd_args(values, tag)
    # Optional Min Per. Ident
    tag = '--min_pct_idnt'
    cmd_args += add_optional_cmd_args(values, tag)
    # Optional Max Blast Hits to Use Arg
    tag = '--max_blast_hits'
    cmd_args += add_optional_cmd_args(values, tag)
    # Optional Max Uniprot Hits to Use Arg
    tag = '--max_uniprot_hits'
    cmd_args += add_optional_cmd_args(values, tag)
    cmd_args += ['--from_downloaded_blast']
    cmd_args += ['True']
    # BLAST results path
    tag = '--BLAST_rslts_path'
    name = 'Path to BLAST results file '
    cmd_args += add_required_folderpath_cmd_args(values, tag, name)
    return cmd_args
    
    
def build_cmd_args_online_BLAST(values, event):
    """
    Builds a list of command line arguements needed for the program
    
    :param values: The values entered into the GUI fields
    :param event: The events that happened in the GUI.
    :return: A list of command line arguements needed for the program.
    :return: None if an error occured.
    """
    cmd_args = ['ec_scrape_gui.py']
    # Blast program to used
    if values['--program'].strip() == '':
        sg.popup("BLAST Program is required")
        return None
    cmd_args += ['--program']
    cmd_args += [values['--program'].strip()]
    # Source file
    if values['--src'].strip() == "":
        sg.popup("Input RAST Genome Annotation is required")
        return None
    cmd_args += ['--src']
    cmd_args += [values['--src'].replace("/","\\").strip()]
    # Destination filename
    if values['--dest'] == '':
        sg.popup("Destination file is required")
        return None
    # Check for correct file extension
    if values['--dest'].split('.')[-1] != 'xlsx':
        sg.popup("Destination file must be a .xlsx file")
        return None
    # Destination folder
    if values['--outDir'] == '':
        sg.popup("Folder for Destination file is required")
        return None
    dest = values['--outDir'] + '/' + values['--dest']
    cmd_args += ['--dest']
    cmd_args += [dest.replace("/","\\")]
    # Email
    if values['--email'].strip() == '':
        sg.popup("User email is required")
        return None
    cmd_args += ['--email']
    cmd_args += [values['--email']]
    # Optional keywords argument
    if values['--keywords'].strip() != "":
        cmd_args += ['--keywords']
        cmd_args += [values['--keywords'].strip()] 
    # Optional Number of Threads Arg
    cmd_args += ['--num_threads']
    cmd_args += [values['--num_threads']]
    # Optional Min Query Cover Arg
    cmd_args += ['--min_qry_cvr']
    cmd_args += [values['--min_qry_cvr']]
    # Optional Min Per. Ident
    cmd_args += ['--min_pct_idnt']
    cmd_args += [values['--min_pct_idnt']]
    # Optional Max Blast Hits to Use Arg
    cmd_args += ['--max_blast_hits']
    cmd_args += [int(values['--max_blast_hits'])]
    # Optional Max Uniprot Hits to Use Arg
    cmd_args += ['--max_uniprot_hits']
    cmd_args += [int(values['--max_uniprot_hits'])]
    return cmd_args
    
    
def build_ec_scrape_via_dwnl_blast_rslt_layout():
    """
    Builds the layout of the window for ec_scrape_via_dwnl_blast_rslt().
    
    :return: The layout for the ec_scrape_via_dwnl_blast_rslt() window.
    """
    delim2 = '-----------------------------------------------------------------'
    delim2 += '----------------------------------------------------------------'
    delim2 += '-----------------------------'
    delim = '================================================================='
    delim += '=========================='
    layout = [
                [sg.Text("EC-Scrape via Downloaded BLAST Results")],
                [sg.Text(delim)],
                [sg.Text("Required Parameters")],
                [sg.Text(delim2)],
                [sg.Text('Select Input RAST Genome Annotation'), \
                    sg.InputText(key='--src'), sg.FileBrowse()],
                [sg.Text('Filename for RAST Genome Annotation to Write')] \
                    + [sg.Input(key='--dest')],
                [sg.Text('Select Folder Holding Downloaded BLAST Results'), \
                    sg.InputText(key='--BLAST_rslts_path'), \
                    sg.FolderBrowse()],
                [sg.Text('Email')] + [sg.Input(key='--email')],
                [sg.Text("\nOptional Parameters")],
                [sg.Text(delim2)],
                [sg.Text('Keywords')] + [sg.Input(key='--keywords')],
                [sg.Text('Min Query Cover')] \
                    + [sg.Input(key='--min_qry_cvr')],
                [sg.Text('Min Per. Ident')] \
                    + [sg.Input(key='--min_pct_idnt')],
                [sg.Text('Max BLAST Hits')] \
                    + [sg.Input(key='--max_blast_hits')],
                [sg.Text('Max Uniprot Hits')] \
                    + [sg.Input(key='--max_uniprot_hits')],
                [sg.Button("Go", key="go_dwnl_ec")],                    
             ]
    return layout

    
def build_ec_scrape_via_online_blast_rslt_layout():
    """
    Builds the layout of the window for ec_scrape_via_dwnl_blast_rslt().
    
    :return: The layout for the ec_scrape_via_dwnl_blast_rslt() window.
    """
    delim2 = '-----------------------------------------------------------------'
    delim2 += '----------------------------------------------------------------'
    delim2 += '-----------------------------'
    delim = '================================================================='
    delim += '=========================='
    # ------ Menu Definition ------ #      
    
    layout = [
        [sg.Text('EC-Scrape via Online BLAST', size=(35, 1), \
            justification='center', font=("Helvetica", 25), \
            relief=sg.RELIEF_RIDGE)],   
        [sg.Text('Required Parameters', justification='left', \
            font=("Helvetica", 15))], 
        [sg.Text('Select BLAST Program'), \
            sg.InputOptionMenu(('blastx', 'blastp'), key='--program')],
        [sg.Text('Input RAST Genome Annotation'), \
            sg.InputText(key='--src'), sg.FileBrowse()],
        [sg.Text('Output RAST Genome Annotation Filename')] \
            + [sg.Input(key='--dest')],
        [sg.Text('Output RAST Genome Annotation Folder'), \
            sg.InputText(key='--outDir'), \
            sg.FolderBrowse()],
        [sg.Text('Email')] + [sg.Input(key='--email')],
        [sg.Text('')],
        [sg.Text('Optional Parameters', justification='left', \
            font=("Helvetica", 15))], 
        [sg.Text('Keywords')] + [sg.Input(key='--keywords')],
        [sg.Text('\nNumber of Threads')] +  [sg.Slider(range=(1, 50),\
            orientation='h', size=(34, 20), default_value=1, \
            key='--num_threads')],
        [sg.Text('\nMin Query Cover')] +  [sg.Slider(range=(0, 100),\
            orientation='h', size=(34, 20), default_value=90, \
            key='--min_qry_cvr')],
        [sg.Text('\nMin Per. Ident')] + [sg.Slider(range=(0, 100), \
            orientation='h', size=(34, 20), default_value=98, \
            key='--min_pct_idnt')],
        [sg.Text('\nMax BLAST Hits')] + [sg.Slider(range=(1, 50), \
            orientation='h', size=(34, 20), default_value=5, \
            key='--max_blast_hits')],
        [sg.Text('\nMax Uniprot Hits')] + [sg.Slider(range=(1, 50), \
            orientation='h', size=(34, 20), default_value=5, \
            key='--max_uniprot_hits')],
        [sg.Button("Go", key="go_online_ec")],]
    return layout  
    
    
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
                    
                    
def create_new_job():
    """
    Creates a new job for EC-Scrape via online BLAST queries.
    """
    layout = build_ec_scrape_via_online_blast_rslt_layout()
    window = sg.Window("EC-Scrape via Online BLAST Results", \
        layout, resizable=True, \
        finalize=True, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "go_online_ec":
            # Compile arguements for program
            cmd_args = build_cmd_args_online_BLAST(values, event)
            if cmd_args is not None:
                window.close()
                args = parse_args_ec_scrape(cmd_args)
                # Annot_Reader class to read and write to genome annotation
                reader = Annot_Reader(args)
                online_blast_ec_scrape(reader, args)
                msg = "EC-Scrape from Online BLAST Results has Completed"
                sg.popup(msg)


def ec_scrape_via_dwnl_blast_rslt():
    """
    Scrapes online databases for EC numbers for proteins from downloaded BLAST 
    results.
    """
    delim3 = '================================================================'
    layout = build_ec_scrape_via_dwnl_blast_rslt_layout()
    window = sg.Window("EC-Scrape via Downloaded BLAST Results", layout, resizable=True, \
             finalize=True, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "go_dwnl_ec":
            window.close()
            # Compile arguements for program
            cmd_args = build_cmd_args_dwnl_BLAST(values, event)
            args = parse_args_ec_scrape(cmd_args)
            # Annot_Reader class to read and write to genome annotation
            reader = Annot_Reader(args)
            # Check for necessary command line arguments
            check_dl_blast_args(args)
            # Build a dictionary mapping proteins by contig location
            loc2row = {}
            for ind in reader.df.index:
                loc = reader.df['location'][ind]
                loc2row[loc] = ind
            # Parse results in --BLAST_rslts_path
            num_rslts = len(os.listdir(args['--BLAST_rslts_path']))
            bar = IncrementalBar('| Processing Downloaded BLAST Results...', \
                    max = num_rslts)
            i = 0
            ec_added = 0
            for file in os.listdir(args['--BLAST_rslts_path']):
                if dl_blast_prcs_hit(file, reader, args, loc2row):
                    ec_added += 1
                sg.OneLineProgressMeter('Processing BLAST Results...', i + 1, \
                        num_rslts, 'Processing Downloaded BLAST Results...')
                bar.next()
                i += 1
            layout =    [
                            [sg.Text("EC-Scrape from Downloaded BLAST Results has Completed")],
                            [sg.Text("EC Numbers were Found for an Additional " \
                                    + str(ec_added) + " Proteins")],
                            [sg.Button("Quit", \
                                key="quit")],
                        ]
            window = sg.Window("Complete", layout, modal=True)
            while True:
                event, values = window.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                elif event == "quit":
                    window.close()


def ec_scrape_via_online_blast():
    """
    Scrapes online databases for EC numbers for proteins from BLAST query 
    results submitted online.
    """
    layout =    [
                    [sg.Text("EC-Scrape via Online BLAST", font=32)],
                    [sg.Button("New Job", key="new")],
                    [sg.Button("Load Job", key="new")],
                ]
    window = sg.Window("EC-Scrape via Online BLAST", layout, \
             resizable=True, finalize=True, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == 'new':
            window.close()
            create_new_job()
        
    window.close()
    
    
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
                        }  
                        reader = Annot_Reader(args)
                        window.close()
                        fasta = cmpl_mult_seq_fasta(reader, \
                            values_2['protein col'], values_2['id col'])
                        f = open(values['--dest'], 'w')
                        f.write(fasta.strip())
                        f.close()
                        sg.popup("Multi-sequence Fasta File has been Compilied")
                        window.close()
        
    window.close()
    
    
        
        
def cmpl_mult_seq_fasta(reader, seq_col, loc_col):
    """
    Parses a genome annotation excel file sequences to add to a multisequence 
    fasta file.
    
    :param reader: An instance of the Annot_Reader class.
    :param seq_col: Column containing the aa sequence.
    :param loc_col: Column containing the ids for proteins
    :return: String of the fasta file to write
    """
    ids = {}
    seq = ""
    fasta = ""
    for row in reader.rows:
        seq = reader.df[seq_col][row]
        seq_id = ""
        # Check is the sequence ID is unique or not
        if reader.df[loc_col][row] in ids.keys():  
            # If not unique, then make it unique
            c = ids[reader.df[loc_col][row]]['count']
            seq_id = reader.df[loc_col][row] + "(" + str(c) + ")"
            ids[reader.df[loc_col][row]]['count'] += 1
            print("not unique", end="")
            print("\t-\t" + str(seq_id))
        else:
            seq_id = reader.df[loc_col][row]
            ids[reader.df[loc_col][row]] =  {
                                                "id" : reader.df[loc_col][row],
                                                "count" : 1
                                            }
        # Add to fasta file as a string
        try:
            if type(seq) == type("str"):
                fasta += ">" + str(seq_id) + "\n" + str(seq) + "\n\n"                
        except Exception as e:
            print(e)
    return fasta
    
    
def main():
    """
    This is the main window which is the start of the program.
    """
    # Define the layout of the main window
    layout =    [
                    [sg.Text('Bulk Protein Modeling', size=(20, 1), \
                    justification='center', font=("Helvetica", 25), \
                    relief=sg.RELIEF_RIDGE)], 
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
        
    window.close()
    
    
if __name__ == "__main__":
    main()