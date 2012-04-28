import sys
import csv

class Collate(object):
    _setA = None
    _setB = None
    
    ''' Csv parsing and formatting
    '''
    def __init__(self, a, b, aM=[], bM=[]):
        self.setA = self._prep(a, *aM)
	self.setB = self._prep(b, *bM)
        if self.setA == None or self.setB == None:
            ## Could also consider defining a custom Exception class if 
            ## you want it to be easy to catch exceptions (e.g. CollateDataError, or some such)
            raise ValueError('A description of the problem which occurred here.')
    
    def _prep(self, csv_file, col=0, start=0, end=sys.maxint):
        ''' Prepare values in selected column from CSV file (f)
        '''
        col, start, end = int(col), int(start), int(end)
        with open(csv_file) as f:
            fn = []
            if col > 0:
                fn += [0]*(col-len(fn)) #: Pad/ ignore columns (< col)
            fn.append('name') #: Mark selected column 
            raw = list(csv.DictReader(f, fieldnames=fn))
            return set(map(lambda e: e['name'], raw[start:end]))
    
    ''' Make properties use validation & write-once only
    '''
    @property
    def setA(self): return self._setA
    
    @property
    def setB(self): return self._setB
    
    @setA.setter
    def setA(self, v):
        if self._setA == None:
            self._setA = v
    
    @setB.setter
    def setB(self, v):
        if self._setB == None:
            self._setB = v

    @setA.getter
    def setA(self): return set(self._setA)

    @setB.getter
    def setB(self): return set(self._setB)

    ''' Comparse datasets (/ wrappers for set built-in)
    '''
    # Comparison sets
    @property
    def all(self): return self.setB.union(self.setB)
    
    @property
    def clean(self): return self.setB.intersection(self.setA)
    
    @property
    def added(self): return self.setB.difference(self.setA)
    
    @property
    def erased(self): return self.setA.difference(self.setB)
    
    # Calculations
    def p_erased(self, pretty=False):
        c, e = len(self.setA), len(self.erased)
        if c > e:
            v = 100 * float(e) / float(c)
        else:
            v = 100
        if pretty:
            return "%.2f%% (%s of %s)" % ( v, e, c )
        else:
            return v
    # Output to file
    def write(self, prop, fd):
        pass 
