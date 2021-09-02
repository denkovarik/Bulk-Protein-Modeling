import sys, os, time
from subprocess import Popen, list2cmdline
import shutil
from progress.bar import IncrementalBar


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
        
        
def exec_commands(cmds):
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
    bar = IncrementalBar('| Aligning Proteins...', max = len(cmds))
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