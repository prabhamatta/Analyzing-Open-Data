# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Productive Bursts

# <headingcell level=2>

# Load Modules and Main Variables

# <codecell>

from urllib2 import urlopen
import json
import re
import pandas as pd
from datetime import datetime
import time
import requests
import matplotlib
from scipy import stats as S
import sys
import numpy as np

sys.path.append("./")
#from tm_python_lib import *


#from settings import github_token
github_token = "819cb7cace7f4a01e41ac5d4e3a9f033c4c6bc15"

ISO8601 = "%Y-%m-%dT%H:%M:%SZ"

settings = {
            'project': 'prabhamatta',
            'repo': 'nlp_information_extraction',
            'github_token': github_token
            }

# <headingcell level=2>

# GitHub API Functions

# <codecell>

# from https://github.com/nipy/dipy/blob/master/tools/github_stats.py

element_pat = re.compile(r'<(.+?)>')
rel_pat = re.compile(r'rel=[\'"](\w+)[\'"]')

def parseLinkHeaders(headers):
    link_s = headers.get('link', '')
    urls = element_pat.findall(link_s)
    rels = rel_pat.findall(link_s)
    d = {}
    for rel,url in zip(rels, urls):
        d[rel] = url
    return d

def getPagedRequest(url):
    """get a full list, handling APIv3's paging"""
    results = []
    while url:
        print("fetching %s" % url)
        f = urlopen(url)
        results_json = json.load(f)
        if type(results_json) == list:
            results.extend(results_json)
        else:
            results.extend([results_json])
        
        links = parseLinkHeaders(f.headers)
        url = links.get('next')
        time.sleep(0.25)
    return results

# <headingcell level=3>

# Functions to Fetch from GitHub API

# <headingcell level=3>

# Functions to Make Data Frames 

# <codecell>

def createCommitsDataframe(commits_json=None, refresh=False):
    
    if not refresh:
        try:
            print 'trying to open commits.json'
            with open('commits.json') as infile:
                print 'reading commits.json'
                df = pd.read_json(infile)
                
                # put timestamp column datatime object
                df['timestamp'] = pd.to_datetime(df.timestamp)
                df.index = df.timestamp
                return df
        except:
            print 'no commits.json found, getting commits and creating DataFrame'
            
    if not commits_json:
        commits_json = getCommits(settings, project_url)
    
    #return  
    df = pd.DataFrame(commits_json)
    
    def addCommitAuthor(row):
        # Commit can have different committer and author
        if row['author']:
            if row['author']['login']:
                return row['author']['login']
            
    def addCommitStats(sha):
        ## API limit is 5000 per hour - TODO: slow  down our calls if we're going to hit
        # the limit
        commit = getCommitInfo(settings, project_url, sha)[0]
        return commit['stats']['additions'], commit['stats']['deletions']
    
    def addCommitDate(commit):
        return commit['author']['date']

    df['author_name'] = df.apply(addCommitAuthor, axis=1)
    ## Out until we can control staying within the API Limit
    #df['additions'], df['deletions'] = zip(*df.sha.apply(addCommitStats))
    df['timestamp'] = df['commit'].apply(addCommitDate)
    df['timestamp'] = pd.to_datetime(df.timestamp)
    df.index = df.timestamp
    print df.head()
    print "returning from createCommitsDataframe..."
    return df

# <codecell>

def createBurstsDataframe(commits_df,t_resol='5D',periods='250D'):
    
    count_commits = commits_df.commit.resample(t_resol,how='count')
    count_authors = commits_df.author_name.resample(t_resol,how=uniquerAuthors)
    Time  = count_commits.index.values
    commits250 = commits_df.commit.resample('250D',how='count')
    authors250 = commits_df.author_name.resample('250D',how=uniquerAuthors)
    Time250  = commits250.index.values
    
    
    contributors = []
    commits = []

    beta = []
    p = []
    r = []
    intercept = []
    
    
    for i,ix in enumerate(Time250[:-1]):
        c = (count_commits.index > ix)*(count_commits.index < Time250[i+1])
        cc = count_commits[c].values
        ca = count_authors[c].values
        c = (cc > 0)*(ca > 0)

        lcc = np.log10(cc[c])
        lca = np.log10(ca[c])

        fit =  S.linregress(lca,lcc)
        #print i,ix,"beta=%.2f (p=%.2f,r=%.2f)"%(fit[0],fit[3],fit[1])
    
        commits.append(cc)
        contributors.append(ca)
        beta.append(fit[0])
        p.append(fit[3])
        r.append(fit[2])
        intercept.append(fit[1])
        
    dico = { 't1' : Time250[:-1],'t2': Time250[1:], "beta" : beta, "p" : p, "r" : r, "commits" : commits, "contributors" : contributors,"intercept":intercept}
    #dico2 = { 'timestamp' : Time250[:-1], "beta" : beta, "p" : p, "r" : r}
    bursts_df = pd.DataFrame(dico,index=dico['t1'])
    
    return bursts_df
    
    

