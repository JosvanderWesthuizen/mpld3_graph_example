import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from mpld3 import plugins, utils
import pandas as pd


class LinkedView(plugins.PluginBase):
    """A simple plugin showing how multiple axes can be linked"""

    JAVASCRIPT = """
    mpld3.register_plugin("linkedview", LinkedViewPlugin);
    LinkedViewPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    LinkedViewPlugin.prototype.constructor = LinkedViewPlugin;
    LinkedViewPlugin.prototype.requiredProps = ["idpts", "idline", "data"];
    LinkedViewPlugin.prototype.defaultProps = {}
    function LinkedViewPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    LinkedViewPlugin.prototype.draw = function(){
      var pts = mpld3.get_element(this.props.idpts);
      var line = mpld3.get_element(this.props.idline);
      var data = this.props.data;

      function mouseover(d, i){
        line.data = data[i];
        line.elements().transition()
            .attr("d", line.datafunc(line.data))
            .style("stroke", this.style.fill);
      }
      pts.elements().on("mouseover", mouseover);
    };
    """

    def __init__(self, points, line, linedata):
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "linkedview",
                      "idpts": utils.get_id(points, suffix),
                      "idline": utils.get_id(line),
                      "data": linedata}

fig, ax = plt.subplots(2,figsize=(15,11))

# scatter periods and amplitudes
np.random.seed(0)
P = 0.2 + np.random.random(size=20)
A = np.random.random(size=20)
x = np.linspace(0, 10, 100)
#data has shape (n_samples, n_dimensions, n_timesteps) i.e. (n_samples, x and y values, number of measurements)
data = np.array([[x, Ai * np.sin(x / Pi)]
                 for (Ai, Pi) in zip(A, P)])
data2 = np.array([[x, Ai * np.cos(x / Pi)]
                 for (Ai, Pi) in zip(A, P)])
data = np.concatenate((data, data2), axis=0)
points = ax[1].scatter(P, A, c=P + A,
                       s=200, alpha=0.5)
ax[1].set_xlabel('Period')
ax[1].set_ylabel('Amplitude')

# create the line object
lines = ax[0].plot(x, 0 * x, '-w', lw=3, alpha=0.5)
ax[0].set_ylim(-1, 1)

ax[0].set_title("Hover over points to see lines")

labels = np.arange(20)
for label, x, y in zip(labels, P, A):
    plt.text(x-.05, y+.05,
        "point" +str(label),
        ha = 'right', va = 'bottom')
    plt.plot([x-.05,x], [y+.05,y], 'k-')

# transpose line data and add plugin
linedata = data.transpose(0, 2, 1).tolist()

#Clear the default plugins, which create buttons for zooming and panning
plugins.clear(fig)
#Create automatic zooming and panning
zoom = plugins.Zoom(button=False, enabled=True)
#Add the plugins to the figure
plugins.connect(fig, LinkedView(points, lines[0], linedata), zoom)

#Save as html
mpld3.save_html(fig, file("figure.html", "wb"))

#Open in browser from python
mpld3.show()