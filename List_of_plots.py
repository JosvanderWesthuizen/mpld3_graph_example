import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from mpld3 import plugins, utils

#Load the data
npz_file = np.load('Neck_data_segmented.npz')
X = npz_file['X'] #shape is (n_samples, n_steps, n_inputs)
Y = npz_file['Y']

#Create a list of 2 samples
X_list = [X[0], X[4]]
Y_list = [Y[0], Y[4]]

fig, ax = plt.subplots(len(X_list),figsize=(17,10))

for idx, sample in enumerate(X_list):
    for dim in xrange(sample.shape[1]):
        ax[idx].plot(sample[:,dim])
    #Set the title to display the label
    ax[idx].set_title('Original label was: '+str(Y_list[idx]))

#Clear the default plugins, which create buttons for zooming and panning
plugins.clear(fig)
#Create automatic zooming and panning
zoom = plugins.Zoom(button=False, enabled=True)
#Add the plugins to the figure
plugins.connect(fig, zoom)

#Save as html
mpld3.save_html(fig, file("figure.html", "wb"))

#Open in browser from python
mpld3.show()