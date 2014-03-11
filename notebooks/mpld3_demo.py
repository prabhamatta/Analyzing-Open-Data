# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# D3 Viewer for Matplotlib

# <markdowncell>

# This notebook shows a few examples of d3 views of matplotlib plots.
# The resulting plots can be panned and zoomed using the mouse.
# 
# See more at http://github.com/jakevdp/mpld3
# 
# Note that not every feature of matplotlib is yet implemented.  Here are a few examples:

# <codecell>

%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# <codecell>

from mpld3 import enable_notebook
enable_notebook()

# <codecell>

# Scatter points
fig, ax = plt.subplots()
np.random.seed(0)
x, y = np.random.normal(0, 1, (2, 200))
color = np.random.random(200)
size = 500 * np.random.random(200)

ax.scatter(x, y, c=color, s=size, alpha=0.3)

ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_title('Matplotlib Plot Rendered in D3!', size=14)

ax.grid(color='lightgray', alpha=0.7)

# <codecell>

# Histogram with modified axes/grid
fig = plt.figure()

ax = fig.add_subplot(111, axisbg='#EEEEEE')
ax.grid(color='white', linestyle='solid')

x = np.random.normal(size=1000)
ax.hist(x, 30, histtype='stepfilled', fc='lightblue', alpha=0.5);

# <codecell>

# Draw lines
fig, ax = plt.subplots()
x = np.linspace(-5, 15, 1000)
for offset in np.linspace(0, 3, 7):
    ax.plot(x, 0.9 * np.sin(x - offset), lw=5, alpha=0.4)
ax.set_xlim(0, 10)
ax.set_ylim(-1.2, 1.0)
ax.text(5, -1.1, "Here are some curves", size=18, ha='center')
ax.grid(color='lightgray', alpha=0.7)

# <codecell>

# multiple subplots, shared axes
fig, ax = plt.subplots(2, 2, figsize=(8, 6),sharex=True, sharey=True)
fig.subplots_adjust(hspace=0.3)

np.random.seed(0)

for axi in ax.flat:
    color = np.random.random(3)
    axi.plot(np.random.random(30), lw=2, c=color)
    axi.set_title("RGB = ({0:.2f}, {1:.2f}, {2:.2f})".format(*color),
                  size=14)
    axi.grid(color='lightgray', alpha=0.7)

