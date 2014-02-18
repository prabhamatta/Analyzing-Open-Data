# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# Name:Prabhavathi Matta
# Assignment 2

import pandas as pd
from pandas import DataFrame

import census
import settings
import us

from itertools import islice

# instantiate the census object

c=census.Census(settings.CENSUS_KEY)

# <codecell>

#places are the geographical regions specifically under 'states' category
#to find the fips of all the states
states_fips = [state.fips for state in us.states.STATES ]

# <codecell>

## EXERCISE
## FILL in with your generator for all census places in the 2010 census 

#submitted in hw
# def places(variables="NAME"):
#     for fip in states_fips:
#         for k in c.sf1.get(variables, geo={'for':'place:*','in':'state:{fips}'.format(fips=fip)}):
#             yield k
    
 
#FASTER and better method    
def places(variables="NAME"):
    for k in c.sf1.get(variables, geo={'for':'place:*'}):
        if k['state'] in states_fips:
            yield k
    
    
## Alternate method: using normal list instead of generator
# def places(variables="NAME"):
#     k = []
#     for fip in states_fips:
#         k.extend(c.sf1.get('NAME,P0010001', geo={'for':'place:*','in':'state:{fips}'.format(fips=fip)}))
#     return k


##this method gives wrong places.
# def places(variables="NAME"):
#     for k in c.sf1.get('NAME,P0010001', geo={'for':'place:*'}):
#          yield k
    
    
    

# <codecell>

# use this code to run your code
# I recommend replacing the None in islice to a small number to make sure you're on 
# the right track

r = list(islice(places("NAME,P0010001"), None))
places_df = DataFrame(r)
places_df.P0010001 = places_df.P0010001.astype('int')
places_df['FIPS'] = places_df.apply(lambda s: s['state']+s['place'], axis=1)

print "number of places", len(places_df)
print "total pop", places_df.P0010001.sum()
places_df.head()

# <codecell>

# if you've done this correctly, the following asserts should stop complaining
assert places_df.P0010001.sum() == 228457238
# number of places in 2010 Census
assert len(places_df) == 29261

