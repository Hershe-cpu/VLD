import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def projectile_simulation(
    velocity,
    angle,
    gravity,
    height
):
    """
    Simulates projectile motion.

    Parameters
    ----------
    velocity : float
        Initial velocity in m/s

    angle : float
        Launch angle in degrees

    gravity : float
        Acceleration due to gravity

    height : float
        Initial height in metres
    """

    # Convert degrees to radians
    theta = np.radians(angle)

    # Initial velocity components
    vx = velocity * np.cos(theta)
    vy = velocity * np.sin(theta)

    # Calculate flight time using:
    #
    # y = h + vy*t - 1/2*g*t²
    #
    # We find when y = 0.

    discriminant = (
        vy**2 + 2 * gravity * height
    )

    flight_time = (
        vy + np.sqrt(discriminant)
    ) / gravity

    # Time values
    t = np.linspace(
        0,
        flight_time,
        100
    )

    # Position equations

    x = vx * t

    y = (
        height
        + vy * t
        - 0.5 * gravity * t**2
    )

    # Maximum height
    max_height = np.max(y)

    # Range
    max_range = np.max(x)

    # -----------------------------------------------------
    # CREATE FIGURE
    # -----------------------------------------------------

    fig, ax = plt.subplots()

    ax.set_xlim(
        0,
        max_range * 1.1
    )

    ax.set_ylim(
        0,
        max_height * 1.2
    )

    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")

    ax.set_title("Projectile Motion")

    # Complete trajectory
    ax.plot(
        x,
        y,
        linestyle="--",
        alpha=0.5
    )

    # Animated object
    ball, = ax.plot(
        [],
        [],
        marker="o",
        markersize=10
    )

    def update(frame):

        ball.set_data(
            [x[frame]],
            [y[frame]]
        )

        return ball,

    animation = FuncAnimation(
        fig,
        update,
        frames=len(t),
        interval=30,
        blit=True
    )

    return (
        fig,
        animation,
        {
            "flight_time": flight_time,
            "maximum_height": max_height,
            "range": max_range
        }
    )