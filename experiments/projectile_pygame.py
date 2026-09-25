import pygame
import math


def run_projectile_animation(velocity, angle, gravity, height):

    pygame.init()

    # Window
    WIDTH = 1000
    HEIGHT = 600

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Projectile Motion - Virtual Lab")

    clock = pygame.time.Clock()

    # Colors
    SKY = (225, 240, 250)
    GROUND = (80, 120, 80)
    BALL = (220, 50, 50)
    TRAJECTORY = (50, 80, 200)
    TEXT = (30, 30, 30)
    GRID = (190, 200, 210)

    # Physics
    angle_rad = math.radians(angle)

    vx = velocity * math.cos(angle_rad)
    vy = velocity * math.sin(angle_rad)

    # Time of flight
    flight_time = (
        vy + math.sqrt(vy**2 + 2 * gravity * height)
    ) / gravity

    # Maximum height
    max_height = (
        height + vy**2 / (2 * gravity)
    )

    # Range
    range_distance = vx * flight_time

    # Scale the physics world to the window
    margin_left = 80
    margin_bottom = 80

    usable_width = WIDTH - margin_left - 50
    usable_height = HEIGHT - margin_bottom - 50

    scale_x = usable_width / max(range_distance, 1)
    scale_y = usable_height / max(max_height, 1)

    scale = min(scale_x, scale_y)

    # Fonts
    font = pygame.font.SysFont("Arial", 20)
    title_font = pygame.font.SysFont(
        "Arial",
        28,
        bold=True
    )

    # Animation
    start_time = pygame.time.get_ticks()

    trajectory_points = []

    running = True

    while running:

        # Handle window events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        # Current time
        elapsed = (
            pygame.time.get_ticks() - start_time
        ) / 1000

        # Slow down animation slightly
        t = min(elapsed * 0.8, flight_time)

        # Projectile position
        x = vx * t

        y = (
            height
            + vy * t
            - 0.5 * gravity * t**2
        )

        y = max(y, 0)

        # Convert physics coordinates
        # into screen coordinates

        screen_x = (
            margin_left + x * scale
        )

        ground_y = HEIGHT - margin_bottom

        screen_y = (
            ground_y - y * scale
        )

        # Save trajectory
        trajectory_points.append(
            (screen_x, screen_y)
        )

        # Background
        screen.fill(SKY)

        # Grid
        for i in range(0, WIDTH, 50):

            pygame.draw.line(
                screen,
                GRID,
                (i, 0),
                (i, HEIGHT),
                1
            )

        for i in range(0, HEIGHT, 50):

            pygame.draw.line(
                screen,
                GRID,
                (0, i),
                (WIDTH, i),
                1
            )

        # Ground
        pygame.draw.line(
            screen,
            GROUND,
            (0, ground_y),
            (WIDTH, ground_y),
            5
        )

        # Trajectory
        if len(trajectory_points) > 1:

            pygame.draw.lines(
                screen,
                TRAJECTORY,
                False,
                trajectory_points,
                3
            )

        # Projectile
        pygame.draw.circle(
            screen,
            BALL,
            (int(screen_x), int(screen_y)),
            12
        )

        # Title
        title = title_font.render(
            "Projectile Motion",
            True,
            TEXT
        )

        screen.blit(
            title,
            (30, 20)
        )

        # Information
        info = [
            f"Velocity: {velocity:.1f} m/s",
            f"Angle: {angle:.1f}°",
            f"Gravity: {gravity:.2f} m/s²",
            f"Time: {t:.2f} s",
            f"X: {x:.2f} m",
            f"Y: {y:.2f} m",
        ]

        for i, text in enumerate(info):

            rendered = font.render(
                text,
                True,
                TEXT
            )

            screen.blit(
                rendered,
                (30, 70 + i * 28)
            )

        # Velocity vector
        vector_length = 50

        vector_x = (
            math.cos(angle_rad)
            * vector_length
        )

        vector_y = (
            -math.sin(angle_rad)
            * vector_length
        )

        pygame.draw.line(
            screen,
            (0, 100, 0),
            (screen_x, screen_y),
            (
                screen_x + vector_x,
                screen_y + vector_y
            ),
            4
        )

        # Update screen
        pygame.display.flip()

        clock.tick(60)

        # Finish animation
        if elapsed >= flight_time + 1:

            pygame.time.wait(1000)

            running = False

    pygame.quit()