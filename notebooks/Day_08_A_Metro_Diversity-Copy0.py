# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Exercise

# <markdowncell>

# In this exercise, reproduce some of the findings from [What Makes Houston the Next Great American City? | Travel | Smithsonian](http://www.smithsonianmag.com/travel/what-makes-houston-the-next-great-american-city-4870584/), specifically the calculation represented in
# 
# ![Alt text](http://thumbs.media.smithsonianmag.com//filer/Houston-diversity-3.jpg__600x0_q85_upscale.jpg "Optional title")
# 
# whose caption is
# 
# <blockquote>To assess the parity of the four major U.S. ethnic and racial groups, Rice University researchers used a scale called the Entropy Index. It ranges from 0 (a population has just one group) to 1 (all groups are equivalent). Edging New York for the most balanced diversity, Houston had an Entropy Index of 0.874 (orange bar).</blockquote>
# 
# The research report by *Smithsonian Magazine* is
# [Houston Region Grows More Racially/Ethnically Diverse, With Small Declines in Segregation: A Joint Report Analyzing Census Data from 1990, 2000, and 2010](http://kinder.rice.edu/uploadedFiles/Urban_Research_Center/Media/Houston%20Region%20Grows%20More%20Ethnically%20Diverse%202-13.pdf) by the Kinder Institute for Urban Research & the Hobby Center for the Study of Texas.  
# 
# In the report, you'll find the following quotes:
# 
# <blockquote>How does Houston’s racial/ethnic diversity compare to the racial/ethnic
# diversity of other large metropolitan areas? The Houston metropolitan
# area is the most racially/ethnically diverse.</blockquote>
# 
# ....
# 
# <blockquote>Houston is one of the most racially/ethnically diverse metropolitan
# areas in the nation as well. *It is the most diverse of the 10 largest
# U.S. metropolitan areas.* [emphasis mine] Unlike the other large metropolitan areas, all
# four major racial/ethnic groups have substantial representation in
# Houston with Latinos and Anglos occupying roughly equal shares of the
# population.</blockquote>
# 
# ....
# 
# <blockquote>Houston has the highest entropy score of the 10 largest metropolitan
# areas, 0.874. New York is a close second with a score of 0.872.</blockquote>
# 
# ....
# 
# Your task is:
# 
# 1. Tabulate all the metropolian/micropolitan statistical areas.  Remember that you have to group various entities that show up separately in the Census API but which belong to the same area.  You should find 942 metropolitan/micropolitan statistical areas in the 2010 Census.
# 
# 1. Calculate the normalized Shannon index (`entropy5`) using the categories of White, Black, Hispanic, Asian, and Other as outlined in the [Day_07_G_Calculating_Diversity notebook](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_07_G_Calculating_Diversity.ipynb#Converting-to-Racial-Dot-Map-Categories) 
# 
# 1. Calculate the normalized Shannon index (`entropy4`) by not considering the Other category.  In other words, assume that the the total population is the sum of White, Black, Hispanic, and Asian.
# 
# 1. Figure out how exactly the entropy score was calculated in the report from Rice University. Since you'll find that the entropy score reported matches neither `entropy5` nor `entropy4`, you'll need to play around with the entropy calculation to figure how to use 4 categories to get the score for Houston to come out to "0.874" and that for NYC to be "0.872".  [I **think** I've done so and get 0.873618 and 
# 0.872729 respectively.]
# 
# 1. Add a calculation of the [Gini-Simpson diversity index](https://en.wikipedia.org/wiki/Diversity_index#Gini.E2.80.93Simpson_index) using the five categories of White, Black, Hispanic, Asian, and Other.
# 
# 1. Note where the Bay Area stands in terms of the diversity index.
# 
# For bonus points:
# 
# * make a bar chart in the style used in the Smithsonian Magazine
# 
# Deliverable:
# 
# 1. You will need to upload your notebook to a gist and render the notebook in nbviewer and then enter the nbviewer URL (e.g., http://nbviewer.ipython.org/gist/rdhyee/60b6c0b0aad7fd531938)
# 2. On bCourses, upload the CSV version of your `msas_df`.
# 
# **HAVE FUN: ASK QUESTIONS AND WORK TOGETHER**

# <headingcell level=1>

# Constraints

# <markdowncell>

