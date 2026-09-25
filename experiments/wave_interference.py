import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def wave_interference_simulation(amplitude=1.0, wavelength=2.0, frequency=1.0):

    # Wave number
    k = 2 * np.pi / wavelength

    # Angular frequency
    omega = 2 * np.pi * frequency

    # Position
    x = np.linspace(0, 10, 500)

    # Time
    t = np.linspace(0, 2, 150)

    fig, ax = plt.subplots()

    ax.set_title("Wave Interference")

    ax.set_xlabel("Position")

    ax.set_ylabel("Amplitude")

    ax.set_xlim(0, 10)

    ax.set_ylim(-2.5 * amplitude, 2.5 * amplitude)

    ax.grid(True)

    (wave1,) = ax.plot([], [], label="Wave 1")

    (wave2,) = ax.plot([], [], label="Wave 2")

    (resultant,) = ax.plot([], [], label="Resultant", linewidth=2)

    ax.legend()

    def update(frame):

        current_time = t[frame]

        y1 = amplitude * np.sin(k * x - omega * current_time)

        y2 = amplitude * np.sin(k * x - omega * current_time)

        y_result = y1 + y2

        wave1.set_data(x, y1)

        wave2.set_data(x, y2)

        resultant.set_data(x, y_result)

        return wave1, wave2, resultant

    animation = FuncAnimation(fig, update, frames=len(t), interval=40, blit=True)

    results = {
        "amplitude_each_wave": amplitude,
        "resultant_amplitude": 2 * amplitude,
        "wavelength": wavelength,
        "frequency": frequency,
        "interference_type": "Constructive interference",
    }

    return fig, animation, results
