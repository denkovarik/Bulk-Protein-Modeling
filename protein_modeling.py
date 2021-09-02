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
    

blast_rslt_dir = 'blast_rslts\\'
blast_working_dir = 'temp_blast\\'
commands = []
# Create and init PSI_BLAST object
psiblast = PSI_BLAST("ncbi-blast-2.12.0+/bin/psiblast.exe", sys.argv)
# Check that the required commmand line arguements were passed in
check_cmd_args(psiblast.args)
# Compile command line arguments
queries = PSI_BLAST.parse_fasta(psiblast.args['script_args']['-query_parallel'])

commands = psiblast.compile_cmd(psiblast.args, blast_rslt_dir, blast_working_dir)

start_time = time.time()
psiblast.exec_commands(commands)

if os.path.isdir(blast_working_dir):
    shutil.rmtree(blast_working_dir)
    
print("")
pdb_dir = "pdb\\"
pdbdownload = PDBList()

tasks = []
align_files = []
for file in os.listdir(blast_rslt_dir):
    if file.split(".")[0] in queries:
        seq = queries[file.split(".")[0]]
        # Read the file
        with open(blast_rslt_dir + file) as f:
            content = f.read()
        path = blast_rslt_dir + file
        try:
            acc = None
            for protein in iter(BLAST_Rslts_Itr(content, path)):
                acc = protein['accession'][:protein['accession'].find("_")]
                break
            if acc is not None:
                downloaded_path = pdbdownload.retrieve_pdb_file(acc, file_format="pdb", pdir=pdb_dir + acc, overwrite=True)
                for file in os.listdir(pdb_dir + acc):
                    src = pdb_dir + acc + "\\" + file
                    dest = acc + ".pdb"
                    if not os.path.isfile(dest):
                        shutil.copy(src , dest)
                    os.remove(src)
                    break
                
                bsali = ">P1;Bs\nsequence:Bs:::::::0.00: 0.00\n" + seq + "*"
                f = open("bs.ali", "w")
                f.write(bsali)
                f.close()
                template_path = acc + ".pdb"
                task = ['py', 'align2d.py', acc, template_path]
                tasks += [task]
                ali_file = 'align\Bs-' + acc + '.ali'
                pap_file = 'align\Bs-' + acc + '.pap'
                align_files += (ali_file, pap_file)
                #Popen(task)
                #os.remove(dest)
        except:
            print("An exception occured")
exec_commands(tasks)
print("---%s seconds ---" % (time.time() - start_time))