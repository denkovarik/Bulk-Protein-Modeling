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
# Create and init PSI_BLAST object
psiblast = PSI_BLAST("ncbi-blast-2.12.0+/bin/psiblast.exe", sys.argv)
# Check that the required commmand line arguements were passed in
check_cmd_args(psiblast.args)
# Compile command line arguments
queries = PSI_BLAST.parse_fasta(psiblast.args['script_args']['-query_parallel'])

# Run the PSI BLAST Algorithm
blast_rslt_dir = 'blast_rslts\\'
blast_working_dir = 'temp_blast\\'
run_psi_blast(psiblast, queries, blast_rslt_dir, blast_working_dir)       
print("\n")


# Create directory for downloaded template files.
pdb_dir = "pdb\\"
align_dir = "align\\"
# Run protein alignment
align_files, templates = protein_alignment(queries, blast_rslt_dir, pdb_dir, align_dir)
# Delete pdb files
shutil.rmtree(pdb_dir)
# Delete blast results files
shutil.rmtree(blast_rslt_dir)
print("\n")

# Run protein modeling
protein_model_rslt_dir = 'protein_models'
protein_modeling(align_files, align_dir, protein_model_rslt_dir)
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