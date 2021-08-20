


class BLAST_Rslts_Itr():
    """
    Iterator for the results returned from BLAST
    """
    def __init__(self, content):
        """
        Initializes an instance of the BLAST_Rslts_Itr class.
        
        :param self: An instance of the BLAST_Rslts_Itr class
        :param content: The content from the html file of the BLAST Results
        """
        # The features from the results row
        self.features = {}
        # The content of the results .html file returned
        self.content = content
        # Find out which BLAST program was used
        s = self.content.find('<meta name="ncbi_program" content="')
        s = self.content.find('content="', s)
        s = self.content.find('"', s) + 1
        e = self.content.find('"', s)
        self.program = self.content[s:e]
        # The current results as a dictionary
        self.cur = None
        # The current start and end positions within the html file
        self.start_pos = 0
        self.end_pos = 0
        self.cur_row = ''
        # Boolean to indicate if at end of results
        self.end = False
        self.began = False
                    
            
    def __iter__(self):
        """
        The overload iter python built-in to make the class iterable.
        
        :param self: An instance of the BLAST_Rslts_Itr class.
        :return: An iterator for the BLAST results
        """
        return self
        
        
    def __next__(self):
        """
        Sets the instance of the BLAST_Rslts_Itr class to the next result of
        all the results returned from BLAST.
            
        :param self: An instance of the BLAST_Rslts_Itr class
        :return: The accession number of the next protein from the results
        """
        if not self.began:
            self.began = True
            # Set the iterator to the first results
            self.begin()
        if not self.end:
            self.start_pos = self.content.find('<tr id=', self.end_pos)
            if self.start_pos == -1:
                self.end_itr()
                # Stop the iteration
                raise StopIteration
            self.end_pos = self.content.find('</tr>', self.start_pos) + 5
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
        Sets the instance of the BLAST_Rslts_Itr class to the beginning of the
        results returned from BLAST.
            
        :param self: An instance of the BLAST_Rslts_Itr class
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
        s = self.content.find('<tbody>', s)
        if s == -1:
            self.end_itr()
            return
        self.start_pos = s
        
        
    def end_itr(self):
        """
        Marks the class as at the end of iteration.
        
        :param self: An instance of the BLAST_Rslts_Itr class.
        """
        self.began = False
        self.end = True
        
        
    def extract_features(self, row):
        """
        Extracts the features from the 'row' parameter, which is a row from
        the results table from a BLAST query. The features that are 
        currently being extracted are the id and the protein names.
         
        :param self: An instance of the BLAST_Rslts_Itr class.
        :param row: A row from the results table in the html file as a String
        """
        self.features['Program'] = self.program
        self.features['Accession'] = self.get_accession(row)
        self.features['Query Cover'] = self.get_query_cover(row)
        self.features['Per. Ident'] = self.get_per_ident(row)
        self.features['E value'] = self.get_e_value(row)
            
            
    def get_accession(self, row):
        """
        Returns the accession number found in the parameter 'row'.
            
        :param self: An instance of the BLAST_Rslts_Itr class.
        :param row: A row from the results table in the html file as a String
        :return: The accession number
        """
        s = row.find('value="')
        if s == -1:
            return None
        s = row.find('"', s) + 1
        e = row.find('"', s)
        accession = row[s:e]
        return accession.strip()
        
        
    def get_e_value(self, row):
        """
        Returns the e value found in the parameter 'row'.
            
        :param self: An instance of the BLAST_Rslts_Itr class.
        :param row: A row from the results table in the html file as a String
        :return: 
        """
        s = row.find('<td class="c9">')
        if s == -1:
            return None
        s = row.find('>', s) + 1
        e = row.find('<', s)
        query_cover = row[s:e]
        return float(query_cover.strip())
        
        
    def get_per_ident(self, row):
        """
        Returns the query cover found in the parameter 'row'.
            
        :param self: An instance of the BLAST_Rslts_Itr class.
        :param row: A row from the results table in the html file as a String
        :return: 
        """
        s = row.find('<td class="c10">')
        if s == -1:
            return None
        s = row.find('>', s) + 1
        e = row.find('%', s)
        query_cover = row[s:e]
        return float(query_cover.strip())
        
        
    def get_query_cover(self, row):
        """
        Returns the query cover found in the parameter 'row'.
            
        :param self: An instance of the BLAST_Rslts_Itr class.
        :param row: A row from the results table in the html file as a String
        :return: 
        """
        s = row.find('<td class="c8">')
        if s == -1:
            return None
        s = row.find('>', s) + 1
        e = row.find('%', s)
        query_cover = row[s:e]
        return float(query_cover.strip())