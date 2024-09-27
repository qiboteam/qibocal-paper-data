import numpy as np
import json
from qibocal.protocols import qubit_crosstalk
import pathlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from qibocal.protocols.flux_dependence.utils import transmon_frequency

WIDTH = 0.5
FONT = 24

BLUE = "#788ae3"
RED = "#d1545e"
DARKBLUE = "#075cb3"
DARKRED = "#8c1822"

path = pathlib.Path("../figures/test_coupling_fine")
data_path = path / "data/Moving flux of D1 and measuring D2.-0"
data = qubit_crosstalk.data_type.load(data_path).data
qubit = ("D2", "D1")
bias = data[qubit].bias
freq = data[qubit].freq*1e-9
signal = np.array(data[qubit].signal.tolist())*1000
signal = (signal - min(signal)) / (max(signal) - min(signal))

plt.figure(figsize=(10 * WIDTH, 10 * WIDTH * 6/8))
plt.imshow(signal.reshape(len(np.unique(bias)), len(np.unique(freq)))[::-1,::],aspect = 'auto', extent = [np.min(freq), np.max(freq), np.min(bias), np.max(bias)], cmap="coolwarm")
plt.xlabel("Qubit 2 Drive Frequency [GHz]", fontsize=14)
plt.ylabel("Qubit 1 Bias [V]", fontsize=14)
plt.text(-0.1, 1.05, '(d)', transform=plt.gca().transAxes, fontsize=14)

ax = plt.gca()
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))

cbar = plt.colorbar()
cbar.set_label("Normalized signal [a.u.]", fontsize=14)

plt.savefig("../figures/avoided_crossing.pdf", bbox_inches="tight", dpi=1000)
