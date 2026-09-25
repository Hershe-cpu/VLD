import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def pendulum_simulation(length, gravity=9.81, angle=15):

    # Convert angle to radians
    theta0 = np.radians(angle)

    # Small-angle approximation
    period = 2 * np.pi * np.sqrt(length / gravity)

    # Time
    t = np.linspace(0, 2 * period, 200)

    # Angular displacement
    theta = theta0 * np.cos(np.sqrt(gravity / length) * t)

    # Pendulum coordinates
    x = length * np.sin(theta)
    y = -length * np.cos(theta)

    fig, ax = plt.subplots()

    ax.set_title("Simple Pendulum")

    ax.set_xlim(-length * 1.3, length * 1.3)

    ax.set_ylim(-length * 1.3, length * 0.3)

    ax.set_aspect("equal")

    ax.grid(True)

    (line,) = ax.plot([], [], "o-", linewidth=2)

    def update(frame):

        line.set_data([0, x[frame]], [0, y[frame]])

        return (line,)

    animation = FuncAnimation(fig, update, frames=len(t), interval=30, blit=True)

    results = {
        "period": period,
        "length": length,
        "gravity": gravity,
        "initial_angle": angle,
    }

    return fig, animation, results
