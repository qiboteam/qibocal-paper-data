import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

data = np.load("data/qubit1_punchout.npz")
WIDTH = 0.5

frequencies = data["0"]["freq"]
amplitudes = data["0"]["amp"]
magnitudes = data["0"]["signal"]

frequencies = np.array(list(dict.fromkeys(frequencies)))
amplitudes = np.array(list(dict.fromkeys(amplitudes)))
magnitudes = np.reshape(data["0"]["signal"], [len(amplitudes), len(frequencies)])

for i in range(magnitudes.shape[0]):
    min_val = magnitudes[i, :].min()
    max_val = magnitudes[i, :].max()
    magnitudes[i, :] = (magnitudes[i, :] - min_val) / (max_val - min_val)

fig, ax = plt.subplots(figsize=(10 * WIDTH, 10 * WIDTH * 6/8))

c = plt.pcolor(frequencies * 1e-9, amplitudes, magnitudes, cmap="coolwarm", rasterized=True)
plt.axvline(
    7.57465, 0.7, color="black", linestyle="dashed", label="Bare Resonator"
)
plt.axvline(
    7.5791,
    0,
    0.1,
    color="black",
    linestyle="dotted",
    # label="Dressed Resonator @ 7.579 GHz",
    label="Dressed Resonator",
)

plt.xlabel("Readout Frequency [GHz]", fontsize=14)
plt.ylabel("Readout Amplitude [a.u.]", fontsize=14)
plt.text(-0.1, 1.05, '(a)', transform=plt.gca().transAxes, fontsize=14)

ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))

colorbar = fig.colorbar(c)
colorbar.set_label("Normalized signal [a.u.]", fontsize=14)
plt.legend(loc=1, fontsize=10)
plt.savefig("../../qubit1_punchout.pdf", bbox_inches="tight", dpi=1000)

# QUBIT 2


data = np.load("data/qubit2_punchout.npz")

frequencies = data["0"]["freq"]
amplitudes = data["0"]["amp"]
magnitudes = data["0"]["signal"]

frequencies = np.array(list(dict.fromkeys(frequencies)))
amplitudes = np.array(list(dict.fromkeys(amplitudes)))
magnitudes = np.reshape(data["0"]["signal"], [len(amplitudes), len(frequencies)])

for i in range(magnitudes.shape[0]):
    min_val = magnitudes[i, :].min()
    max_val = magnitudes[i, :].max()
    magnitudes[i, :] = (magnitudes[i, :] - min_val) / (max_val - min_val)

fig, ax = plt.subplots()

c = plt.pcolor(frequencies * 1e-9, amplitudes, magnitudes, cmap="coolwarm")
plt.axvline(
    7.41645, 0.65, color="black", linestyle="dashed", label="Bare Resonator @ 7.416 GHz"
)
plt.axvline(
    7.4186,
    0,
    0.2,
    color="black",
    linestyle="dotted",
    label="Dressed Resonator @ 7.418 GHz",
)

plt.xlabel("Readout Frequency [GHz]")
plt.ylabel("Readout Amplitude [a.u.]")

colorbar = fig.colorbar(c)
colorbar.set_label("Normalized Magnitude [a.u.]")
plt.legend(loc=1, fontsize="10")
plt.savefig("qubit2_punchout.pdf", dpi=100)
