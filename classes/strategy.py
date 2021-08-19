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
        self.begin()
        
        
    def begin(self):
        """
        Sets up the iterator to the start position and perform 
        initialization.
        
        :param self: The instance of th Outfmt_0_Strat iterator.
        """
        self.end = False
        self.pos = self.content.find(">")
        
        
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