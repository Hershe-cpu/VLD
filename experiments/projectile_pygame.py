import math

import pygame


def run_projectile_animation(velocity, angle, gravity, height):

    pygame.init()

    # Window
    WIDTH = 1000
    HEIGHT = 600

    # Right-side information panel
    PANEL_X = 760
    PANEL_WIDTH = 220

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
    flight_time = (vy + math.sqrt(vy**2 + 2 * gravity * height)) / gravity

    # Maximum height
    max_height = height + vy**2 / (2 * gravity)

    # Range
    range_distance = vx * flight_time

    # Scale the physics world to the window
    margin_left = 80
    margin_bottom = 80

    usable_width = PANEL_X - margin_left - 30
    usable_height = HEIGHT - margin_bottom - 50

    scale_x = usable_width / max(range_distance, 1)
    scale_y = usable_height / max(max_height, 1)

    scale = min(scale_x, scale_y)

    # Fonts
    font = pygame.font.SysFont("Arial", 20)
    title_font = pygame.font.SysFont("Arial", 28, bold=True)

    # Animation
    start_time = pygame.time.get_ticks()

    trajectory_points = []

    running = True
    simulation_complete = False

    while running:
        # Handle window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r:
                    start_time = pygame.time.get_ticks()
                    trajectory_points = []
                    simulation_complete = False

        # Current time
        elapsed = (pygame.time.get_ticks() - start_time) / 1000

        # Slow down animation slightly
        if not simulation_complete:
            t = min(elapsed * 0.8, flight_time)

            if t >= flight_time:
                t = flight_time
                simulation_complete = True

        else:
            t = flight_time

        # Projectile position
        x = vx * t

        y = height + vy * t - 0.5 * gravity * t**2

        y = max(y, 0)

        # Convert physics coordinates
        # into screen coordinates

        screen_x = margin_left + x * scale

        ground_y = HEIGHT - margin_bottom

        screen_y = ground_y - y * scale

        # Save trajectory
        trajectory_points.append((screen_x, screen_y))

        # Background
        screen.fill(SKY)

        # Grid
        for i in range(0, WIDTH, 50):
            pygame.draw.line(screen, GRID, (i, 0), (i, HEIGHT), 1)

        for i in range(0, HEIGHT, 50):
            pygame.draw.line(screen, GRID, (0, i), (WIDTH, i), 1)
        # Coordinate system
        axis_x = margin_left
        axis_y = ground_y

        AXIS = (40, 40, 40)

        # X-axis
        pygame.draw.line(screen, AXIS, (axis_x, axis_y), (WIDTH - 70, axis_y), 3)

        # Y-axis
        pygame.draw.line(screen, AXIS, (axis_x, axis_y), (axis_x, 40), 3)

        # X-axis arrow
        pygame.draw.polygon(
            screen,
            AXIS,
            [(WIDTH - 20, axis_y), (WIDTH - 35, axis_y - 7), (WIDTH - 35, axis_y + 7)],
        )

        # Y-axis arrow
        pygame.draw.polygon(
            screen, AXIS, [(axis_x, 30), (axis_x - 7, 45), (axis_x + 7, 45)]
        )

        # X-axis tick marks and labels

        if range_distance > 100 and range_distance < 300:
            x_step = 20
        elif range_distance > 300 and range_distance < 500:
            x_step = 25
        elif range_distance > 500:
            x_step = 100
        else:
            x_step = 5

        for value in range(0, int(range_distance) + x_step, x_step):
            tick_x = axis_x + value * scale

            if tick_x < WIDTH - 30:
                pygame.draw.line(
                    screen, AXIS, (tick_x, axis_y - 5), (tick_x, axis_y + 5), 2
                )

                label = font.render(str(value), True, TEXT)

                screen.blit(label, (tick_x - 6, axis_y + 10))

        # Y-axis tick marks and labels

        if 100 < max_height < 500:
            y_step = 20
        elif max_height > 500:
            y_step = 25
        elif max_height > 50:
            y_step = 10
        else:
            y_step = 5

        for value in range(0, int(max_height) + y_step, y_step):
            tick_y = axis_y - value * scale

            if tick_y > 40:
                pygame.draw.line(
                    screen, AXIS, (axis_x - 5, tick_y), (axis_x + 5, tick_y), 2
                )

                label = font.render(str(value), True, TEXT)

                screen.blit(label, (axis_x - 35, tick_y - 10))

        # Axis labels

        x_label = font.render("X (m)", True, TEXT)

        y_label = font.render("Y (m)", True, TEXT)

        screen.blit(x_label, (WIDTH - 80, axis_y + 35))

        screen.blit(y_label, (axis_x - 45, 20))

        # Ground
        pygame.draw.line(screen, GROUND, (0, ground_y), (WIDTH, ground_y), 5)

        # Trajectory
        if len(trajectory_points) > 1:
            pygame.draw.lines(screen, TRAJECTORY, False, trajectory_points, 3)

        # Projectile
        pygame.draw.circle(screen, BALL, (int(screen_x), int(screen_y)), 12)

        # Information

        current_vx = vx
        current_vy = vy - gravity * t

        # Right-side information panel

        pygame.draw.rect(screen, SKY, (PANEL_X, 0, PANEL_WIDTH, HEIGHT))

        # Panel title
        panel_title = title_font.render("Parameters", True, TEXT)

        screen.blit(panel_title, (PANEL_X + 15, 30))

        # Information
        info = [
            f"Initial Velocity: {velocity:.1f} m/s",
            f"Launch Angle: {angle:.1f}°",
            f"Gravity: {gravity:.2f} m/s²",
            "",
            f"Time: {t:.2f} s",
            f"Vx: {current_vx:.2f} m/s",
            f"Vy: {current_vy:.2f} m/s",
            "",
            f"Max Height: {max_height:.2f} m",
            f"Range: {range_distance:.2f} m",
            f"Flight Time: {flight_time:.2f} s",
        ]

        for i, text in enumerate(info):
            rendered = font.render(text, True, TEXT)

            screen.blit(rendered, (PANEL_X + 15, 65 + i * 25))

        if simulation_complete:
            complete_text = font.render("\n             Press R to Replay", True, TEXT)
            screen.blit(complete_text, (PANEL_X + 15, HEIGHT - 60))

        # Update screen
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    import sys

    velocity = float(sys.argv[1])
    angle = float(sys.argv[2])
    gravity = float(sys.argv[3])
    height = float(sys.argv[4])

    run_projectile_animation(velocity, angle, gravity, height)