# Below is testing code to help make sure you are on the right track.  A key assumption made here is that you will end up with a Pandas DataFrame called `msas_df`, indexed by the FIPS code of a metropolitan/micropolitan area (e.g., Houston's code is 26420) and with the the following columns:
# 
# * Total
# * White
# * Black
# * Hispanic
# * Asian
# * Other
# * p_White
# * p_Black
# * p_Hispanic
# * p_Asian
# * p_Other
# * entropy4
# * entropy5
# * entropy_rice
# * gini_simpson
# 
# You should have 942 rows, one for each MSA.  You can compare your results for `entropy5`, `entropy_rice` with mine.

# <codecell>

# FILL IN WITH YOUR CODE

import census
import settings
import us


import time
from pandas import DataFrame, Series, Index
import pandas as pd
from itertools import islice
import numpy as np


c = census.Census(key=settings.CENSUS_KEY)

# <codecell>


def msas(variables="NAME"):
    
     for state in us.STATES:
        geo = {'for':'metropolitan statistical area/micropolitan statistical area:*', 
               'in':'state:{state_fips}'.format(state_fips=state.fips)
               }
    
        for msa in c.sf1.get(variables, geo=geo):
            yield msa




# <codecell>


def P005_range(n0,n1): 
    return tuple(('P005'+ "{i:04d}".format(i=i) for i in xrange(n0,n1)))

P005_vars = P005_range(1,18)
P005_vars_str = ",".join(P005_vars)
P005_vars_with_name = ['NAME'] + list(P005_vars)


# http://manishamde.github.io/blog/2013/03/07/pandas-and-python-top-10/#create
def convert_to_rdotmap(row):
    """takes the P005 variables and maps to a series with White, Black, Asian, Hispanic, Other
    Total and Name"""
    return pd.Series({'Total':row['P0050001'],
                      'White':row['P0050003'],
                      'Black':row['P0050004'],
                      'Asian':row['P0050006'],
                      'Hispanic':row['P0050010'],
                      'Other': row['P0050005'] + row['P0050007'] + row['P0050008'] + row['P0050009'],
                      }, index=['Total', 'White', 'Black', 'Hispanic', 'Asian', 'Other'])


def normalize(s):
    """take a Series and divide each item by the sum so that the new series adds up to 1.0"""
    total = np.sum(s)
    return s.astype('float') / total


def entropy(series):
    """Normalized Shannon Index"""
    # a series in which all the entries are equal should result in normalized entropy of 1.0
    
    # eliminate 0s
    series1 = series[series!=0]

    # if len(series) < 2 (i.e., 0 or 1) then return 0
    
    if len(series) > 1:
        # calculate the maximum possible entropy for given length of input series
        max_s = -np.log(1.0/len(series))
    
        total = float(sum(series1))
        p = series1.astype('float')/float(total)
        return sum(-p*np.log(p))/max_s
    else:
        return 0.0

    
def convert_P005_to_int(df):
    # do conversion in place
    df[list(P005_vars)] = df[list(P005_vars)].astype('int')
#     df.NAME = df.NAME

    return df
    

def diversity(r):

    """Returns a DataFrame with the following columns
    """
    df = DataFrame(r)
    df = convert_P005_to_int(df)
    df1 = df.apply(convert_to_rdotmap, axis=1)
    
    df1['entropy5'] = df1[['Asian','Black','Hispanic','White','Other']].apply(entropy,axis=1)
    df1['entropy4'] = df1[['Asian','Black','Hispanic','White']].apply(entropy,axis=1)
    return df1

# <codecell>


msa_list = list(islice(msas(P005_vars_with_name), None))
len(msa_list)

# <codecell>

msa_list
dr = DataFrame(msa_list)
dr = convert_P005_to_int(dr)
dr.head()

grouped = dr.groupby('metropolitan statistical area/micropolitan statistical area').sum()
grouped.head()

# <codecell>


df_diversity = diversity(grouped)

# <codecell>


#'p_Asian', 'p_Black', 'p_Hispanic', 'p_Other','p_White'
df_diversity['p_Asian'] = df_diversity['Asian']/df_diversity['Total']
df_diversity['p_Black'] = df_diversity['Black']/df_diversity['Total']
df_diversity['p_Hispanic'] = df_diversity['Hispanic']/df_diversity['Total']
df_diversity['p_Other'] = df_diversity['Other']/df_diversity['Total']
df_diversity['p_White'] = df_diversity['White']/df_diversity['Total']

