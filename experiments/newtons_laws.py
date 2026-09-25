import matplotlib.pyplot as plt
import numpy as np


def newtons_law_simulation(mass, force):

    # Newton's second law
    acceleration = force / mass

    # Time
    t = np.linspace(0, 10, 200)

    # Initial velocity = 0
    initial_velocity = 0

    # Position
    position = initial_velocity * t + 0.5 * acceleration * t**2

    # Velocity
    velocity = initial_velocity + acceleration * t

    fig, ax = plt.subplots()

    ax.plot(t, position, label="Position")

    ax.set_title("Newton's Second Law")

    ax.set_xlabel("Time (s)")

    ax.set_ylabel("Position (m)")

    ax.grid(True)

    ax.legend()

    results = {
        "mass": mass,
        "force": force,
        "acceleration": acceleration,
        "final_velocity": velocity[-1],
        "final_position": position[-1],
    }

    return fig, None, results
