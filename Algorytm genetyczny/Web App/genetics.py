import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import random
import time

def generate_cities(n=10, radius=250, center=(0, 0)):

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    cities = [(center[0] + radius * np.cos(a), center[1] + radius * np.sin(a)) for a in angles]
    return cities

def initialize_population(n_cities, population_size=10):

    population = []
    for _ in range(population_size):
        individual = list(np.random.permutation(n_cities))
        population.append(individual)
    return population

def calculate_distance(path, cities):

    distance = 0.0
    for i in range(len(path)):
        city_a = cities[path[i]]
        city_b = cities[path[(i + 1) % len(path)]]  # wracamy do punktu startowego
        distance += np.linalg.norm(np.array(city_a) - np.array(city_b))
    return distance

def optimal_path_distance(cities):

    n = len(cities)
    path = list(range(n))  # odwiedzamy w kolejności
    return calculate_distance(path, cities)


def roulette_selection(population, fitnesses):

    inverted_fitnesses = [1 / f for f in fitnesses]
    total_fitness = sum(inverted_fitnesses)
    probabilities = [f / total_fitness for f in inverted_fitnesses]

    selected_index = np.random.choice(len(population), p=probabilities)
    return population[selected_index]


def crossover(parent1, parent2):

    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size
    child[start:end + 1] = parent1[start:end + 1]

    pointer = 0
    for city in parent2:
        if city not in child:
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = city

    return child

def mutate(path, mutation_rate=0.05):

    path = path.copy()
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(path)), 2)
        path[i], path[j] = path[j], path[i]
    return path


def genetic_algorithm(
        cities,
        population_size=100,
        generations=500,
        crossover_rate=0.9,
        mutation_rate=0.05,
        elite_size=0.05,
        update=None
):
    start = time.time()
    population = initialize_population(len(cities), population_size)
    best_distances = []
    best_paths = []
    initial_mutation_rate = mutation_rate
    stagnation_count = 0
    previous_best = 0

    for gen in range(generations):

        routes = [calculate_distance(individual, cities) for individual in population]
        sorted_population = [x for _, x in sorted(zip(routes, population))]
        best_individual = sorted_population[0]

        best_distance = calculate_distance(best_individual, cities)
        best_distances.append(best_distance)
        best_paths.append(best_individual)

        if previous_best == best_distance:
            stagnation_count += 1
            if stagnation_count >= 5:
              mutation_rate += 0.1
              stagnation_count = 0
        else:
            stagnation_count = 0
            mutation_rate=initial_mutation_rate

            # Callback do aktualizacji wykresu
        if update is not None:
               update(gen, best_distances, best_paths)

        previous_best = best_distance

        elite_individuals = int(elite_size*len(sorted_population))
        if elite_individuals == 0: elite_individuals = 1
        new_population = sorted_population[:elite_individuals]

        while len(new_population) < population_size:
            parent1 = roulette_selection(population, routes)
            parent2 = roulette_selection(population, routes)

            if random.random() < crossover_rate:
                child = crossover(parent1, parent2)
            else:
                child = parent1[:]

            if random.random() < mutation_rate:
                child = mutate(child)

            new_population.append(child)

        population = new_population

    end = time.time()
    seconds = end - start

    return best_paths, best_distances, seconds

def create_route_animation(cities, paths, center, radius, filename="evolution.gif"):
    fig, ax = plt.subplots(figsize=(5, 5))

    selected_frames = list(range(0, len(paths), 5))
    if len(paths) - 1 not in selected_frames:
        selected_frames.append(len(paths) - 1)  # dodaj ostatnią ramkę jeśli nie została ujęta

    def update(frame_idx):
        frame = selected_frames[frame_idx]
        ax.clear()
        ax.axis('off')
        path = paths[frame] + [paths[frame][0]]  # zamykamy trasę
        x = [cities[i][0] for i in path]
        y = [cities[i][1] for i in path]
        ax.plot(x, y, 'o-', color='blue')
        ax.set_title(f'Pokolenie {frame}')
        ax.grid(False)

    anim = FuncAnimation(fig, update, frames=len(selected_frames), interval=50)
    anim.save(filename, writer=PillowWriter(fps=5))
    plt.close()