# <codecell>


def giniSimpson(series):
    """Normalized Shannon Index"""
    # a series in which all the entries are equal should result in normalized entropy of 1.0
    
    # eliminate 0s
    series1 = series[series!=0]
    
    if len(series) > 1:
        # calculate the maximum possible entropy for given length of input series
        max_s = -np.log(1.0/len(series))
    
        total = float(sum(series1))
        p = series1.astype('float')/float(total)
        return sum(p*(1-p))
    else: 
        return 0.0 
    

def entropyRice(series):
    """Rice Entropy Index"""
    # a series in which all the entries are equal should result in normalized entropy of 1.0
    
    # eliminate 0s
    series1 = series[series!=0]
    
    if len(series) > 1:
        max_s = -np.log(1.0/4) #only 4 races are considered in this Entropy
        p = series1.astype('float')
        p_other = series['p_Other'].astype('float')
        E_other = (-p_other*np.log(p_other))
        
        return (sum(-p*np.log(p)) - E_other)/max_s
    else: 
        return 0.0
    
df_diversity['gini_simpson'] = df_diversity[['Asian','Black','Hispanic','White','Other']].apply(giniSimpson,axis=1)

df_diversity['entropy_rice'] = df_diversity[['p_Asian', 'p_Black','p_Hispanic', 'p_Other','p_White']].apply(entropyRice,axis=1)


# <codecell>

msas_df = df_diversity
len(msas_df)

# <codecell>

# Testing code

def to_unicode(vals):
    return [unicode(v) for v in vals]

def test_msas_df(msas_df):

    min_set_of_columns =  set(['Asian','Black','Hispanic', 'Other', 'Total', 'White',
     'entropy4', 'entropy5', 'entropy_rice', 'gini_simpson','p_Asian', 'p_Black',
     'p_Hispanic', 'p_Other','p_White'])  
    
    #--> what does this assert mean?
    assert min_set_of_columns & set(msas_df.columns) == min_set_of_columns
    
    # https://www.census.gov/geo/maps-data/data/tallies/national_geo_tallies.html
    # 366 metro areas
    # 576 micropolitan areas
    
    assert len(msas_df) == 942  
    
    # total number of people in metro/micro areas
    
    assert msas_df.Total.sum() == 289261315
    assert msas_df['White'].sum() == 180912856
    assert msas_df['Other'].sum() == 8540181
    
    # list of msas in descendng order by entropy_rice 
    # calculate the top 10 metros by population
    top_10_metros = msas_df.sort_index(by='Total', ascending=False)[:10]
    
    msa_codes_in_top_10_pop_sorted_by_entropy_rice = list(top_10_metros.sort_index(by='entropy_rice', 
                                                ascending=False).index) 
    
    assert to_unicode(msa_codes_in_top_10_pop_sorted_by_entropy_rice)== [u'26420', u'35620', u'47900', u'31100', u'19100', 
        u'33100', u'16980', u'12060', u'37980', u'14460']


    top_10_metro = msas_df.sort_index(by='Total', ascending=False)[:10]
    
    list(top_10_metro.sort_index(by='entropy_rice', ascending=False)['entropy5'])
    
    np.testing.assert_allclose(top_10_metro.sort_index(by='entropy_rice', ascending=False)['entropy5'], 
    [0.79628076626851163, 0.80528601550164602, 0.80809418318973791, 0.7980698349711991,
     0.75945930510650161, 0.74913610558765376, 0.73683277781032397, 0.72964862063970914,
     0.64082509648457675, 0.55697288400004963])
    
    np.testing.assert_allclose(top_10_metro.sort_index(by='entropy_rice', ascending=False)['entropy_rice'],
    [0.87361766576115552,
     0.87272877244078051,
     0.85931803868749834,
     0.85508015237749468,
     0.82169723530719896,
     0.81953527301129059,
     0.80589423784325431,
     0.78602596561378812,
     0.68611350427640316,
     0.56978827050565117])

# <codecell>

# you are on the right track if test_msas_df doesn't complain
test_msas_df(msas_df)

# <codecell>

