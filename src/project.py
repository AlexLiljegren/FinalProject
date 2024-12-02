import pygame
import sys

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
RED_FILTER = (255, 0, 0)
GREEN_FILTER = (0, 255, 0)
BLUE_FILTER = (0, 0, 255)

# Load image sequences for multiple animations
frame_count_1 = 32
frame_count_2 = 32

# Function to initialize the game
def initialize_game():
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))  # Default windowed mode
    pygame.display.set_caption("Alexander Liljegren Final Project")

    frames_1 = [pygame.image.load(f"Fatalis_Final{i}.png") for i in range(1, frame_count_1 + 1)]

    frames_2 = [pygame.image.load(f"Fatalis_Final_Fire{i}.png") for i in range(1, frame_count_2 + 1)]

    return screen, frames_1, frames_2, screen_width, screen_height

# Function to handle user input (key presses)
def handle_input(event, paused, fullscreen, current_filter, frames_1, frames_2, current_frames, frame_count, screen, screen_width, screen_height):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:  
            current_frames = frames_1
            frame_count = len(frames_1)
        elif event.key == pygame.K_f:  
            current_frames = frames_2
            frame_count = len(frames_2)
        elif event.key == pygame.K_F11:
            fullscreen = not fullscreen  # Toggle fullscreen state
            if fullscreen:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                screen_width, screen_height = pygame.display.get_surface().get_size()
            else:
                screen = pygame.display.set_mode((800, 600))  # Return to windowed mode
                screen_width, screen_height = 800, 600  # Reset screen size back to windowed size
        elif event.key == pygame.K_SPACE:
            paused = not paused

    return paused, fullscreen, current_filter, current_frames, frame_count, screen, screen_width, screen_height

# Function to apply the color filter to an image
def apply_color_filter(image, color_filter):
    # Create a new surface with the same size as the image
    filtered_image = image.copy()

    # Apply the filter by filling the surface with the color filter
    filtered_image.fill(color_filter, special_flags=pygame.BLEND_RGBA_MULT)

    return filtered_image

# Function to update the animation frame (only if not paused)
def update_animation(current_frame, frame_count, last_update_time, frame_rate, paused):
    current_time = pygame.time.get_ticks()

    if not paused:
        if current_time - last_update_time > frame_rate:
            current_frame = (current_frame + 1) % frame_count
            last_update_time = current_time

    return current_frame, last_update_time

# Main game loop
def main():
    screen, frames_1, frames_2, screen_width, screen_height = initialize_game()

    current_frames = frames_1
    frame_count = len(frames_1)
    current_frame = 0
    last_update_time = pygame.time.get_ticks()
    frame_rate = 100
    paused = False
    fullscreen = False
    current_filter = None

    clock = pygame.time.Clock()

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle input (key presses)
            paused, fullscreen, current_filter, current_frames, frame_count, screen, screen_width, screen_height = handle_input(
                event, paused, fullscreen, current_filter, frames_1, frames_2, current_frames, frame_count, screen, screen_width, screen_height)

        # Check if the color filter keys are being held down
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            current_filter = RED_FILTER
        elif keys[pygame.K_g]:
            current_filter = GREEN_FILTER
        elif keys[pygame.K_b]:
            current_filter = BLUE_FILTER
        else:
            current_filter = None

        current_frame, last_update_time = update_animation(current_frame, frame_count, last_update_time, frame_rate, paused)
        screen.fill(WHITE)
        frame_width, frame_height = current_frames[current_frame].get_size()
        scaled_frame = pygame.transform.scale(current_frames[current_frame], (screen_width, screen_height))

        if current_filter:
            scaled_frame = apply_color_filter(scaled_frame, current_filter)

        screen.blit(scaled_frame, (0, 0))
        pygame.display.flip()
        clock.tick(16)


if __name__ == "__main__":
    main()