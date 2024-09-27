import argparse
from qibocal.protocols.flux_dependence.utils import transmon_frequency as fit_function
import numpy as np
import json
import os
from pathlib import Path
import matplotlib.pyplot as plt

WIDTH = 0.33
FONT = 24

BLUE = "#788ae3"
RED = "#d1545e"
DARKBLUE = "#075cb3"
DARKRED = "#8c1822"

def extract_params (path, parameter, qubit):
    with open(path) as f:
        data = json.load(f)
    return data[parameter][qubit]

def main(args):
    path = args.data_path
    path_out = args.output_path
    qubit =  f"\"{args.qubit}\""
    remove_report = args.remove_report
    t1s = []
    t2s = []
    biases = []
    gate_infidelities = []
    fidelities = []

    reports = os.listdir(path)
    biases = [float(i.split("_")[-1]) for i in reports]
    reports = [x for _, x in sorted(zip(biases, reports))]
    biases = sorted(biases)


    with open(path+'/'+reports[0]+'/new_platform/parameters.json') as f:
        platform = json.load(f)
    platform_data = platform["characterization"]["single_qubit"][args.qubit]
    params_qubit = {
        "w_max": platform_data["drive_frequency"],  # FIXME: this is not the qubit frequency
        "xj": 0,
        "d": 0,
        "normalization": platform_data["crosstalk_matrix"][args.qubit],
        "offset": -platform_data["sweetspot"]*  platform_data["crosstalk_matrix"][args.qubit],  # Check is this the right one ???
        "crosstalk_element": 1,
        "charging_energy": platform_data["Ec"],
    }
    for i, report in enumerate(reports):
        if report not in remove_report:
            report_path = path + "/" + report
            results_path = Path(report_path+"/data/t1-0/results.json")
            if results_path.exists():
                t1s.append(extract_params(results_path,"\"t1\"", qubit))

            else:
                biases.remove(biases[i])

            results_path = Path(report_path+"/data/ramsey-2/results.json")
            if results_path.exists():
                t2s.append(extract_params(results_path,"\"t2\"", qubit))

            results_path = Path(report_path+"/data/readout_characterization-0/results.json")
            if results_path.exists():
                fidelities.append(extract_params(results_path,"\"fidelity\"", qubit))

            results_path = Path(report_path+"/data/rb_ondevice-0/results.json")
            if results_path.exists():
                pars = extract_params(results_path,"\"pars\"", qubit)

                cov = extract_params(results_path,"\"cov\"", qubit)
                stdevs = np.sqrt(np.diag(np.reshape(cov, (3, 3))))
                one_minus_p = 1 - pars[2]
                r_c = one_minus_p * (1 - 1 / 2**1)
                r_g = r_c / 1.875  # 1.875 is the average number of gates in clifford operation
                r_c_std = stdevs[2] * (1 - 1 / 2**1)
                r_g_std = r_c_std / 1.875
                gate_infidelities.append([r_g, r_g_std])
        else:
            biases.remove(biases[i])

    t1s = np.array(t1s)
    t2s = np.array(t2s)
    gate_infidelities = np.array(gate_infidelities)
    detuning = np.array([fit_function(b, **params_qubit) for b in biases])*1.e-9


    halfn = int(len(t1s)/2)


# Detuning vs t1
    plt.figure(figsize=(WIDTH * 10, WIDTH * 10 * 6/8))
    plt.plot(detuning[:halfn], t1s[:,0][:halfn]*1e-3, color=DARKRED, linewidth=0.7)
    plt.plot(detuning[halfn:], t1s[:,0][halfn:]*1e-3, color=DARKBLUE, linewidth=0.7)
    plt.errorbar(detuning[:halfn], t1s[:,0][:halfn]*1e-3, yerr = t1s[:,1][:halfn]*1e-3, fmt='o', markersize=4, color="black", markerfacecolor=RED, ecolor='black', markeredgewidth=0.7, elinewidth=0.7, alpha=1, label=r"$b < b_0$", capsize=3)
    plt.errorbar(detuning[halfn:], t1s[:,0][halfn:]*1e-3, yerr = t1s[:,1][halfn:]*1e-3, fmt='o', markersize=4, color="black", markerfacecolor=BLUE, ecolor='black', markeredgewidth=0.7, elinewidth=0.7, alpha=1, label=r"$b\geq b_0$", capsize=3)
    plt.xlabel('Frequency [GHz]', fontsize=12)
    plt.ylabel(r'$\text{T}_1$ [$\mu$s]', fontsize=12)
    plt.legend(loc=3)
    plt.savefig(path_out+'/t1_detuning.pdf', bbox_inches="tight", dpi=300)

