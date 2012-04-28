import sys
import csv

class Collate(object):
    
    ''' Csv parsing and formatting
    '''
    def __init__(self, a, b, aM=[], bM=[]):
    	## I think the names a, b, aM, and bM need to be a bit more verbose,
    	## or if not possible, make sure they are described. 
        self.setA = self._prep(a, *aM)
        self.setB = self._prep(b, *bM)
        if self.setA == None or self.setB == None:
            ## Could also consider defining a custom Exception class if 
            ## you want it to be easy to catch exceptions (e.g. CollateDataError, or some such)
            raise ValueError('A description of the problem which occurred here.')
    
    def _prep(self, csv_file, col=0, start=0, end=sys.maxint):
        ''' Prepare values in selected column from CSV file (f)
        '''
        with open(csv_file) as f: ## Good use of a context :)
            fieldnames = []
            if col > 0:
                fieldnames += [0]*(col-len(fieldnames)) #: Pad/ ignore columns (< col)
            fieldnames.append('name') #: Mark selected column 
            raw = list(csv.DictReader(f, fieldnames=fieldnames))
            return set(map(lambda e: e['name'], raw[start:end]))
    
    ''' Make properties use validation & write-once only
    '''
    @property
    def setA(self):
    	return self._setA
    
    @property
    def setB(self):
    	return self._setB
    
    @setA.setter
    def setA(self, v):
        ## Either raise an excepton, or set the value always.
        ## (setting it only in some circumstances isn't
        ## really expected, and could lead to hard to debug bugs.
        ## So either do what is expected (set it), or raise an error that 
        ## will smack the developer in the face :) )
        if self._setA == None:
            raise SomeKindOfError("setA has already been set.")
        self._setA = v
    
    @setB.setter
    def setB(self, v):
        # As above
        if self._setB == None:
            raise SomeKindOfError("setA has already been set.")
        self._setB = v

    @setA.getter
    def setA(self):
    	return set(self._setA)

    @setB.getter
    def setB(self):
    	return set(self._setB)

    ''' Comparse datasets (/ wrappers for set built-in)
    '''
    # Comparison sets
    @property
    def all(self):
    	return self.setB.union(self.setA)
    
    @property
    def clean(self):
    	return self.setB.intersection(self.setA)
    
    @property
    def added(self):
    	return self.setB.difference(self.setA)
    
    @property
    def erased(self):
    	return self.setA.difference(self.setB)
    
    # Calculations
    def p_erased(self, pretty=False):
        ## Again, I'd pick some more verbose variable names here,
        ## it just makes it easier to read at a later date.
        ## Same may also apply to 'p_erased' - not sure what the 'p'
        ## stands for (but I am a little worse for wear today!)
        c, e = len(self.setA), len(self.erased)
        if c > e:
            v = 100 * float(e) / float(c)
        else:
            v = 100
        if pretty:
            ## My knowledge of format strings isn't that great. So,
            ## for my part, I'd love a little comment here to say what 
            ## is going on :)
            ## Oh! I see now, printing a percentage to two decimal places. Gotcha.
            return "%.2f%% (%s of %s)" % ( v, e, c )
        else:
            return v
    # Output to file
    def write(self, prop, fd):
        pass 
