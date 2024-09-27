import json
import pathlib

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from qibocal.protocols import chevron_signal


WIDTH = 0.5
FONT = 24

BLUE = "#788ae3"
RED = "#d1545e"
DARKBLUE = "#075cb3"
DARKRED = "#8c1822"

# cmap = LinearSegmentedColormap.from_list("custom_cmap", [DARKRED, DARKBLUE])

path = pathlib.Path("../figures/test_chevron_paper")
data_path = path / "data/chevron-0"
data = chevron_signal.data_type.load(data_path)
qubit = ("D1", "D2")
length = data[qubit].length
amp = data[qubit].amp
signal = np.array(data[qubit].signal_low.tolist()) * 1000
signal = (signal - min(signal)) / (max(signal) - min(signal))

with open(data_path/"results.json") as f:
    results = json.load(f)

plt.figure(figsize=(10 * WIDTH, 10 * WIDTH * 6/8))
plt.imshow(signal.reshape(len(np.unique(length)), len(np.unique(amp))).T,
           aspect = 'auto',
           extent = [np.min(length), np.max(length), np.min(amp),np.max(amp)],
           cmap="coolwarm",
        )
plt.text(-0.1, 1.05, '(e)', transform=plt.gca().transAxes, fontsize=14)

plt.xlabel("Flux pulse duration [ns]", fontsize=14)
plt.ylabel("Flux pulse amplitude [a.u.]", fontsize=14)
cbar = plt.colorbar()
cbar.set_label("Normalized signal [a.u.]", fontsize=14)

plt.savefig("../figures/chevron.pdf", bbox_inches="tight", dpi=1000)