# <headingcell level=2>

# Some Functions for Analysis

# <codecell>

def uniquerAuthors(auth):
    return len(set([a for a in auth if a != None]))


# <headingcell level=2>

# Load and Fetch Data + Create DataFrame

# <codecell>

#print datetime.fromtimestamp(0).strftime(ISO8601) # for github since param
project_url = 'https://api.github.com/repos/{project}/{repo}'.format(**settings)

def getIssues(settings, project_url, state='all'):
    url = project_url + '/issues?access_token={0}&state={1}'.format(settings['github_token'],state)
    return getPagedRequest(url)

def getIssueComments(settings, project_url, issue_id):
    # GET /repos/:owner/:repo/issues/:number/comments
    url = project_url + '/issues/{0}/comments?access_token={1}'.format(
                                                                        issue_id,
                                                                        settings['github_token'])
    return getPagedRequest(url)

def getCommits(settings, project_url):
    # GET /repos/:owner/:repo/commits
    url = project_url + '/commits?access_token={0}'.format(settings['github_token'])
    return getPagedRequest(url)

def getCommitInfo(settings, project_url, sha):
    # GET /repos/:owner/:repo/commits/:sha
    url = project_url + '/commits/{0}?access_token={1}'.format(sha, settings['github_token'])
    #print json.load(urlopen(url))
    return getPagedRequest(url)
    
def getReleases(settings, project_url):
    # GET /repos/:owner/:repo/releases
    pass

# <codecell>

project_url

# <codecell>

#xxx = getCommitInfo(settings, project_url, 'd31f0a266863e23ddfb5f68d48059a5d67f6d683')[0]

# <codecell>

commits_df = createCommitsDataframe()
#commits_df.head()

# <codecell>

type(commits_df)

# <codecell>

period = 200

bursts_df = createBurstsDataframe(commits_df,t_resol='5D',periods='%sD'%period)
bursts_df.head()

# <markdowncell>

# Add greybar colummn commits_df

# <codecell>

timestamps =  np.array(commits_df.index.values.astype('int'))

greybar = np.zeros_like(timestamps).astype('string')

bursts_timestamps = bursts_df.index.values.astype('int')[:-1]

for i,ix in enumerate(bursts_timestamps[:-1]):
    
    c = ( ix < timestamps )*( timestamps < bursts_timestamps[i+1])
    index = np.argwhere(timestamps[c])
    
    #print c[:1000]
    beta = bursts_df.beta[i]
    p = bursts_df.p[i]

    #print i,ix,bursts_timestamps[i+1],p,beta
    
    if beta > 1 and p < 0.1:
        greybar[index] = "#909090"
        #print "good"
    
    elif p >= 0.1:
        greybar[index] = "#FFFFFF"
        #print "blah"
    
    else:
        greybar[index] = "#FFFFFF"
        

# <codecell>

commits_df['greybar'] = greybar
commits_df.head()

# <headingcell level=3>

# Plot Time Series

# <codecell>

resampled_authors = commits_df.author_name.resample('5D',how=uniquerAuthors)
resampled_commits = commits_df.commit.resample('5D',how='count')
Time  = resampled_authors.index.values.astype('int')/1.e9/3600/24
Time = Time - Time.min()

Time = np.array(np.concatenate([[Time[0]],Time,[Time[-1]]]))
resampled_authors = np.concatenate([[0],resampled_authors,[0]])
resampled_commits = np.concatenate([[0],resampled_commits,[0]])

greybar = np.zeros_like(Time).astype('string')



#figure(1,(15,7))

# Plot a grey bar when a productive burst is detected 
timestamps= bursts_df.t1.astype('int')/1.e9/3600/24
timestamps = timestamps - timestamps.min()
for i,ix in enumerate(timestamps):
    beta = bursts_df.beta[i]
    p = bursts_df.p[i]
    
    ix2 = ix + period*1.e9*3600*24
    print ix,ix2
    c = ( ix <= Time )*( Time <= ix2 )
    #index = np.argwhere(Time[c])
    #print Time[c]
    
    if beta > 1 and p < 0.1:
        bar(ix,140,period,color='#909090',linewidth=0.5,alpha=0.6)
        greybar[c] = '#909090'
        
    else:
        greybar[c] = "#FFFFFF"
        
        
# Plot Time Series
fill(Time,resampled_commits,color="red")
fill(Time,resampled_authors,color="green")
xlim(xmax=Time[-1])
xlabel("Time [days]")
ylabel("Active Contributors (green), Commits (red)")


#print greybar

# <codecell>

S.spearmanr(resampled_authors,resampled_commits)

# <headingcell level=3>

# Export CSCV

# <codecell>

# Time Series

output = open(".\timeseries.csv",'wb')
output.write("time,commits,authors,greybar\n") 
for i,ix in enumerate(Time):
   output.write("%s,%s,%s,%s\n" %(ix,resampled_authors[i],resampled_commits[i],greybar[i]))

output.close()

# <codecell>


