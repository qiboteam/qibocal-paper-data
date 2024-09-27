import numpy as np
import json
from qibocal.protocols import dispersive_shift
import pathlib
import matplotlib.pyplot as plt
from qibocal.protocols.utils import lorentzian

WIDTH = 0.5
FONT = 24

BLUE = "#788ae3"
RED = "#d1545e"

DARKBLUE = "#075cb3"
DARKRED = "#8c1822"

lstyles = ["-.", "--"]
colors = [RED, BLUE]
darkcolors = [DARKRED, DARKBLUE]

path = pathlib.Path("../figures/test_dispersive_shift")
data_path = path / "data/dispersive_shift-0"
data = dispersive_shift.data_type.load(data_path)
qubit = "D1"

with open(data_path/"results.json") as f:
    results = json.load(f)

plt.figure(figsize=(10 * WIDTH, 10 * WIDTH * 6/8))
best_freq = results["\"best_freq\""]["\"D1\""]*1e-9
for i, key in enumerate(["\"fitted_parameters_state_zero\"", "\"fitted_parameters_state_one\""]):
    freq = data[(qubit,i)].freq*1e-9
    fit_params =  results[key]["\"D1\""]
    model_signal = lorentzian(np.unique(freq), *fit_params)
    signal = data[(qubit,i)].signal
    plt.plot(freq, signal * 1000, color=colors[i], label = fr"$|{i}\rangle$", lw=2.5, alpha=0.7)
    # plt.plot(freq, model_signal * 1000, color=darkcolors[i], label = fr"fit $|{i}\rangle$", linestyle=lstyles[i], lw=1.5)
plt.text(-0.1, 1.05, '(c)', transform=plt.gca().transAxes, fontsize=14)

plt.axvline(x=best_freq, label = r"Best", ls="--", color="black", lw=1)
plt.xlabel("Frequency [GHz]", fontsize=14)
plt.xlim(min(freq), max(freq))
plt.ylabel("Signal [a.u.]", fontsize=14)
plt.legend(fontsize=10, ncols=1, loc=3)
plt.savefig("../figures/disp_shift.pdf", bbox_inches="tight", pad_inches=0.15, dpi=1000)