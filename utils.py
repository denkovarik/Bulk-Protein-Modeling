import sys, os, time
from subprocess import Popen, list2cmdline
import shutil
from progress.bar import IncrementalBar
import pandas as pd
from Bio.PDB import *
from classes.BLAST_Rslts_Itr import BLAST_Rslts_Itr
from classes.strategy import Outfmt_0_Strat
import PySimpleGUI as sg


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
    cur_job = 0
    num_jobs = len(cmds)
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
            
            
def exec_commands_gui(cmds, msg = '| Running Commands'):
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
    cur_job = 0
    num_jobs = len(cmds)
    sg.OneLineProgressMeter(msg, cur_job, num_jobs, msg)
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
                    cur_job += 1
                    sg.OneLineProgressMeter(msg, cur_job, num_jobs, msg)
                    bar.next()
                else:
                    fail()

        if not processes and not cmds:
            break
        else:
            time.sleep(0.05)
            
            
def protein_alignment(queries, blast_rslt_dir, pdb_dir, align_dir):
    """
    Downloads the pdb template proteins and performs protein alignment.
    
    :param queries: Dictionary of queries consisting of sequences identified 
                    by their name as the keys.
    :param blast_rslt_dir: Directory storing the BLAST results
    :param pdb_dir: Directory to place the pdb template proteins in
    :param align_dir: Directory to place the aligned protein files in
    :return: List of tuples containing the accession of the template protein 
             that was aligned and the produced files from the protein alignment.
    :return: List template protein filepaths
    """
    # Create directory to store pdb template proteins
    if not os.path.isdir(pdb_dir):
        os.mkdir(pdb_dir)
    # Create directory to store the files produced from the alignment algorithm
    if not os.path.isdir(align_dir):
        os.mkdir(align_dir)
    pdbdownload = PDBList()
    tasks = []
    align_files = []
    # Count the number of queries to perform protein modeling on
    num_queries = 0
    for file in os.listdir(blast_rslt_dir):
        if file.split(".")[0] in queries:
            num_queries += 1           
    bar = IncrementalBar('| Collecting Files for Alignment...\t', max = num_queries)
    orig = sys.stdout
    log_file = open(os.devnull, "w")
    sys.stdout = log_file   
    templates = []
    for file in os.listdir(blast_rslt_dir):
        if file.split(".")[0] in queries:
            seq_id = file.split(".")[0]
            seq = queries[seq_id]
            # Read the file
            with open(blast_rslt_dir + file) as f:
                content = f.read()
            path = blast_rslt_dir + file
            acc = None
            try:
                for protein in iter(BLAST_Rslts_Itr(content, path)):
                    acc = protein['accession'][:protein['accession'].find("_")]
                    break
                # Download the pdb file
                if acc is not None:
                    sys.stdout = log_file
                    downloaded_path = pdbdownload.retrieve_pdb_file(acc, file_format="pdb", pdir=pdb_dir + acc, overwrite=True)
                    sys.stdout = orig
                    for file in os.listdir(pdb_dir + acc):
                        src = pdb_dir + acc + "\\" + file
                        dest = acc + ".pdb"
                        if not os.path.isfile(dest):
                            shutil.copy(src , dest)
                        os.remove(src)
                        break
                        
                    bsali = ">P1;Bs\nsequence:Bs:::::::0.00: 0.00\n" + seq + "*"
                    ali_file = "Bs-" + acc + "A.ali"
                    f = open(ali_file, "w")
                    f.write(bsali)
                    f.close()
                    template_path = acc + ".pdb"
                    templates += [template_path]
                    task = ['py', 'align2d.py', acc, template_path, ali_file]
                    tasks += [task]
                    pap_file = 'align\\Bs-' + acc + 'A.pap'
                    align_files += [(acc, ali_file, pap_file, seq_id)]
            except:
                pass
            bar.next()          
    print("\n")
    exec_commands(tasks, '| Aligning Proteins...\t')
    return align_files, templates
    
    