# code to save your dataframe to a CSV
msas_df.to_csv("msas_2010.csv", encoding="UTF-8")

# <codecell>

# load back the CSV and test again
df12 = DataFrame.from_csv("msas_2010.csv", encoding="UTF-8")

test_msas_df(df12)

# <codecell>

top_10_metro = msas_df.sort_index(by='Total', ascending=False)[:10]

top_10_metro.sort_index(by='entropy_rice',ascending=False)

# <codecell>

# 6. Note where the Bay Area stands in terms of the diversity index.
def msas_for_bayarea(variables="NAME"):
    geo = {'for':'metropolitan statistical area/micropolitan statistical area:*', 
           'in':'state:{state_fips}'.format(state_fips='06')
           }
    for msa_ca in c.sf1.get(variables, geo=geo):
        yield msa_ca


msa_ca_list = list(islice(msas_for_bayarea(['P0050001','NAME']), None))

# <codecell>

"""Following is the df of msa of CA - which are bay area? Let us look at various MSAs in CA and manually handpick them"""
DataFrame(msa_ca_list)
# list(DataFrame(msa_ca_list)['metropolitan statistical area/micropolitan statistical area'].astype('int'))
#  df[list(P005_vars)] = df[list(P005_vars)].astype('int')

# <codecell>

"""I am considering the following 4 areas as bay area MSAs"""
# Napa, CA Metro Area	 136484	 34900	 06
# San Francisco-Oakland-Fremont, CA Metro Area	 4335391	 41860	 06
# San Jose-Sunnyvale-Santa Clara, CA Metro Area	 1836911	 41940	 06
# Santa Rosa-Petaluma, CA Metro Area	 483878	 42220	 06
df_bay = msas_df[msas_df.index.isin(['34900', '41860', '41940', '42220'])]

# <codecell>

df_bay

# <codecell>

# Barchart showing desities of top 10 MSAs 
def createBarchart(msas_df,df_bay):
    #http://matplotlib.org/examples/api/barchart_demo.html
    %pylab --no-import-all inline
    import numpy as np
    import matplotlib.pyplot as plt
    n_groups = 10
    top_10_metro = msas_df.sort_index(by='Total', ascending=False)[:10]
    top_10_metro = top_10_metro.sort_index(by='entropy_rice',ascending=False) #  sorting by Entropy_rice
    
#     #adding bayarea MSAs to Top 10
#     top_10_metro= top_10_metro.add(df_bay, fill_value=0)
#     print len(top_10_metro)
    
    white   = tuple(top_10_metro['p_White'])
    hispanic   = tuple(top_10_metro['p_Hispanic'])
    black   = tuple(top_10_metro['p_Black'])
    asian   = tuple(top_10_metro['p_Asian'])
    other   = tuple(top_10_metro['p_Other'])
    
    fig, ax = plt.subplots(figsize=(14,5))
    
    index = np.arange(n_groups)
    bar_width = 0.15
    
    opacity = 0.7
    error_config = {'ecolor': '0.3'}
    
    rects1 = plt.bar(index, white, bar_width,
                     alpha=opacity,
                     color='b',
                     label='white')
    
    rects2 = plt.bar(index + bar_width, hispanic, bar_width,
                     alpha=opacity,
                     color='r',
                     label='hispanic')
    rects3 = plt.bar(index + 2*bar_width, black, bar_width,
                     alpha=opacity,
                     color='c',
                     label='black')
    
    rects4 = plt.bar(index + 3*bar_width, asian, bar_width,
                     alpha=opacity,
                     color='y',
                     label='asian')
    rects5 = plt.bar(index + 4*bar_width, other, bar_width,
                     alpha=opacity,
                     color='g',
                     label='other')
    

    plt.xlabel('MSA IDs')
    plt.ylabel('Percentages')
    plt.title('Barchart showing desities of Top 10 most Diverse MSAs')
    plt.xticks(index + 2*bar_width, tuple(top_10_metro.index),  rotation=45)
    plt.legend()
    plt.yticks(np.arange(0,1.1,.1))
    plt.tight_layout()
    plt.show()


    
    
createBarchart(msas_df,df_bay)
##'34900', '41860', '41940', '42220' are Bay area MSAs

# <codecell>

