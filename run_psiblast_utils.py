import sys, os, time
from subprocess import Popen, list2cmdline
import shutil
from progress.bar import IncrementalBar
         
            
def usage():
    msg = "\nThis program is basically a wrapper for the psiblast program,\n" 
    msg += "which is part of the blastall program from NCBI. All arguements\n"
    msg += "that are used in the psiblast program can also be passed into\n"
    msg += "this script. This script also provide an additional option to\n"
    msg += "blast multiple jobs in parallel. This can be done by specifying the\n"
    msg += "[-query_parallel query_file] option. This program will write the\n" 
    msg += "blast results to the folder 'blast_results', and the file for each\n"
    msg += "result will be saved by the fasta sequence description (what is\n"
    msg += "specified on the line after the '>' symbol). Please note the if\n" 
    msg += "duplicate fasta sequence descriptions exist, then they may override\n"
    msg += "each other."
    
    usage = "Usage for run_psiblast.py:\n"
    usage += "\tpy run_psiblast "
    usage += "[-query_parallel query_file]\n"
    usage += "\t\t[-h] [-help] [-import_search_strategy filename]\n"
    usage += "\t\t[-export_search_strategy filename] [-db database_name]\n"
    usage += "\t\t[-dbsize num_letters] [-gilist filename] [-seqidlist filename]\n"
    usage += "\t\t[-negative_gilist filename] [-negative_seqidlist filename]\n"
    usage += "\t\t[-taxids taxids] [-negative_taxids taxids] [-taxidlist filename]\n"
    usage += "\t\t[-negative_taxidlist filename] [-ipglist filename]\n"
    usage += "\t\t[-negative_ipglist filename] [-entrez_query entrez_query]\n"
    usage += "\t\t[-subject subject_input_file] [-subject_loc range] [-query input_file]\n"
    usage += "\t\t[-out output_file] [-evalue evalue] [-word_size int_value]\n"
    usage += "\t\t[-gapopen open_penalty] [-gapextend extend_penalty]\n"
    usage += "\t\t[-qcov_hsp_perc float_value] [-max_hsps int_value]\n"
    usage += "\t\t[-xdrop_ungap float_value] [-xdrop_gap float_value]\n"
    usage += "\t\t[-xdrop_gap_final float_value] [-searchsp int_value]\n"
    usage += "\t\t[-sum_stats bool_value] [-seg SEG_options] [-soft_masking soft_masking]\n"
    usage += "\t\t[-matrix matrix_name] [-threshold float_value] [-culling_limit int_value]\n"
    usage += "\t\t[-best_hit_overhang float_value] [-best_hit_score_edge float_value]\n"
    usage += "\t\t[-subject_besthit] [-window_size int_value] [-lcase_masking]\n"
    usage += "\t\t[-query_loc range] [-parse_deflines] [-outfmt format] [-show_gis]\n"
    usage += "\t\t[-num_descriptions int_value] [-num_alignments int_value]\n"
    usage += "\t\t[-line_length line_length] [-html] [-sorthits sort_hits]\n"
    usage += "\t\t[-sorthsps sort_hsps] [-max_target_seqs num_sequences]\n"
    usage += "\t\t[-num_threads int_value] [-remote] [-comp_based_stats compo]\n"
    usage += "\t\t[-use_sw_tback] [-gap_trigger float_value] [-num_iterations int_value]\n"
    usage += "\t\t[-out_pssm checkpoint_file] [-out_ascii_pssm ascii_mtx_file]\n"
    usage += "\t\t[-save_pssm_after_last_round] [-save_each_pssm] [-in_msa align_restart]\n"
    usage += "\t\t[-msa_master_idx index] [-ignore_msa_master] [-in_pssm psi_chkpt_file]\n"
    usage += "\t\t[-pseudocount pseudocount] [-inclusion_ethresh ethresh]\n"
    usage += "\t\t[-phi_pattern file] [-version]\n"
    
    print(msg)
    print("")
    print(usage)
    
    
def write_queries(queries, working_dir):
    """
    Writes a dictionary of fasta queries to file. 
    
    :param queries: Dictionary of fasta sequences to write.
    :param working_dir: Working directory to place fasta seqeunces to blast.
    """
    for key in queries.keys():
        f = open(working_dir+key+".fasta", 'w')
        f.write(">" + key + "\n" + queries[key])
        f.close()            