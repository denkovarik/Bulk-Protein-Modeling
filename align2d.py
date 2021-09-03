from modeller import *
import sys, os


# Get filepaths
pdbid = sys.argv[1]
atom_files_path = sys.argv[2]
ali_path = sys.argv[3]

env = environ()
aln = alignment(env)
try:
    mdl = model(env, file=pdbid, model_segment=('FIRST:A','LAST:A'))
    aln.append_model(mdl, align_codes= pdbid + "A", atom_files=atom_files_path)
    aln.append(file=ali_path, align_codes='Bs')
    aln.align2d()
    ali_file = 'align\Bs-' + pdbid + 'A.ali'
    pap_file = 'align\Bs-' + pdbid + 'A.pap'
    aln.write(file=ali_file, alignment_format='PIR')
    aln.write(file=pap_file, alignment_format='PAP')
except:
    print("An exception occured running align2d on " + pdbid)

os.remove(ali_path)
