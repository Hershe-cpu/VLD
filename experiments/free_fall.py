import numpy as np
import matplotlib.pyplot as plt


def free_fall_simulation(
    height,
    gravity=9.81
):

    # Time required to fall
    fall_time = np.sqrt(
        2 * height / gravity
    )

    # Time values
    t = np.linspace(
        0,
        fall_time,
        200
    )

    # Height during fall
    y = (
        height
        - 0.5 * gravity * t**2
    )

    # Velocity
    velocity = gravity * t

    fig, ax = plt.subplots()

    ax.plot(
        t,
        y
    )

    ax.set_title(
        "Free Fall"
    )

    ax.set_xlabel(
        "Time (s)"
    )

    ax.set_ylabel(
        "Height (m)"
    )

    ax.grid(True)

    results = {
        "initial_height": height,
        "gravity": gravity,
        "fall_time": fall_time,
        "final_velocity": velocity[-1]
    }

    return fig, None, results