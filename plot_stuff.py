import openmc
import numpy as np

sp = openmc.StatePoint('statepoint.10.h5')

tbr = sp.tallies[2].mean[:, -1, 0]
tbr_sd = sp.tallies[2].std_dev[:, -1, 0]
heat = sp.tallies[3].mean[:, 0, 0].reshape((1, 7))
#heat_sd = sp.tallies[3].std_dev[:, 0, 0].reshape((4, 7))
print(np.sum(tbr))
print(np.sum(heat)/14.1E6)
