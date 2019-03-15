import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
import os
import numpy as np
from scipy.signal import savgol_filter

secondgraph = False

plt.rcParams.update({'font.size': 11})

learner_labels = {"eps": "ε=0.1",
                  "eps2": "ε=0.01",
                  "htmrl": "HTMRL",
                  "chtmrl": "HTMRL (small)",
                  "veryhtmrl": "HTMRL (tiny)",
                  "htmrl-nobo": "Noboost",
                  "htmrl-longrew": "Longrew"}


#colors = ["#d7191c", "#fdae61", "#ffffbf", "#abdda4", "#2b83ba"]
if not secondgraph:
    colors = ["#fdae61", "#d7191c", "#1d577c", "#000000"]
else:
    colors = ["#d7191c", "#1d557c", "#3092cf", "#97c8e7"]
styles = ["-", "-", "-", "-", "-"]

def act_count(path):
    name = path.split("/")[-1]
    digits = name_to_digits(name)
    return digits

datadir = "./data/bandit_extra"
#dirs = [x[0] for x in os.walk(datadir)][1:]

repeats = 1000
length = 10000
#print(dirs)
ax = plt.gca()

ctr = 0
d = datadir + "/boosted"
if not secondgraph:
    learners = ["htmrl", "htmrl-nobo", "htmrl-longrew"]
else:
    learners = ["eps2", "htmrl", "chtmrl", "veryhtmrl" ]

mask = list(range(10000))
for a in range(0,10000,2000):
    for b in range(1900,2000):
        mask.remove(a+b)
        print(a+b)

for learner in learners: 
    if d == "raw":
        continue
    with open(d + "/" + learner, "r") as f:
        points = [float(val) for val in f.readlines()]
        #assert len(points ) == (repeats+1) * length
        points = np.array(points[:(repeats*length)])
        name = d.split("/")[-1]
        points = np.reshape(points, (repeats, length))

        #undo moving window cumsum
        #points *= 100

        #for i in range(length - 100):
        #    points[:,i + 100] += points[:,i]

        #points[:,1:] -= points[:,:-1].copy()

        #redo with larger window
        #points = np.cumsum(points, axis=1)
        #points[:,10:] -= points[:,:-10]
        #points[:,:10] /= (np.array(np.arange(10.)) + 1.0)
        #points[:,10:] /= 10.

        #points = points[:,10:]
        meanpoints = np.mean(points, axis=0)
        stdpoints = np.std(points,axis=0)
        print(stdpoints.shape)
        #print(points[:,1000])

        try:
            #done = np.where(meanpoints == 1.0)[0][0]
            done = meanpoints.shape[0] - 1
            print(done)
            meanpoints = meanpoints[:done]
            stdpoints = stdpoints[:done]
        except:
            pass
        meanpoints = savgol_filter(meanpoints, 201,3)
        plt.plot(mask, meanpoints[mask], label=learner_labels[learner], alpha=0.9, ls=styles[ctr], color=colors[ctr])
        print(stdpoints)
        #ax.fill_between(range(len(meanpoints)), meanpoints - stdpoints, meanpoints + stdpoints, alpha=0.5)
        ctr += 1


#ax.set_xscale("log")
handles, labels = ax.get_legend_handles_labels()
order = [2,1,0] if not secondgraph else [1,2,3,0]
handles = [handles[i] for i in order]
labels = [labels[i] for i in order]
ax.legend(handles, labels, loc=4)
#ax.legend(loc=4)
plt.xlim(right=11000)
plt.ylim(bottom=1.0, top=1.5)
#plt.xticks(range(0,11000,1000))
#plt.ylim(bottom=-1.1743108423442274, top=1.1705477696310274)
plt.xlabel("Training steps")
plt.ylabel("Mean reward (latest 10 steps)")
plt.grid()
name = "nonstatic-htmrl" if not secondgraph else "nonstatic-minhtmrl"
#plt.savefig("performance_{}.pdf".format(name), format="pdf", dpi=1200, bbox_inches='tight', pad_inches = 0)
plt.show(block=True)
