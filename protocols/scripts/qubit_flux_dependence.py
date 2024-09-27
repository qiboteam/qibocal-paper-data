import numpy as np
import json
from qibocal.protocols import qubit_flux
import pathlib
import matplotlib.pyplot as plt
from qibocal.protocols.flux_dependence.utils import transmon_frequency

WIDTH = 0.5
FONT = 24

BLUE = "#788ae3"
RED = "#d1545e"
DARKBLUE = "#075cb3"
DARKRED = "#8c1822"

path = pathlib.Path("../figures/test_flux_again")
data_path = path / "data/qubit flux dependence-0"
data = qubit_flux.data_type.load(data_path)
qubit = "D1"
bias = np.unique(data[qubit].bias)
freq = np.unique(data[qubit].freq)*1e-9
signal = np.array(data[qubit].signal.tolist())
signal = (signal - min(signal)) / (max(signal) - min(signal))

results = qubit_flux.results_type.load(data_path)
params = results.fitted_parameters[qubit]

predicted_frequency = transmon_frequency(bias, **params)
filter = np.logical_and(predicted_frequency>= np.min(freq), predicted_frequency<np.max(freq))

plt.figure(figsize=(10 * WIDTH, 10 * WIDTH * 6/8))
plt.imshow(signal.reshape(len(np.unique(bias)), len(np.unique(freq))),aspect = 'auto', extent = [np.min(freq), np.max(freq), np.min(bias), np.max(bias)], cmap="coolwarm", origin="lower")
plt.plot(predicted_frequency[filter], bias[filter], color="black", lw=1, ls="--")
plt.xlabel("Drive Frequency [GHz]", fontsize=14)
plt.ylabel("Bias [V]", fontsize=14)
plt.text(-0.1, 1.05, '(b)', transform=plt.gca().transAxes, fontsize=14)
cbar = plt.colorbar()
cbar.set_label("Normalized signal [a.u.]", fontsize=14)
plt.savefig("../figures/flux_dep.pdf", bbox_inches="tight", dpi=1000)