def protein_alignment_gui(queries, blast_rslt_dir, pdb_dir, align_dir):
    """
    Downloads the pdb template proteins and performs protein alignment.
    
    :param queries: Dictionary of queries consisting of sequences identified 
                    by their name as the keys.
    :param blast_rslt_dir: Directory storing the BLAST results
    :param pdb_dir: Directory to place the pdb template proteins in
    :param align_dir: Directory to place the aligned protein files in
    :return: List of tuples containing the accession of the template protein 
             that was aligned and the produced files from the protein alignment.
    :return: List template protein filepaths
    """
    # Create directory to store pdb template proteins
    if not os.path.isdir(pdb_dir):
        os.mkdir(pdb_dir)
    # Create directory to store the files produced from the alignment algorithm
    if not os.path.isdir(align_dir):
        os.mkdir(align_dir)
    pdbdownload = PDBList()
    tasks = []
    align_files = []
    # Count the number of queries to perform protein modeling on
    num_queries = 0
    for file in os.listdir(blast_rslt_dir):
        if file.split(".")[0] in queries:
            num_queries += 1           
    bar = IncrementalBar('| Collecting Files for Alignment...\t', max = num_queries)
    orig = sys.stdout
    log_file = open(os.devnull, "w")
    sys.stdout = log_file   
    templates = []
    i = 0
    for file in os.listdir(blast_rslt_dir):
        if file.split(".")[0] in queries:
            title = "Downloading Template Proteins"
            msg = 'Downloading Template Protein for ' + file.split(".")[0] + "..."
            sg.OneLineProgressMeter(title, i, num_queries, msg)
            i += 1            
            seq_id = file.split(".")[0]
            seq = queries[seq_id]
            # Read the file
            with open(blast_rslt_dir + file) as f:
                content = f.read()
            path = blast_rslt_dir + file
            acc = None
            try:
                for protein in iter(BLAST_Rslts_Itr(content, path)):
                    acc = protein['accession'][:protein['accession'].find("_")]
                    break
                # Download the pdb file
                if acc is not None:
                    sys.stdout = log_file
                    downloaded_path = pdbdownload.retrieve_pdb_file(acc, file_format="pdb", pdir=pdb_dir + acc, overwrite=True)
                    sys.stdout = orig
                    for file in os.listdir(pdb_dir + acc):
                        src = pdb_dir + acc + "\\" + file
                        dest = acc + ".pdb"
                        if not os.path.isfile(dest):
                            shutil.copy(src , dest)
                        os.remove(src)
                        break
                        
                    bsali = ">P1;Bs\nsequence:Bs:::::::0.00: 0.00\n" + seq + "*"
                    ali_file = "Bs-" + acc + "A.ali"
                    f = open(ali_file, "w")
                    f.write(bsali)
                    f.close()
                    template_path = acc + ".pdb"
                    templates += [template_path]
                    task = ['py', 'align2d.py', acc, template_path, ali_file]
                    tasks += [task]
                    pap_file = 'align\\Bs-' + acc + 'A.pap'
                    align_files += [(acc, ali_file, pap_file, seq_id)]
            except:
                pass
            bar.next()
    sg.OneLineProgressMeter(title, i, num_queries, "Finished!")
    print("\n")
    exec_commands_gui(tasks, 'Aligning Proteins...')
    return align_files, templates
    
    
def protein_modeling(align_files, align_dir, protein_model_rslt_dir):
    """
    Performs high volume protein modeling.
    
    :param align_files: List of tuples containing the accession of the template 
                        protein that was aligned and the produced files from 
                        the protein alignment.
    :param align_dir: Directory containing the alignment files
    :param protein_model_rslt_dir: Directory to store the modeled proteins.
    """
    if not os.path.isdir(protein_model_rslt_dir):
        os.mkdir(protein_model_rslt_dir)
    num_alignments = 0
    tasks = []
    for entry in align_files:
        if entry[1][entry[1].rfind("\\") + 1:] in os.listdir(align_dir):
            task = ['py', 'model-single.py', '-knowns', entry[0]+"A", \
                '-ali_path', align_dir + entry[1], '-results_dir', \
                protein_model_rslt_dir, '-template_path', entry[0] + ".pdb", \
                '-target_id', entry[3]]
            tasks += [task]
            num_alignments += 1
            
    exec_commands(tasks, '| Modeling Proteins...\t')
    
    
def protein_modeling_gui(align_files, align_dir, protein_model_rslt_dir):
    """
    Performs high volume protein modeling.
    
    :param align_files: List of tuples containing the accession of the template 
                        protein that was aligned and the produced files from 
                        the protein alignment.
    :param align_dir: Directory containing the alignment files
    :param protein_model_rslt_dir: Directory to store the modeled proteins.
    """
    if not os.path.isdir(protein_model_rslt_dir):
        os.mkdir(protein_model_rslt_dir)
    num_alignments = 0
    tasks = []
    for entry in align_files:
        if entry[1][entry[1].rfind("\\") + 1:] in os.listdir(align_dir):
            task = ['py', 'model-single.py', '-knowns', entry[0]+"A", \
                '-ali_path', align_dir + entry[1], '-results_dir', \
                protein_model_rslt_dir, '-template_path', entry[0] + ".pdb", \
                '-target_id', entry[3]]
            tasks += [task]
            num_alignments += 1
            
    exec_commands_gui(tasks, 'Modeling Proteins...')
       
            
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
    
    
def run_psi_blast(psiblast, queries, blast_rslt_dir, blast_working_dir):
    """
    Runs the PSI BLAST algorithm
    
    :param psiblast: A PSI_BLAST object to run the PSI BLAST algorithm
    :param queries: Dictionary of queries consisting of sequences identified 
                    by their name as the keys.
    :param blast_rslt_dir: Directory to store the BLAST results
    :param blast_working_dir: Temp working directory for BLAST algorithm.
    """
    # Compile the commands line commands to run the PSI algorithm 
    commands = psiblast.compile_cmd(psiblast.args, blast_rslt_dir, blast_working_dir)
    #Execute the commands
    psiblast.exec_commands(commands)
    # Remove the Working Directory for the PSI BLAST Algorithm
    if os.path.isdir(blast_working_dir):
        shutil.rmtree(blast_working_dir)
        
     
def run_psi_blast_gui(psiblast, queries, blast_rslt_dir, blast_working_dir):
    """
    Runs the PSI BLAST algorithm for the gui version
    
    :param psiblast: A PSI_BLAST object to run the PSI BLAST algorithm
    :param queries: Dictionary of queries consisting of sequences identified 
                    by their name as the keys.
    :param blast_rslt_dir: Directory to store the BLAST results
    :param blast_working_dir: Temp working directory for BLAST algorithm.
    """
    # Compile the commands line commands to run the PSI algorithm 
    commands = psiblast.compile_cmd(psiblast.args, blast_rslt_dir, blast_working_dir)
    #Execute the commands
    msg = "Running PSI BLAST Algorithm..."
    psiblast.exec_commands_gui(commands, msg)
    # Remove the Working Directory for the PSI BLAST Algorithm
    if os.path.isdir(blast_working_dir):
        shutil.rmtree(blast_working_dir)