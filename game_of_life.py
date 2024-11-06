import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GameOfLife:
    def __init__(self, size=(50, 50), random_seed=None):
        """
        Initialize the Game of Life grid
        
        Parameters:
        - size: Tuple of grid dimensions (rows, columns)
        - random_seed: Optional seed for reproducible random initial state
        """
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # Create a random initial grid with 20% chance of cell being alive
        self.grid = np.random.choice([0, 1], size=size, p=[0.8, 0.2])
        self.size = size

    def count_neighbors(self, x, y):
        """
        Count live neighbors for a given cell
        
        Parameters:
        - x, y: Cell coordinates
        
        Returns:
        - Number of live neighbors
        """
        # Create a slice of 3x3 grid around the cell, handling edge cases
        neighbors = self.grid[
            max(0, x-1):min(self.size[0], x+2), 
            max(0, y-1):min(self.size[1], y+2)
        ]
        
        # Subtract the cell itself from the total
        return np.sum(neighbors) - self.grid[x, y]

    def update(self):
        """
        Apply Game of Life rules to update the grid
        
        Returns:
        - Updated grid
        """
        # Create a copy of the grid to store next generation
        next_grid = self.grid.copy()
        
        # Iterate through each cell
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                # Count live neighbors
                live_neighbors = self.count_neighbors(x, y)
                
                # Apply Game of Life rules
                if self.grid[x, y] == 1:
                    # Cell is alive
                    if live_neighbors < 2 or live_neighbors > 3:
                        next_grid[x, y] = 0  # Cell dies
                else:
                    # Cell is dead
                    if live_neighbors == 3:
                        next_grid[x, y] = 1  # Cell becomes alive
        
        self.grid = next_grid
        return self.grid

    def simulate(self, generations=100, interval=200):
        """
        Simulate and visualize Game of Life
        
        Parameters:
        - generations: Number of generations to simulate
        - interval: Milliseconds between frames
        """
        # Set up the plot
        fig, ax = plt.subplots()
        img = ax.imshow(self.grid, interpolation='nearest', cmap='binary')
        plt.title('Conway\'s Game of Life')
        
        # Animation update function
        def update_plot(frame):
            self.update()
            img.set_data(self.grid)
            return [img]
        
        # Create animation
        anim = animation.FuncAnimation(
            fig, 
            update_plot, 
            frames=generations, 
            interval=interval, 
            blit=True
        )
        
        plt.show()

    @classmethod
    def predefined_patterns(cls):
        """
        Create some interesting predefined patterns
        """
        patterns = {
            'glider': np.array([
                [0, 1, 1],
                [0, 0, 1],
                [1, 1, 1]
            ]),
            'blinker': np.array([
                [0, 1, 0],
                [0, 1, 1],
                [0, 1, 0]
            ]),
            'beacon': np.array([
                [1, 1, 0, 0],
                [1, 1, 1, 0],
                [0, 1, 1, 1],
                [0, 0, 1, 1]
            ])
        }
        return patterns

def main():
    # Create Game of Life instance
    game = GameOfLife(size=(100, 100), random_seed=42)
    
    # Simulate for 200 generations
    game.simulate(generations=200, interval=100)

if __name__ == "__main__":
    main()
