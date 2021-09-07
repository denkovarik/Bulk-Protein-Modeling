import sys, os, time
from subprocess import Popen, list2cmdline
import shutil
from progress.bar import IncrementalBar
import pandas as pd


def check_cmd_args(args):
    """
    Checks that the required command line arguments where passed into the
    function.
    
    :param args: The command line arguements as a dictionary
    """
    # Determine if help was specified
    if '-help' in args['blast_args'].keys():
        usage()
        if '-program' in args['script_args'].keys():
            print("\nUsage and help for NCBI psiblast program:")
            Popen([args['script_args']['-program'], '-help'])
        exit()
    elif '-h' in args['blast_args'].keys():
        usage()
        exit()

    # Make sure the required command line arguements where entered.
    if not '-query_parallel' in args['script_args'].keys():
        err = "Command line argument '-query_parallel' must be specified to\n"
        err += "identify the fasta file containing the sequences to run the\n"
        err += "protein modeling on.\n"
        print(err)
        usage()
        exit()
    elif not '-db' in args['blast_args'].keys():
        err = "Command line argument '-db' must be specified to\n"
        err += "identify the database to use for BLAST."
        print(err)
        usage()
        exit()
        
        
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
        if reader.df[loc_col][row] in ids.keys():
            c = ids[reader.df[loc_col][row]]['count']
            seq_id = reader.df[loc_col][row] + "(" + str(c) + ")"
            ids[reader.df[loc_col][row]]['count'] += 1
        else:
            seq_id = reader.df[loc_col][row]
            ids[reader.df[loc_col][row]] =  {
                                                "id" : reader.df[loc_col][row],
                                                "count" : 1
                                            }
        fasta += ">" + seq_id + "\n" + seq + "\n\n"
    return fasta
    
    
def cpu_count():
    ''' 
    Returns the number of CPUs in the system
    '''
    num = 1
    if sys.platform == 'win32':
        try:
            num = int(os.environ['NUMBER_OF_PROCESSORS'])
        except (ValueError, KeyError):
            pass
    elif sys.platform == 'darwin':
        try:
            num = int(os.popen('sysctl -n hw.ncpu').read())
        except ValueError:
            pass
    else:
        try:
            num = os.sysconf('SC_NPROCESSORS_ONLN')
        except (ValueError, OSError, AttributeError):
            pass

    return num
        
        
def exec_commands(cmds, msg = '| Running Commands'):
    ''' Exec commands in parallel in multiple process 
    (as much as we have CPU)
    '''
    if not cmds: return # empty list

    def done(p):
        return p.poll() is not None
    def success(p):
        return p.returncode == 0
    def fail():
        sys.exit(1)

    max_task = cpu_count()
    processes = []
    bar = IncrementalBar(msg, max = len(cmds))
    while True:
        while cmds and len(processes) < max_task:
            task = cmds.pop()
            with open(os.devnull, 'w') as fp:
                processes.append((Popen((task), stdout=fp)))

        for p in processes:
            if done(p):
                if success(p):
                    processes.remove(p)
                    bar.next()
                else:
                    fail()

        if not processes and not cmds:
            break
        else:
            time.sleep(0.05)
            
            
def read_header(filepath):
    """
    Reads the header of a genome annotation and returns the column names as a 
    list.
    
    :param filepath: Filepath to the genome annotation
    :return: A list of the column names
    """  
    col_labels = []
    excel_data_df = pd.read_excel(filepath)
    for col in excel_data_df.columns:
        col_labels += [col]
    return col_labels