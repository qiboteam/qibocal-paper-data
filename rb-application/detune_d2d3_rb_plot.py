import numpy as np
import matplotlib.pyplot as plt
import os
import json


WIDTH  = 0.5
FONT = 24

BLUE = "#788ae3"
RED = "#d1545e"
DARKBLUE = "#075cb3"
DARKRED = "#8c1822"

#####################################
# MAKE SURE TO UNZIP THE FILE FIRST #
#####################################
overall_path = f'../data/detune_rb/'
path = f"{overall_path}data/"
rb_paths = [item for item in os.listdir(path) if item.startswith('rb_ondevice')]
sorted_rb_items = sorted(rb_paths, key=lambda x: int(x.split('-')[1]))

all_decay_params, all_decay_errs = [], []
for rbpath in sorted_rb_items:
    with open(f"{path}{rbpath}/results.json") as f:
        data_dict = json.load(f)
    popt = data_dict['"pars"']['"D1"']
    pcov = np.array(data_dict['"cov"']['"D1"']).reshape(3,3)
    perr = np.sqrt(np.diag(pcov))
    all_decay_params.append(popt[2])
    all_decay_errs.append(perr[2])

all_decay_params, all_decay_errs = np.array(all_decay_params), np.array(all_decay_errs)

tot_points = len(sorted_rb_items)
mask = np.zeros(tot_points).astype(bool)
mask[2::4] = True
mask[3::4] = True
mask[1] = True
decay_params_plot = all_decay_params[mask]
decay_errs_plot = all_decay_errs[mask]

infidelity = (1 - decay_params_plot) / 2
pulse_fidelities = 1 - infidelity / 1.875

pulse_fidelities_err = decay_errs_plot / decay_params_plot * pulse_fidelities



with open(f"{overall_path}biases.txt") as f:
    all_biases = np.loadtxt(f)
all_biases_plot = all_biases[1::2]
all_biases_plot

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

x = np.arange(1, len(pulse_fidelities) + 1)
fig, ax1 = plt.subplots(1, figsize=(WIDTH * 10, WIDTH * 10 * 6/8))

ax2 = ax1.twinx()
# ax2.plot(x, np.repeat(all_biases_plot[:,0],2), linewidth=0.7, label="qubit 2")
ax2.plot(
    x,
    np.append(all_biases_plot[0,1], np.repeat(all_biases_plot[:,1],2)),
    linewidth=0.7, label="qubit 3",
    color=DARKBLUE
)
ax2.set_ylim(-0.204, 0.199)
ax2.set_ylabel('flux', fontsize=12)
# ax2.legend(loc='center', bbox_to_anchor=(0.48, 0.45))
ax2.text(0.9, -0.13, "flux qubit 3", color=DARKBLUE)
# ax2.text(0.5, -0.41, "flux qubit 2", color=colors[0])

ax1.errorbar(x[1::2], pulse_fidelities[1::2], yerr = pulse_fidelities_err[1::2], fmt='o',linestyle='none', markersize=4, color="black", markerfacecolor=RED, ecolor="black", markeredgewidth=0.7,  alpha=1, label=r"before re-calibration", capsize=3, elinewidth=0.7)
ax1.errorbar(x[::2], pulse_fidelities[::2], yerr = pulse_fidelities_err[::2], fmt='o',linestyle='none', markersize=4, color="black", markerfacecolor=BLUE, ecolor="black", markeredgewidth=0.7, alpha=1, label="after re-calibration", capsize=3, elinewidth=0.7)
ax1.plot(x, pulse_fidelities, '-', color="black", linewidth=0.7)
ax1.set_xlabel('time step',  fontsize=12)
ax1.set_ylabel(r'$\pi/2$ fidelity',  fontsize=12)


ax1.legend(loc=6)
plt.savefig(f'../figures/detune_d2d3_rb_plot.pdf', bbox_inches="tight", dpi=600)