# Barchart showing desities of Bay Area MSAs
def createBarchart(msas_df,df_bay):
    #http://matplotlib.org/examples/api/barchart_demo.html
    %pylab --no-import-all inline
    import numpy as np
    import matplotlib.pyplot as plt
    n_groups = 4
    top_10_metro = msas_df.sort_index(by='Total', ascending=False)[:10]
    top_10_metro = top_10_metro.sort_index(by='entropy_rice',ascending=False) #  sorting by Entropy_rice
    
    # bayarea MSAs
    top_10_metro= df_bay
    print len(top_10_metro)
    
    white   = tuple(top_10_metro['p_White'])
    hispanic   = tuple(top_10_metro['p_Hispanic'])
    black   = tuple(top_10_metro['p_Black'])
    asian   = tuple(top_10_metro['p_Asian'])
    other   = tuple(top_10_metro['p_Other'])
    
    fig, ax = plt.subplots(figsize=(14,5))
    
    index = np.arange(n_groups)
    bar_width = 0.10
    
    opacity = 0.7
    error_config = {'ecolor': '0.3'}
    
    rects1 = plt.bar(index, white, bar_width,
                     alpha=opacity,
                     color='b',
                     label='white')
    
    rects2 = plt.bar(index + bar_width, hispanic, bar_width,
                     alpha=opacity,
                     color='r',
                     label='hispanic')
    rects3 = plt.bar(index + 2*bar_width, black, bar_width,
                     alpha=opacity,
                     color='c',
                     label='black')
    
    rects4 = plt.bar(index + 3*bar_width, asian, bar_width,
                     alpha=opacity,
                     color='y',
                     label='asian')
    rects5 = plt.bar(index + 4*bar_width, other, bar_width,
                     alpha=opacity,
                     color='g',
                     label='other')
    

    plt.xlabel('MSA IDs')
    plt.ylabel('Percentages')
    plt.title('Barchart showing desities of Bay Area MSAs')
    plt.xticks(index + 2*bar_width, tuple(top_10_metro.index),  rotation=45)
    plt.legend()
    plt.yticks(np.arange(0,1.1,.1))
    plt.tight_layout()
    plt.show()


    
    
createBarchart(msas_df,df_bay)
##'34900', '41860', '41940', '42220' are Bay area MSAs

# <codecell>

# Barchart showing desities of top 10 MSAs vs Bay Area MSAs
def createBarchart(msas_df,df_bay):
    #http://matplotlib.org/examples/api/barchart_demo.html
    %pylab --no-import-all inline
    import numpy as np
    import matplotlib.pyplot as plt
    n_groups = 10
    top_10_metro = msas_df.sort_index(by='Total', ascending=False)[:10]
    top_10_metro = top_10_metro.sort_index(by='entropy_rice',ascending=False) #  sorting by Entropy_rice
    
#     #adding bayarea MSAs to Top 10
#     top_10_metro= top_10_metro.add(df_bay, fill_value=0)
#     print len(top_10_metro)
    
    white   = tuple(top_10_metro['p_White'])
    hispanic   = tuple(top_10_metro['p_Hispanic'])
    black   = tuple(top_10_metro['p_Black'])
    asian   = tuple(top_10_metro['p_Asian'])
    other   = tuple(top_10_metro['p_Other'])
    
    fig, (ax2, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(18,5))
    
    index = np.arange(n_groups)
    bar_width = 0.20
    
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    
#     plt.subplot(1, 2, 1)
    rects1 = ax1.bar(index, white, bar_width,
                     alpha=opacity,
                     color='b',
                     label='white')
    
    rects2 = ax1.bar(index + bar_width, hispanic, bar_width,
                     alpha=opacity,
                     color='r',
                     label='hispanic')
    rects3 = ax1.bar(index + 2*bar_width, black, bar_width,
                     alpha=opacity,
                     color='c',
                     label='black')
    
    rects4 = ax1.bar(index + 3*bar_width, asian, bar_width,
                     alpha=opacity,
                     color='y',
                     label='asian')
    rects5 = ax1.bar(index + 4*bar_width, other, bar_width,
                     alpha=opacity,
                     color='g',
                     label='other')


    ax1.set_xlabel('Race')
    ax1.set_ylabel('Percentages')
    ax1.set_yticks(np.arange(0,1.1,.1))
    ax1.set_xticklabels(index + 2*bar_width, tuple(top_10_metro.index))
    
   
    
    
    white   = tuple(df_bay['p_White'])
    hispanic   = tuple(df_bay['p_Hispanic'])
    black   = tuple(df_bay['p_Black'])
    asian   = tuple(df_bay['p_Asian'])
    other   = tuple(df_bay['p_Other'])
        
    index1 = np.arange(4)
    bar_width = 0.15
    
