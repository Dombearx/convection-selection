import utils
import pprint as pp
import matplotlib.pyplot as plt
import numpy as np

fit = utils.readParetoFront("newFront.gen")
fit = [f[1:-1] for f in fit]
splitted = [(float(f.split(",")[0][1:-1]), float(f.split(",")[1][1:-1]))
            for f in fit]

pp.pprint(splitted)

x = [s[0] for s in splitted]
y = [s[1] for s in splitted]


fig, axs = plt.subplots()

axs.scatter(x, y)

#ax.set_xlabel('Grades Range')
#ax.set_ylabel('Grades Scored')
#ax.set_title('scatter plot')
plt.show()
