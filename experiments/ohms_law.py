import matplotlib.pyplot as plt
import numpy as np


def ohms_law_simulation(voltage, resistance):

    # Ohm's law
    current = voltage / resistance

    # Voltage range for graph
    voltages = np.linspace(0, max(voltage, 1), 100)

    currents = voltages / resistance

    fig, ax = plt.subplots()

    ax.plot(voltages, currents)

    ax.scatter([voltage], [current])

    ax.set_title("Ohm's Law")

    ax.set_xlabel("Voltage (V)")

    ax.set_ylabel("Current (A)")

    ax.grid(True)

    results = {"voltage": voltage, "resistance": resistance, "current": current}

    return fig, None, results