# Detuning vs t2
    plt.figure(figsize=(WIDTH * 10, WIDTH * 10 * 6/8 - 0.1))
    plt.plot(detuning[:halfn], t2s[:,0][:halfn]*1e-3, color=DARKRED, linewidth=0.7)
    plt.plot(detuning[halfn:], t2s[:,0][halfn:]*1e-3, color=DARKBLUE, linewidth=0.7)
    plt.errorbar(detuning[:halfn], t2s[:,0][:halfn]*1e-3, yerr = t2s[:,1][:halfn]*1e-3, fmt='o', markersize=4, color="black", markerfacecolor=RED, ecolor='black', markeredgewidth=0.7, elinewidth=0.7, alpha=1, label=r"$b < b_0$", capsize=3)
    plt.errorbar(detuning[halfn:], t2s[:,0][halfn:]*1e-3, yerr = t2s[:,1][halfn:]*1e-3, fmt='o', markersize=4, color="black", markerfacecolor=BLUE, ecolor='black', markeredgewidth=0.7, elinewidth=0.7, alpha=1, label=r"$b\geq b_0$", capsize=3)
    plt.xlabel('Frequency [GHz]', fontsize=12)
    plt.ylabel(r'$\text{T}^*_2$ [$\mu$s]', fontsize=12)
    plt.legend()
    plt.savefig(path_out+'/t2_detuning.pdf', bbox_inches="tight", dpi=300)

# Bias vs t1
    plt.figure()
    plt.errorbar(biases, t1s[:,0]*1e-3, yerr = t1s[:,1]*1e-3,fmt='--o', markersize=4, markerfacecolor='red', ecolor='black')
    plt.xlabel('bias [V]')
    plt.ylabel(r'$T_1$ [$\mu$s]')
    plt.savefig(path_out+'/t1_bias.pdf')

# Bias vs t2
    plt.figure()
    plt.errorbar(biases, t2s[:,0]*1e-3,yerr = t2s[:,1]*1e-3, fmt='--o', markersize=4, markerfacecolor='red', ecolor='black')
    plt.xlabel('bias [V]')
    plt.ylabel(r'$T_2$ [$\mu$s]')
    plt.savefig(path_out + '/t2_bias.pdf')

# Bias vs gate infidelity
    plt.figure()
    plt.errorbar(biases, gate_infidelities[:,0],yerr = gate_infidelities[:,1]*1e-3, fmt='--o', markersize=4, markerfacecolor='red', ecolor='black')
    plt.xlabel('bias [V]')
    plt.ylabel(r'gate infidelities')
    plt.savefig(path_out + '/gate_inf_bias.pdf')

#Bias vs fidelity
    plt.figure(figsize=(WIDTH * 10, WIDTH * 10 * 6/8))
    plt.plot(detuning[:halfn], fidelities[:halfn], markersize=4, color=DARKRED, linewidth=0.7)
    plt.plot(detuning[halfn:], fidelities[halfn:], markersize=4, color=DARKBLUE, linewidth=0.7)
    plt.plot(detuning[:halfn], fidelities[:halfn], markersize=4, markerfacecolor=RED, marker="o", color="BLACK", linewidth=0.7, ls="", label=r"$b<b_0$")
    plt.plot(detuning[halfn:], fidelities[halfn:], markersize=4, markerfacecolor=BLUE, marker="o", color="BLACK", linewidth=0.7, ls="", label=r"$b\geq b_0$")
    plt.xlabel('Frequency [GHz]', fontsize=12)
    plt.ylabel(r'Readout Fidelity', fontsize=12)
    plt.legend(loc=3)
    plt.savefig(path_out + '/ro_fidelity_detuning.pdf', bbox_inches="tight")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str)
    parser.add_argument("--output_path", type=str)
    parser.add_argument("--qubit", type=str)
    parser.add_argument("--remove_report", default = None, type=str)
    args = parser.parse_args()
    if args.remove_report is None:
        args.remove_report = []
    main(args)
