import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def circular_motion_simulation(radius, velocity):

    # Angular velocity
    omega = velocity / radius

    # Centripetal acceleration
    centripetal_acceleration = velocity**2 / radius

    # Time
    period = 2 * np.pi / omega

    t = np.linspace(0, 2 * period, 200)

    # Circular coordinates
    theta = omega * t

    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    fig, ax = plt.subplots()

    ax.set_title("Uniform Circular Motion")

    ax.set_xlim(-radius * 1.3, radius * 1.3)

    ax.set_ylim(-radius * 1.3, radius * 1.3)

    ax.set_aspect("equal")

    ax.grid(True)

    (circle,) = ax.plot(x, y, linestyle="--")

    (point,) = ax.plot([], [], "o")

    def update(frame):

        point.set_data([x[frame]], [y[frame]])

        return (point,)

    animation = FuncAnimation(fig, update, frames=len(t), interval=30, blit=True)

    results = {
        "radius": radius,
        "velocity": velocity,
        "angular_velocity": omega,
        "centripetal_acceleration": centripetal_acceleration,
        "period": period,
    }

    return fig, animation, results
