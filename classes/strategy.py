from abc import ABC, abstractmethod


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all 
    supported versions of some algorithm.

    The Context uses this interface to call the algorithm defined by 
    Concrete Strategies.
    """
    pass


class Outfmt_0_Strat(Strategy):
    """
    Class for the outfmt 0 strategy for the BLAST_Rslts_Itr class.
    """
    def __init__(self, content, filepath):
        """
        Initializes an instance of the Outfmt_0_Strat class.
        
        :param self: The instance of the Outfmt_0_Strat class.
        :param content: The BLAST rslts file to iterate over.
        :param filepath: The filepath to the BLAST rslts file.
        """
        # First make sure file is outfmt 0 
        ext = filepath.split(".")[-1]
        if not Outfmt_0_Strat.is_outfmt_0(content, ext):
            raise exception("BLAST rslts file not right format")
        self.content = content
        self.filepath = filepath
        self.pos = 0
        self.began = False
        self.begin()    
                        
            
    def __iter__(self):
        """
        The overload iter python built-in to make the class iterable.
        
        :param self: An instance of the Outfmt_0_Strat class.
        :return: An iterator for the BLAST results
        """
        return self
        
        
    def __next__(self):
        """
        Sets the instance of the Outfmt_0_Strat class to the next result of
        all the results returned from BLAST.
            
        :param self: An instance of the Outfmt_0_Strat class
        :return: The accession number of the next protein from the results
        """
        if not self.began:
            self.began = True
            # Set the iterator to the first results
            self.begin()
        if not self.end:
            self.start_pos = self.content.find('>', self.end_pos)
            if self.start_pos == -1:
                self.end_itr()
                # Stop the iteration
                raise StopIteration
            self.end_pos = self.content.find('>', self.start_pos + 1)
            if self.end_pos == -1:
                self.end_itr()
                # Stop the iteration
                raise StopIteration
            self.cur_row = self.content[self.start_pos:self.end_pos]
            # Extract the features
            self.extract_features(self.cur_row)
            return self.features
        # Stop the iteration
        raise StopIteration
        
        
    def begin(self):
        """
        Sets up the iterator to the start position and perform 
        initialization.
        
        :param self: The instance of th Outfmt_0_Strat iterator.
        """
        # Boolean to indicate if at end of results
                # The current results as a dictionary
        self.cur = None
        # The current start and end positions within the html file
        self.start_pos = 0
        self.end_pos = 0
        self.cur_row = ''
        # Boolean to indicate if at end of results
        self.end = False
        self.began = True
        # The features from the results row
        self.features = {}
        s = 0
        # Find the starting point of the results table
        s = self.content.find("Sequences producing significant alignments:", s)
        if s == -1:
            self.end_itr()
            return
        self.start_pos = s
        
         
    def end_itr(self):
        """
        Marks the class as at the end of iteration.
        
        :param self: An instance of the Outfmt_0_Strat class.
        """
        self.began = False
        self.end = True
        
        
    def extract_accession(self, row):
        """
        Extracts the accession number from the current row.
        
        :param self: An instance of the Outfmt_0_Strat class.
        :param row: A row from the results table in the html file as a String
        """
        s = row.find(">") + 1
        e = row.find(" ", s)
        acc = row[s:e].strip()
        return acc
        
        
    def extract_e_value(self, row):
        """
        Extracts the E value from the current row.
        
        :param self: An instance of the Outfmt_0_Strat class.
        :param row: A row from the results table in the html file as a String
        """
        s = row.find("Expect =")
        s = row.find("=", s) + 1
        e = row.find(",", s)
        e_value = float(row[s:e].strip())
        return e_value
        
        
    def extract_features(self, row):
        """
        Extracts the features from the 'row' parameter, which is a row from
        the results table from a BLAST query. The features that are 
        currently being extracted are the id and the protein names.
         
        :param self: An instance of the Outfmt_0_Strat class.
        :param row: A row from the results table in the html file as a String
        """
        self.features['accession'] = self.extract_accession(row)
        self.features['score'] = self.extract_score(row)
        self.features['e_value'] = self.extract_e_value(row)
        self.features['per_ident'] = self.extract_per_ident(row)
        
        
    def extract_per_ident(self, row):
        """
        Extracts the E value from the current row.
        
        :param self: An instance of the Outfmt_0_Strat class.
        :param row: A row from the results table in the html file as a String
        """
        s = row.find("Identities =")
        s = row.find("(", s) + 1
        e = row.find("%", s)
        e_value = float(row[s:e].strip())
        return e_value
        
        
        
    def extract_score(self, row):
        """
        Extracts the score from the current row.
        
        :param self: An instance of the Outfmt_0_Strat class.
        :param row: A row from the results table in the html file as a String
        """
        s = row.find("Score =")
        s = row.find("=", s) + 1
        e = row.find("bits", s)
        score = float(row[s:e].strip())
        return score
        
        
    @staticmethod
    def is_outfmt_0(content, ext):
        """
        Determines if a BLAST results file is of the format outfmt 0.
        
        :param content: The content of the BLAST results file.
        :param ext: The extension of the file.
        """
        if ext == "txt":
            pos = content.find("Sequences producing significant alignments:")
            if pos == -1:
                return False
            pos = content.find(">")
            if pos == -1:
                return False
            pos = content.find("Score = ")
            if pos == -1:
                return False
            pos = content.find("Expect = ")
            if pos == -1:
                return False
            pos = content.find("Identities = ")
            if pos == -1:
                return False
            pos = content.find("Positives = ")
            if pos == -1:
                return False
            pos = content.find("Gaps = ")
            if pos == -1:
                return False
            return True
        return False