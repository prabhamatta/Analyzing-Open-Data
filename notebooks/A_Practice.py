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

