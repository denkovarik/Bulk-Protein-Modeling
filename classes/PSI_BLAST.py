import sys, os, time
from subprocess import Popen, list2cmdline
import shutil
from progress.bar import IncrementalBar


class PSI_BLAST():
    """
    Class to run the psiblast program from the NCBI blastall programs
    """  
    def __init__(self, prgm_path, cmd_args):
        """
        Initializes an instance of the PSI_BLAST class.
        
        :param self: The instance of the PSI_BLAST class.
        :param prgm_path: Path to the psiblast program
        :param cmd_args: List of the cmd args.
        """
        # Make sure that prgm_path exists
        if not os.path.isfile(prgm_path):
            print(prgm_path + " does not exist")
            exit()
        # parse the cmd args
        self.prgm_path = prgm_path
        self.args = self.parse_args(sys.argv)
        
        
    def compile_cmd(self, args, blast_rslt_dir, blast_working_dir):
        """
        Compiles the dictionary of arguements into a list of arguements that can be run.
        
        :param self: The instance of the PSI_BLAST class.
        :param args: A dictionary of command line arguements
        :param blast_rslt_dir: Path to the directory to store the results in
        :param blast_working_dir: Path to the temp directory to store fasta sequences
        :return: A list of command line arguements
        """
        commands = []
        cmd = []
        cmd += [args['script_args']['-program']]
        # Continue previous job?
        if '-continue' in args['script_args'].keys() and os.path.isdir(blast_working_dir):
            if not os.path.isdir(blast_rslt_dir):
                os.mkdir(blast_rslt_dir)
            ignored = set(('-out','-query'))
            # Compile the command line arguements to be run
            for key in args['blast_args'].keys():
                if not key in ignored and args['blast_args'][key] is not None:
                    cmd += [key]
                    cmd += [args['blast_args'][key]]
            # Now create a command for each fasta sequence
            for file in os.listdir(blast_working_dir):
                seq_cmd = cmd.copy()
                seq_cmd += ['-query']
                seq_cmd += [blast_working_dir + file]
                seq_cmd += ['-out']
                seq_cmd += [blast_rslt_dir + file.split('.')[0] \
                        + args['script_args']['rslt_ext']]
                commands += [seq_cmd]
        # If the -query_parallel arg is not specified, then just run program normally
        elif not '-query_parallel' in args['script_args'].keys():
            for key in args['blast_args'].keys():
                cmd += [key]
                if args['blast_args'][key] is not None:
                    cmd += [args['blast_args'][key]]  
            commands += [cmd]
        else:
            # Create files for fasta sequences.
            queries = self.parse_fasta(args['script_args']['-query_parallel'])
            if not os.path.isdir(blast_rslt_dir):
                os.mkdir(blast_rslt_dir)
            if not os.path.isdir(blast_working_dir):
                os.mkdir(blast_working_dir)
            self.write_queries(queries, blast_working_dir)
            ignored = set(('-out','-query'))
            # Compile the command line arguements to be run
            for key in args['blast_args'].keys():
                if not key in ignored and args['blast_args'][key] is not None:
                    cmd += [key]
                    cmd += [args['blast_args'][key]]
            # Now create a command for each fasta sequence
            for loc in queries.keys():
                seq_cmd = cmd.copy()
                seq_cmd += ['-query']
                seq_cmd += [blast_working_dir + loc + '.fasta']
                seq_cmd += ['-out']
                seq_cmd += [blast_rslt_dir + loc + args['script_args']['rslt_ext']]
                commands += [seq_cmd]
            
        return commands
        

    def cpu_count(self):
        ''' 
        Returns the number of CPUs in the system
        
        :param self: The instance of the PSI_BLAST class.
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
        

    def exec_commands(self, cmds):
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

        max_task = self.cpu_count()
        processes = []
        bar = IncrementalBar('| BLASTing Sequences...', max = len(cmds))
        while True:
            while cmds and len(processes) < max_task:
                task = cmds.pop()
                i = 0
                while i < len(task):
                    file = ""
                    if task[i] == '-query' and i < len(task) - 1:
                        file = task[i+1]
                        break
                    i += 1
                processes.append((Popen(task), file))

            for p in processes:
                if done(p[0]):
                    if success(p[0]):
                        os.remove(p[1])
                        processes.remove(p)
                        bar.next()
                    else:
                        fail()

            if not processes and not cmds:
                break
            else:
                time.sleep(0.05)
                
        
    def fix_win_filepath(self, filepath):
        """
        Replaces every '/' char with '\\'.
        
        :param self: The instance of the PSI_BLAST class.
        :param filepath: The filepath to fix
        :return: String of a filepath with every '/' char replaced with '\\'.
        """
        i = 0
        while filepath.find("\\") != -1:
            filepath = filepath.replace("\\", "/")
        while filepath.find("/") != -1:
            filepath = filepath.replace("/", "\\")
        return filepath
                
                
    def parse_args(self, cmd_args):
        """
        Parses the command line arguments passed into the function.
        
        :param self: The instance of the PSI_BLAST class.
        :param args: A list of command line arguments.
        :return: A dictionary of command line arguments.
        """
        # Dictionary of the command line arguements
        args = {
                    "blast_args"    : {},
                    "script_args"   : {}
               }
        script_args = set(("-program", "-query_parallel"))
        args['script_args']["-program"] = self.prgm_path
        # Add program arguement
        i = 1
        while i < len(cmd_args):
            # Command line arguements specific to this script
            if cmd_args[i] in script_args:
                args['script_args'][cmd_args[i]] = cmd_args[i+1]
                i += 1  
            # Command line arguements specific to this psiblast
            elif cmd_args[i][0] == "-":
                if i + 1 < len(cmd_args) and cmd_args[i+1][0] != "-":
                    args['blast_args'][cmd_args[i]] = cmd_args[i+1]
                    i += 1 
                else:
                    args['blast_args'][cmd_args[i]] = None
            i += 1            
        # fix filepaths if in windows
        if os.name == 'nt':
            for key in args['script_args'].keys():
                if args['script_args'][key] is not None:
                    args['script_args'][key] \
                        = self.fix_win_filepath(args['script_args'][key])
            for key in args['blast_args'].keys():
                if args['blast_args'][key] is not None:
                    args['blast_args'][key] \
                        = self.fix_win_filepath(args['blast_args'][key])
        # Determine file extension
        if '-outfmt' in args['blast_args'].keys():
            if args['blast_args']['-outfmt'] == '5':
                args['script_args']['rslt_ext'] = '.xml'
            elif '-html' in args['blast_args'].keys():
                args['script_args']['rslt_ext'] = '.xml'
            else:
                args['script_args']['rslt_ext'] = '.txt'
        else:
            args['script_args']['rslt_ext'] = '.txt'
        return args
        
        
    def parse_fasta(self, filepath):
        """
        Parses a fasta file and extracts the sequence descriptions and sequences.
        
        :param self: The instance of the PSI_BLAST class.
        :param filepath: The filepath of the file containing the multiple fasta 
                         sequences.
        :return: A dictionary mapping fasta descriptions to their sequences.
        """
        queries = {}
        f = open(filepath, 'r')
        content = f.read()
        f.close()
        content = content.split("\n")
        i = 0
        while i < len(content):
            if len(content[i].strip()) > 0:
                if content[i].strip()[0] == '>':
                    des = content[i][1:].strip()
                    queries[des] = content[i+1] 
                    i += 1
            i += 1
        return queries   

    def write_queries(self, queries, working_dir):
        """
        Writes a dictionary of fasta queries to file. 
        
        :param self: The instance of the PSI_BLAST class.
        :param queries: Dictionary of fasta sequences to write.
        :param working_dir: Working directory to place fasta seqeunces to blast.
        """
        for key in queries.keys():
            f = open(working_dir+key+".fasta", 'w')
            f.write(">" + key + "\n" + queries[key])
            f.close()   