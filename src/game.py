import random


class Snake:
    """Encapsulates snake state and game rules."""

    def __init__(self, grid_w: int, grid_h: int, mode: str = "Classic"):
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.mode = mode
        self.obstacles = set()
        self.reset()

    def reset(self) -> None:
        self.segments = [(self.grid_w // 2, self.grid_h // 2)]
        self.direction = (1, 0)
        self.obstacles.clear()
        self.apple = self._spawn_apple()

    def _spawn_apple(self):
        while True:
            p = (random.randrange(self.grid_w), random.randrange(self.grid_h))
            p = (random.randrange(self.grid_w), random.randrange(self.grid_h))
            if p not in self.segments and p not in self.obstacles:
                return p

    def _spawn_obstacle(self):
        for _ in range(50): # Try 50 times to find a spot
            p = (random.randrange(self.grid_w), random.randrange(self.grid_h))
            # Don't spawn on snake, apple, or existing obstacles
            # Also avoid spawning too close to the head to prevent cheap deaths
            # And avoid spawning too close to the apple to prevent blocking it
            head = self.segments[-1]
            dist_head = abs(p[0] - head[0]) + abs(p[1] - head[1])
            dist_apple = abs(p[0] - self.apple[0]) + abs(p[1] - self.apple[1])
            
            if (p not in self.segments and 
                p != self.apple and 
                p not in self.obstacles and 
                dist_head > 3 and 
                dist_apple > 3):
                self.obstacles.add(p)
                return

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

        if new_head in self.segments or new_head in self.obstacles:
            #self.reset()
            return (False, True, False)  # Died

        self.segments.append(new_head)

        # Check if apple was eaten
        if new_head == self.apple:
            ate = True
            
            if len(self.segments) + len(self.obstacles) == self.grid_w * self.grid_h:
                # Board is full, the player wins!
                return (True, False, True)  # Won

            # If not won, spawn the next apple
            self.apple = self._spawn_apple()

            # Spawn obstacle every 3 apples in Arcade mode
            # Score is len(segments) - 1 (since we just grew)
            score = len(self.segments) - 1
            if self.mode == "Arcade" and score % 3 == 0:
                self._spawn_obstacle()

        # move forward (drop tail)
        # Only drop the tail if an apple was NOT eaten.
        if not ate:
            self.segments.pop(0)

        # If reached this point, the game is still running (not died, not won)
        return (ate, False, False)

    def positions(self):
        return list(self.segments)

    def to_dict(self):
        return {
            "segments": self.segments,
            "direction": self.direction,
            "apple": self.apple,
            "mode": self.mode,
            "obstacles": list(self.obstacles),
        }

    def from_dict(self, data):
        self.segments = [tuple(p) for p in data["segments"]]
        self.direction = tuple(data["direction"])
        self.apple = tuple(data["apple"])
        self.mode = data.get("mode", "Classic")
        self.obstacles = set(tuple(p) for p in data.get("obstacles", []))
