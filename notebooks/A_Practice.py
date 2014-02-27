# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

f = lambda x: x
double_x = lambda x: 2*x

# <codecell>

def identity(x):
    return x

# <codecell>

def double (x):
    return 2*x

# <markdowncell>

# What is this?

# <codecell>

identity(5)

# <codecell>

double_x(5)

# <codecell>


from pandas import DataFrame, Series, Index
d = {
     'a':10,
     'b':20,
     'c':30
     }
s = Series(d, dtype='object')
s

# <codecell>


def test(series):
    """Normalized Shannon Index"""
    # a series in which all the entries are equal should result in normalized entropy of 1.0
    
    # eliminate 0s
    series1 = series[series!=0]
    
    if len(series) > 1:
        # calculate the maximum possible entropy for given length of input series
        max_s = -np.log(1.0/len(series))
    
        total = float(sum(series1))
        p = series1.astype('float')/float(total)

#         p_other = series1.astype('float')/float(total)
#         E_other = -p*np.log(p))/max_s
        
        return sum(-p*np.log(p))/max_s
    else:
        return 0.0
    
    
import numpy as np
s['c']

# <codecell>

#Prabha: calculate
couties_df.P0010001.apply(lambda n: n)

#to apply to a column
def double(x):
    return 2*x
counties_df.P0010001.apply(double)

# <codecell>

 # islice('ABCDEFG', 2) --> A B
    # islice('ABCDEFG', 2, 4) --> C D
    # islice('ABCDEFG', 2, None) --> C D E F G
    # islice('ABCDEFG', 0, None, 2) --> A C E G

