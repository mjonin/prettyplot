import matplotlib
import matplotlib.pyplot as plt
import seaborn as snb
import matplotlib.text as mtext
from matplotlib.transforms import Bbox
import sys
import numpy as np
from matplotlib import colors

# use output window
#backend = 'Qt'
#get_ipython().run_line_magic('matplotlib', backend)
#print('Using IPython and '+backend+' as graphic window for plot from file '+__name__)

try:
    get_ipython()
    backend = 'QtAgg'
    matplotlib.use(backend)
    plt.ion()
    plt.rcParams['interactive'] = True
    plt.rcParams['agg.path.chunksize'] = 0
except:
    try:
        backend = 'GR'
        matplotlib.use(backend)
    except:
        pass

use_backend = matplotlib.get_backend()
print('Using '+backend+' as graphic window for plot from file '+__name__)

if sys.platform == 'linux':
    plt.style.use('seaborn-v0_8-paper')
else:
    plt.style.use('seaborn-v0_8-paper')

# These are the "Tableau 20" colors as RGB.  
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)
CB_colors = {
    'blue':   [55,  126, 184],  #377eb8 
    'orange': [255, 127, 0],    #ff7f00
    'green':  [77,  175, 74],   #4daf4a
    'pink':   [247, 129, 191],  #f781bf
    'brown':  [166, 86,  40],   #a65628
    'purple': [152, 78,  163],  #984ea3
    'gray':   [153, 153, 153],  #999999
    'red':    [228, 26,  28],   #e41a1c
    'yellow': [222, 222, 0]     #dede00
} 

#plt.ion()

plt.rcParams['figure.max_open_warning'] = False

plt.rcParams['text.usetex'] = True
plt.rcParams['axes.formatter.use_mathtext'] = True

#plt.rcParams['figure.facecolor'] = 'white'
#plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.autolayout'] = True
plt.rcParams['figure.figsize'] = (7.2,7.2/1.6)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Computer Modern Serif'
plt.rcParams['font.size'] = 13
plt.rcParams['figure.titlesize'] = 13
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['legend.fontsize'] = 13
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13
plt.rcParams['legend.loc'] = 'best'
#plt.rcParams['legend.bbox_to_anchor'] = (1.04, 1)
#plt.rcParams['legend.borderaxespad'] = 0

plt.rcParams['hatch.linewidth'] = 0.3

plt.rcParams['text.color'] = 'black'
plt.rcParams['axes.labelcolor'] = 'black'
plt.rcParams['xtick.color'] = 'black'
plt.rcParams['ytick.color'] = 'black'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['xtick.color'] = 'black'
plt.rcParams['ytick.color'] = 'black'

plt.rcParams['xtick.direction'] = 'out'
plt.rcParams['ytick.direction'] = 'out'
plt.rcParams['xtick.bottom'] = True
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.left'] = True
plt.rcParams['ytick.right'] = True
#plt.rcParams['xtick.major.size'] = 1.25
#plt.rcParams['xtick.minor.size'] = 1.0
#plt.rcParams['ytick.major.size'] = 5.0
#plt.rcParams['ytick.minor.size'] = 3.0

plt.rcParams['axes.grid'] = False
plt.rcParams['axes.spines.right'] = True
plt.rcParams['axes.spines.top'] = True
plt.rcParams['axes.spines.bottom'] = True
plt.rcParams['axes.spines.left'] = True

#plt.rcParams['axes.linewidth'] = 3.0

plt.rcParams['legend.handlelength'] = 5.0

plt.rcParams['figure.dpi'] = 90
plt.rcParams['savefig.dpi'] = 500
#plt.rcParams['savefig.bbox']= "tight"

# Modify the color cycle to include darker versions for repeated use
current_palette = snb.color_palette()

def darken_color(color, factor=0.7):
    return [max(0, c * factor) for c in color]

modified_palette = []
for color in current_palette+current_palette:
    if color in modified_palette:
        modified_palette.append( darken_color(color) )
    else:
        modified_palette.append(color)
    
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=modified_palette)


# special class for seaborn legends.

# usage with: e.g.: 
# from prettyPlot import handler_map
# handles, labels = ax.get_legend_handles_labels()
# ax.legend(handles,labels, handler_map=handler_map, loc=2, bbox_to_anchor=(1.175, 1))
class LegendTitle(object):
    def __init__(self, text_props=None):
        self.text_props = text_props or {}
        self.text_props['fontsize'] = plt.rcParams['legend.fontsize']
        super(LegendTitle, self).__init__()

    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        title = mtext.Text(x0+10, y0, orig_handle,  **self.text_props)
        handlebox.add_artist(title)
        return title

handler_map = {str: LegendTitle()}


def full_extent(ax, pad=0.1):
    """Get the full extent of an axes, including axes labels, tick labels, and
    titles."""
    # For text objects, we need to draw the figure first, otherwise the extents
    # are undefined.
    ax.figure.canvas.draw()
    items = ax.get_xticklabels() + ax.get_yticklabels() 
    items += [ax, ax.title, ax.xaxis.label, ax.yaxis.label]
    #items += [ax, ax.title]
    bbox = Bbox.union([item.get_window_extent() for item in items])

    return bbox.expanded(1.0 + pad, 1.0 + pad)

def get_bbox_axis(ax,fig,expand=(1,1)):
    return ax.get_tightbbox(fig.canvas.renderer).transformed(fig.dpi_scale_trans.inverted()).expanded(*expand)

class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))