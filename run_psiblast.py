import sys, os, time
import shutil     
from classes.PSI_BLAST import PSI_BLAST
from run_psiblast_utils import *
    

blast_rslt_dir = 'blast_rslts\\'
blast_working_dir = 'temp_blast\\'
commands = []

psiblast = PSI_BLAST("ncbi-blast-2.12.0+/bin/psiblast.exe", sys.argv)

# Determine if help was specified
if '-h' in psiblast.args['blast_args'].keys():
    usage()
elif '-help' in psiblast.args['blast_args'].keys():
    usage()
    if '-program' in psiblast.args['script_args'].keys():
        print("\nUsage and help for NCBI psiblast program:")
        Popen([psiblast.args['script_args']['-program'], '-help'])
    exit()

# Compile command line arguments
commands = psiblast.compile_cmd(psiblast.args, blast_rslt_dir, blast_working_dir)

start_time = time.time()
psiblast.exec_commands(commands)
if os.path.isdir(blast_working_dir):
    shutil.rmtree(blast_working_dir)
print("---%s seconds ---" % (time.time() - start_time))