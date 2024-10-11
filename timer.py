import pygame

class Timer:
    def __init__(self, images, start_index=0, loop_continuously=True, delta=1000):
        if not images:
            raise ValueError("The timer's list of images is empty")
        if start_index >= len(images):
            raise ValueError("start_index out of bounds")

        self.images = images  # List of images (frames)
        self.delta = delta  # Time between frames in milliseconds
        self.loop_continuously = loop_continuously  # Loop the animation continuously or stop after last frame
        self.index = start_index  # Current frame index
        self.latest = pygame.time.get_ticks()  # Time when the last frame was updated

        # Flags to control the timer
        self._animation_finished = False  # Track if the non-looping animation is finished
        self.active = True  # Timer starts as active by default

    def reset(self):
        """Reset the timer to the first frame and mark the animation as active."""
        self.index = 0
        self.latest = pygame.time.get_ticks()
        self._animation_finished = False
        self.active = True

    def stop(self):
        """Stop the timer from updating frames."""
        self.active = False

    def start(self):
        """Start the timer to resume updating frames."""
        self.active = True

    def finished(self):
        """Return True if the animation is finished (non-looping animations)."""
        return not self.loop_continuously and self._animation_finished

    def current_image(self):
        """Return the current image in the animation, handling frame switching."""
        if not self.active:
            return self.images[self.index]  # Keep showing the current image if the timer is inactive

        now = pygame.time.get_ticks()

        # Check if it's time to update the frame
        if now - self.latest >= self.delta:
            if not self.finished():  # Only update frame if animation isn't finished
                self.index += 1
                self.latest = now

                # If we've reached the end of the frames:
                if self.index >= len(self.images):
                    if self.loop_continuously:
                        self.index = 0  # Loop back to the first frame
                    else:
                        self.index = len(self.images) - 1  # Stop at the last frame
                        self._animation_finished = True

        return self.images[self.index]
