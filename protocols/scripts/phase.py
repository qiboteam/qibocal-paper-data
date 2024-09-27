
import numpy as np
import json
from qibocal.protocols import correct_virtual_z_phases
import pathlib
import matplotlib.pyplot as plt
from qibocal.protocols.two_qubit_interaction.virtual_z_phases import fit_function

WIDTH = 0.5
FONT = 24

BLUE = "#788ae3"
RED = "#d1545e"

DARKBLUE = "#075cb3"
DARKRED = "#8c1822"

lstyles = ["-.", "--"]
colors = [RED, BLUE]
darkcolors = [DARKRED, DARKBLUE]
labels = ["I seq.", "X seq."]

path = pathlib.Path("../figures/test_phase")
data_path = path / "data/correct_phase-0"
data = correct_virtual_z_phases.data_type.load(data_path)
qubits = ["D2", "D1"]

with open(data_path/"results.json") as f:
    results = json.load(f)

plt.figure(figsize=(10 * WIDTH, 10 * WIDTH * 6/8))
for i, gate in enumerate(["I", "X"]):
    prob = data.data[(*qubits,gate)].target
    phase = data.thetas
    fit_params =  results[ "\"fitted_parameters\""][f"[\"D2\", \"D1\", \"{gate}\"]"]
    model_signal = fit_function(np.unique(phase), *fit_params)
    plt.plot(phase, prob, label = labels[i], color=colors[i], alpha=0.65, lw=2.5)
    plt.plot(phase, model_signal, label = f"fit {gate} seq.", linestyle = lstyles[i], color=darkcolors[i], lw=1.5)
plt.text(-0.1, 1.05, '(f)', transform=plt.gca().transAxes, fontsize=14)

plt.xlabel("Phase [rad]", fontsize=14, labelpad=0.3)
plt.ylabel("Excited state probability", fontsize=14, labelpad=0.3)
plt.xlim(0,7)
plt.ylim(-0.05,1.05)
plt.legend(fontsize=10,loc=4)
plt.savefig("../figures/phase.pdf", bbox_inches="tight", pad_inches=0.15, dpi=1000)
