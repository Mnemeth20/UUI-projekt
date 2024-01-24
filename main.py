import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class UrbanTrafficSimulator2D:
    def __init__(self, grid_size, car_density, max_speed, slow_prob):
        self.grid_size = grid_size
        self.car_density = car_density
        self.max_speed = max_speed
        self.slow_prob = slow_prob

        
        self.road = np.zeros((grid_size, grid_size), dtype=int)
        self.cars = np.zeros((grid_size, grid_size), dtype=int)

        self.initialize_traffic()

        self.stats = {'total_cars': [], 'average_speed': []}

    def initialize_traffic(self):
        cars = np.random.choice([0, 1], size=(self.grid_size, self.grid_size), p=[1 - self.car_density, self.car_density])
        self.cars = cars * np.random.randint(1, self.max_speed + 1, size=(self.grid_size, self.grid_size))
        self.road = np.ones((self.grid_size, self.grid_size), dtype=int)

    def update_traffic(self):
        new_cars = np.zeros_like(self.cars)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.cars[i, j] > 0:
                    speed = min(self.cars[i, j], self.max_speed)
                    next_position = [(i + speed) % self.grid_size, (j + speed) % self.grid_size]
                    new_cars[next_position[0], next_position[1]] = speed

        self.cars = new_cars

    def slow_down(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.cars[i, j] > 0 and np.random.rand() < self.slow_prob:
                    self.cars[i, j] = max(0, self.cars[i, j] - 1)

    def collect_stats(self):
        total_cars = np.sum(self.cars > 0)
        average_speed = np.mean(self.cars[self.cars > 0])
        self.stats['total_cars'].append(total_cars)
        self.stats['average_speed'].append(average_speed)

    def step(self):
        self.update_traffic()
        self.slow_down()
        self.collect_stats()

    def display(self):
        plt.imshow(self.road + self.cars, cmap='viridis', interpolation='none', vmin=0, vmax=self.max_speed + 1)
        plt.colorbar(ticks=np.arange(0, self.max_speed + 2))
        plt.title(f"Urban Traffic Simulation\nFrame: {len(self.stats['total_cars'])}")
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        plt.show()

def animate(frame, simulator):
    plt.clf()
    simulator.step()
    simulator.display()
    print(f"Total Cars: {simulator.stats['total_cars'][-1]}, Average Speed: {simulator.stats['average_speed'][-1]:.2f}")

def main():
    grid_size = 30
    car_density = 0.2
    max_speed = 5
    slow_prob = 0.2

    simulator = UrbanTrafficSimulator2D(grid_size, car_density, max_speed, slow_prob)

    fig = plt.figure()
    ani = animation.FuncAnimation(fig, animate, fargs=(simulator,), frames=100, interval=200, repeat=False)
    plt.show()

if __name__ == "__main__":
    main()