#     plt.subplot(1, 2, 2)
    rects1 = ax2.bar(index1, white, bar_width,
                     alpha=opacity,
                     color='b',
                     label='white')
    
    rects2 = ax2.bar(index1 + bar_width, hispanic, bar_width,
                     alpha=opacity,
                     color='r',
                     label='hispanic')
    rects3 = ax2.bar(index1 + 2*bar_width, black, bar_width,
                     alpha=opacity,
                     color='c',
                     label='black')
    
    rects4 = ax2.bar(index1 + 3*bar_width, asian, bar_width,
                     alpha=opacity,
                     color='y',
                     label='asian')
    rects5 = ax2.bar(index1 + 4*bar_width, other, bar_width,
                     alpha=opacity,
                     color='g',
                     label='other')


    ax2.set_xlabel('MSA IDs')
    ax2.set_ylabel('Percentages')
    ax2.set_xticklabels(index1 + 2*bar_width, tuple(df_bay.index))
    ax2.set_yticks(np.arange(0,1.1,.1))

    fig.suptitle('Barchart showing desities of Top 10 most Diverse MSAs', fontsize=14)

#     plt.title('Barchart showing desities of Top 10 most Diverse MSAs')
    ax2.legend()
    plt.tight_layout()
    plt.show()


    
    
createBarchart(msas_df,df_bay)
##'34900', '41860', '41940', '42220' are Bay area MSAs    plt.yticks(np.arange(0,1.1,.1))

# <codecell>

# Barchart showing desities of top 10 MSAs and Bay Area MSAs
def createBarchart(msas_df):
    #http://matplotlib.org/examples/api/barchart_demo.html
    %pylab --no-import-all inline
    import numpy as np
    import matplotlib.pyplot as plt
    
    N = 14
    top_10_metro = msas_df.sort_index(by='Total', ascending=False)[:10]
    top_10_metro = top_10_metro.sort_index(by='entropy_rice',ascending=False) #  sorting by Entropy_rice
    
    #adding bayarea MSAs to Top 10
    top_10_metro= top_10_metro.add(df_bay, fill_value=0)
    print len(top_10_metro)
    
    fig, ax = plt.subplots(figsize=(14,5))
    asian   = tuple(top_10_metro['p_Asian'])
    black   = tuple(top_10_metro['p_Black'])
    hispanic   = tuple(top_10_metro['p_Hispanic'])
    white   = tuple(top_10_metro['p_White'])
    other   = tuple(top_10_metro['p_Other'])

    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence
    
    comb = lambda a, b: tuple(x+y for x, y in zip(a, b))
   
    ao = comb(asian, other)
    bao = comb(black, ao)
    hbao = comb(hispanic, bao)
    
    p5 = plt.bar(ind, other,   width, color='g', alpha=0.8)
    p4 = plt.bar(ind, asian,   width, color='y', alpha=0.8, bottom=other)
    p3 = plt.bar(ind, black,   width, color='c', alpha=0.8, bottom=ao)
    p2 = plt.bar(ind, hispanic,   width, color='r', alpha=0.8, bottom=bao)
    p1 = plt.bar(ind, white,   width, color='b', alpha=0.8,bottom=hbao)

#   p2 = plt.bar(ind, womenMeans, width, color='y', bottom=menMeans)
    
    #crimson', 'burlywood', 'chartreuse'
    plt.ylabel('Percentages')
    plt.xlabel('MSA IDs')

    plt.title('Barchart showing desities of top 10 MSAs and Bay Area MSAs')
    plt.xticks(ind+width/2., tuple(top_10_metro.index), rotation=45 )
    plt.yticks(np.arange(0,1.1,.1))
    plt.legend( (p1[0], p2[0],p3[0], p4[0],p5[0]), ('White', 'Hispanic', 'Black', 'Asian', 'Others') )
    
    plt.show()
    
    
createBarchart(msas_df)
            

