import random


class Snake:
    """Encapsulates snake state and game rules."""

    def __init__(self, grid_w: int, grid_h: int):
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.reset()

    def reset(self) -> None:
        self.segments = [(self.grid_w // 2, self.grid_h // 2)]
        self.direction = (1, 0)
        self.apple = self._spawn_apple()

    def _spawn_apple(self):
        while True:
            p = (random.randrange(self.grid_w), random.randrange(self.grid_h))
            if p not in self.segments:
                return p

    def change_dir(self, new_dir: tuple) -> None:
        # Prevent reversing direction
        if new_dir[0] == -self.direction[0] and new_dir[1] == -self.direction[1]:
            return
        self.direction = new_dir

    def step(self) -> tuple[bool, bool, bool]:
        """Advance the snake by one cell.

        Returns a tuple (ate_apple, died, won).
        """
        head = self.segments[-1]
        new_head = (
            (head[0] + self.direction[0]) % self.grid_w,
            (head[1] + self.direction[1]) % self.grid_h,
        )

        # Initialize the flag to avoid NameError later
        ate = False

        if new_head in self.segments:
            #self.reset()
            return (False, True, False)  # Died

        self.segments.append(new_head)

        # Check if apple was eaten
        if new_head == self.apple:
            ate = True

            if len(self.segments) == self.grid_w * self.grid_h:
                # Board is full, the player wins!
                return (True, False, True)  # Won

            # If not won, spawn the next apple
            self.apple = self._spawn_apple()

        # move forward (drop tail)
        # Only drop the tail if an apple was NOT eaten.
        if not ate:
            self.segments.pop(0)

        # If reached this point, the game is still running (not died, not won)
        return (ate, False, False)

    def positions(self):
        return list(self.segments)
