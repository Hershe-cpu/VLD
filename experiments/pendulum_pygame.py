import math
import sys

import pygame


def run_pendulum_animation(length, gravity, angle):

    pygame.init()
    pygame.font.init()

    # --------------------------------------------------
    # WINDOW
    # --------------------------------------------------

    WIDTH = 1000
    HEIGHT = 600

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Pendulum - Virtual Lab")

    clock = pygame.time.Clock()

    # --------------------------------------------------
    # COLORS
    # --------------------------------------------------

    SKY = (225, 240, 250)
    GRID = (190, 200, 210)
    AXIS = (40, 40, 40)
    ROD = (50, 70, 90)
    BOB = (220, 50, 50)
    PIVOT = (30, 30, 30)
    TEXT = (30, 30, 30)
    PANEL_BORDER = (150, 160, 170)

    # --------------------------------------------------
    # PANEL
    # --------------------------------------------------

    PANEL_X = 760
    PANEL_WIDTH = WIDTH - PANEL_X

    # --------------------------------------------------
    # FONTS
    # --------------------------------------------------

    font = pygame.font.SysFont("Arial", 16)

    title_font = pygame.font.SysFont("Arial", 24, bold=True)

    small_font = pygame.font.SysFont("Arial", 14)

    # --------------------------------------------------
    # PHYSICS
    # --------------------------------------------------

    angle_rad = math.radians(angle)

    angular_frequency = math.sqrt(gravity / length)

    period = 2 * math.pi * math.sqrt(length / gravity)

    # --------------------------------------------------
    # COORDINATE SYSTEM
    # --------------------------------------------------

    pivot_x = 380
    pivot_y = 120

    # Scale physical length to pixels
    max_display_length = 350

    scale = max_display_length / max(length, 0.1)

    # --------------------------------------------------
    # ANIMATION STATE
    # --------------------------------------------------

    start_time = pygame.time.get_ticks()

    simulation_complete = False

    running = True

    # --------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------

    while running:
        # --------------------------------------------------
        # EVENTS
        # --------------------------------------------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r:
                    start_time = pygame.time.get_ticks()

                    simulation_complete = False

        # --------------------------------------------------
        # TIME
        # --------------------------------------------------

        elapsed = (pygame.time.get_ticks() - start_time) / 1000

        # Run for several oscillations
        simulation_duration = period

        if not simulation_complete:
            t = min(elapsed, simulation_duration)

            if t >= simulation_duration:
                t = simulation_duration
                simulation_complete = True

        else:
            t = simulation_duration

        # --------------------------------------------------
        # PENDULUM PHYSICS
        # --------------------------------------------------

        theta = angle_rad * math.cos(angular_frequency * t)

        # Angular velocity
        omega = -angle_rad * angular_frequency * math.sin(angular_frequency * t)

        # Convert to pixels
        bob_x = pivot_x + length * scale * math.sin(theta)

        bob_y = pivot_y + length * scale * math.cos(theta)

        # --------------------------------------------------
        # BACKGROUND
        # --------------------------------------------------

        screen.fill(SKY)

        # --------------------------------------------------
        # GRID
        # --------------------------------------------------

        for x in range(0, PANEL_X, 50):
            pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT), 1)

        for y in range(0, HEIGHT, 50):
            pygame.draw.line(screen, GRID, (0, y), (PANEL_X, y), 1)

        # --------------------------------------------------
        # GROUND / REFERENCE LINE
        # --------------------------------------------------

        reference_y = pivot_y + length * scale

        pygame.draw.line(
            screen, GRID, (80, int(reference_y)), (PANEL_X - 30, int(reference_y)), 2
        )

        # --------------------------------------------------
        # ANGLE REFERENCE
        # --------------------------------------------------

        pygame.draw.line(
            screen, AXIS, (pivot_x, pivot_y), (pivot_x, int(reference_y)), 2
        )

        # --------------------------------------------------
        # PENDULUM ROD
        # --------------------------------------------------

        pygame.draw.line(screen, ROD, (pivot_x, pivot_y), (int(bob_x), int(bob_y)), 6)

        # --------------------------------------------------
        # PIVOT
        # --------------------------------------------------

        pygame.draw.circle(screen, PIVOT, (pivot_x, pivot_y), 10)

        # --------------------------------------------------
        # BOB
        # --------------------------------------------------

        pygame.draw.circle(screen, BOB, (int(bob_x), int(bob_y)), 18)

        # --------------------------------------------------
        # ANGLE ARC
        # --------------------------------------------------

        arc_radius = 70

        arc_rect = pygame.Rect(
            pivot_x - arc_radius, pivot_y - arc_radius, arc_radius * 2, arc_radius * 2
        )

        # Draw only when there is an angle
        if abs(theta) > 0.01:
            if theta > 0:
                start_angle = math.pi / 2 - theta
                end_angle = math.pi / 2

            else:
                start_angle = math.pi / 2
                end_angle = math.pi / 2 - theta

        # --------------------------------------------------
        # ANGLE LABEL
        # --------------------------------------------------

        angle_text = font.render(f"θ = {math.degrees(theta):.1f}°", True, TEXT)

        screen.blit(angle_text, (pivot_x + 75, pivot_y - 45))

        # --------------------------------------------------
        # RIGHT INFORMATION PANEL
        # --------------------------------------------------

        pygame.draw.rect(screen, SKY, (PANEL_X, 0, PANEL_WIDTH, HEIGHT))

        # Panel separator
        pygame.draw.line(screen, PANEL_BORDER, (PANEL_X, 0), (PANEL_X, HEIGHT), 2)

        # --------------------------------------------------
        # PANEL TITLE
        # --------------------------------------------------

        panel_title = title_font.render("Parameters", True, TEXT)

        screen.blit(panel_title, (PANEL_X + 15, 25))

        # --------------------------------------------------
        # INFORMATION
        # --------------------------------------------------

        info = [
            f"Length: {length:.2f} m",
            f"Gravity: {gravity:.2f} m/s²",
            f"Initial Angle: {angle:.1f}°",
            "",
            f"Time: {t:.2f} s",
            f"Angle: {math.degrees(theta):.2f}°",
            f"Angular Velocity: {omega:.3f} rad/s",
            "",
            "Model: Small Angle",
        ]
        for i, text in enumerate(info):
            rendered = font.render(text, True, TEXT)
            screen.blit(rendered, (PANEL_X + 15, 70 + i * 25))

            # SIMULATION STATUS #

            if simulation_complete:
                replay_text = font.render("Press R to Replay", True, TEXT)

                screen.blit(replay_text, (PANEL_X + 15, HEIGHT - 40))

                # AXIS / LABELS #

                x_label = small_font.render("Vertical Reference", True, TEXT)
                screen.blit(x_label, (pivot_x + 10, int(reference_y) + 10))

                # UPDATE SCREEN #

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

    # COMMAND LINE ENTRY #


if __name__ == "__main__":
    print("Starting pendulum animation...")
    if len(sys.argv) < 4:
        print("Usage:")
        print("python experiments/pendulum_pygame.py LENGTH GRAVITY ANGLE")
        sys.exit(1)
    length = float(sys.argv[1])
    gravity = float(sys.argv[2])
    angle = float(sys.argv[3])
    print(f"Length = {length}")
    print(f"Gravity = {gravity}")
    print(f"Angle = {angle}")
    run_pendulum_animation(length, gravity, angle)
