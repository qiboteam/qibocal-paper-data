"""
Run as 
python rb_neldermead.py --platform qw11q --targets D1 --output qw11q/neldermead
"""

import argparse

import numpy as np
from qibolab.qubits import QubitId
from scipy.optimize import minimize

from qibocal.cli.report import report
from qibocal.auto.execute import Executor

NUM_OF_SEQUENCES = int(1e2)
MAX_CIRCUIT_DEPTH = 512
DELTA_CLIFFORD = 1
LOGARITHMIC = True
SAVE_SEQUENCES = False
NAVG = 512

MAXFEV = 30
DETUNE_PERCENT = 8.75 #10

def rb_infidelity(x, e, target):

    # print(f'trying amplitude: {float(amplitude)}...\n')

    amplitude = float(x[0])
    drag_param = float(x[1])

    e.platform.qubits[target].native_gates.RX.amplitude = float(amplitude)
    e.platform.qubits[target].native_gates.RX.shape = f"Drag(5, {drag_param})"

    rb_output = e.rb_ondevice(
        logarithmic = LOGARITHMIC,
        apply_inverse=True,
        delta_clifford=DELTA_CLIFFORD,
        max_circuit_depth=MAX_CIRCUIT_DEPTH,
        n_avg=NAVG,
        num_of_sequences=NUM_OF_SEQUENCES,
        save_sequences=SAVE_SEQUENCES,
        state_discrimination=True,
    )

    one_minus_p = 1 - rb_output.results.pars.get(target)[2]
    r_c = one_minus_p * (1 - 1 / 2**1)
    r_g = r_c / 1.875

    # if r_g < 1e-5:
    #     r_g = 1e-2

    print()
    print()
    print(f"trying amplitude: {float(amplitude)}...\n")
    print(f"trying drag param: {float(drag_param)}...\n")
    print(f"           reached infidelity: {r_g}\n")
    print()

    return r_g


def main(targets: list[QubitId], platform_name: str, output: str):

    with Executor.open(
        "myexec",
        path=output,
        platform=platform_name,
        targets=targets,
        update=False,
        force=True,
    ) as e:
        platform = e.platform

        target = targets[0]
        amplitude0 =  e.platform.qubits[target].native_gates.RX.amplitude 
        amplitude0 = amplitude0 - amplitude0 * DETUNE_PERCENT/100
        e.platform.qubits[target].native_gates.RX.amplitude = float(amplitude0)
        drag_param0 = 0.035

        bnds = [(0.035, 0.045), (-0.05, 0.05)]

        x0 = np.array([amplitude0, drag_param0])


        res = minimize(
            rb_infidelity,
            x0,
            args=(e, target),
            method="Nelder-Mead",
            tol=1e-7,
            bounds=bnds,
            options={"maxfev": MAXFEV, "disp": True},
        )

        print(res)
        print()
        print(res.x)

        # report(e.path, e.history)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Qubit recalibration")
    parser.add_argument("--platform", type=str, help="Qibo platform")
    parser.add_argument("--output", type=str, help="Output folder")
    parser.add_argument(
        "--targets", nargs="+", help="Target qubit to recalibrate", required=True
    )

    args = parser.parse_args()
    main(targets=args.targets, platform_name=args.platform, output=args.output)
