import sys, os, time
import shutil     
from classes.PSI_BLAST import PSI_BLAST
from run_psiblast_utils import *
from classes.BLAST_Rslts_Itr import BLAST_Rslts_Itr
from classes.strategy import Outfmt_0_Strat
from Bio.PDB import *
from modeller import *
from subprocess import Popen, list2cmdline
from utils import *
from progress.bar import IncrementalBar
    
# Mark the Start Time
start_time = time.time()
# Define filepaths to working and results directory for the PSI BLAST algorithm
blast_rslt_dir = 'blast_rslts\\'
blast_working_dir = 'temp_blast\\'

######################### Run the PSI BLAST Algorithm #########################
# Create and init PSI_BLAST object
psiblast = PSI_BLAST("ncbi-blast-2.12.0+/bin/psiblast.exe", sys.argv)
# Check that the required commmand line arguements were passed in
check_cmd_args(psiblast.args)
# Compile command line arguments
queries = PSI_BLAST.parse_fasta(psiblast.args['script_args']['-query_parallel'])
# Compile the commands line commands to run the PSI algorithm 
commands = psiblast.compile_cmd(psiblast.args, blast_rslt_dir, blast_working_dir)
#Execute the commands
psiblast.exec_commands(commands)
# Remove the Working Directory for the PSI BLAST Algorithm
if os.path.isdir(blast_working_dir):
    shutil.rmtree(blast_working_dir)
###############################################################################
    
print("\n")

pdb_dir = "pdb\\"
pdbdownload = PDBList()

tasks = []
align_files = []
# Count the number of queries to perform protein modeling on
num_queries = 0
for file in os.listdir(blast_rslt_dir):
    if file.split(".")[0] in queries:
        num_queries += 1
        
bar = IncrementalBar('| Collecting Files for Alignment...\t', max = num_queries)

for file in os.listdir(blast_rslt_dir):
    if file.split(".")[0] in queries:
        seq = queries[file.split(".")[0]]
        # Read the file
        with open(blast_rslt_dir + file) as f:
            content = f.read()
        path = blast_rslt_dir + file

        acc = None
        for protein in iter(BLAST_Rslts_Itr(content, path)):
            acc = protein['accession'][:protein['accession'].find("_")]
            break
        if acc is not None:
            #downloaded_path = pdbdownload.retrieve_pdb_file(acc, file_format="pdb", pdir=pdb_dir + acc, overwrite=True)
            for file in os.listdir(pdb_dir + acc):
                src = pdb_dir + acc + "\\" + file
                dest = acc + ".pdb"
                if not os.path.isfile(dest):
                    shutil.copy(src , dest)
                os.remove(src)
                break
                
            bsali = ">P1;Bs\nsequence:Bs:::::::0.00: 0.00\n" + seq + "*"
            ali_filename = "bs_" + acc + ".ali"
            f = open(ali_filename, "w")
            f.write(bsali)
            f.close()
            template_path = acc + ".pdb"
            task = ['py', 'align2d.py', acc, template_path, ali_filename]
            tasks += [task]
        bar.next()

print("\n")
exec_commands(tasks, '| Aligning Proteins...\t')

print("\n")

print("---Runtime: %s seconds ---" % (time.time() - start_time))