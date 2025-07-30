import argparse
import csv
import os
import subprocess
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

class Chromosome:
    def __init__(self, genes, sim_id):
        self.genes = genes
        self.sim_id = sim_id
        self.adapt = None

    def evaluate(self):
        gene_str = ",".join(map(str, self.genes))
        cmd = [sys.executable, "fast.py", gene_str, str(self.sim_id)]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Simulation failed: {result.stderr}")

        vehicles_file = f"vehicles{self.sim_id}.csv"
        with open(vehicles_file, newline="", encoding="UTF8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            sim_count = int(rows[4][0])

        self.adapt = sim_count
        return sim_count

    def __repr__(self):
        return f"Chromosome(genes={self.genes}, adapt={self.adapt})"


class GeneticAlgorithm:
    def __init__(
        self,
        sim_id,
        population_size=16,
        generations=10,
        mutation_rate=20,
        output_csv=None
    ):
        self.sim_id = sim_id
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.output_csv = output_csv or f"chromosomes{sim_id}.csv"

        self.population = []
        self.best = None
        self.averages = []

        with open(self.output_csv, 'w', newline="", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow(["Generation", "Index", "Genes", "Fitness"])

    def initialize(self):
        self.population = []
        for idx in range(self.population_size):
            genes = [random.randint(15, 40) for _ in range(4)]
            chrom = Chromosome(genes, self.sim_id)
            chrom.evaluate()
            self._update_best(chrom)
            self.population.append(chrom)
        self._record_generation(1)

    def run(self):
        self.initialize()
        for gen in range(2, self.generations + 1):
            self._step(gen)
        self._plot_results()
        print(f"Best solution: {self.best}")

    def _step(self, generation):
        new_pop = []
        with open(self.output_csv, 'a', newline="", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow([])
            writer.writerow([f"Generation {generation}"])

        while len(new_pop) < self.population_size:
            parent1 = self._select()
            parent2 = self._select()
            child_genes1, child_genes2 = self._crossover(parent1.genes, parent2.genes)

            child1 = Chromosome(child_genes1, self.sim_id)
            child2 = Chromosome(child_genes2, self.sim_id)

            child1.evaluate()
            child2.evaluate()
            self._update_best(child1)
            self._update_best(child2)

            new_pop.extend([child1, child2])

        self.population = new_pop[: self.population_size]
        self._record_generation(generation)

    def _select(self):
        weights = [c.adapt for c in self.population]
        index = random.choices(range(len(self.population)), weights=weights, k=1)[0]
        return self.population[index]

    def _crossover(self, genes1, genes2):
        child1, child2 = [], []
        for g1, g2 in zip(genes1, genes2):
            if random.random() < 0.5:
                child1.append(g1)
                child2.append(g2)
            else:
                child1.append(g2)
                child2.append(g1)

        for child in (child1, child2):
            if random.randint(1, 100) <= self.mutation_rate:
                idx = random.randrange(len(child))
                child[idx] = max(8, child[idx] + random.randint(-10, 10))

        return child1, child2

    def _update_best(self, chrom):
        if self.best is None or chrom.adapt > self.best.adapt:
            self.best = chrom

    def _record_generation(self, generation):
        total = 0
        rows = []
        for idx, chrom in enumerate(self.population):
            rows.append([generation, idx, chrom.genes, chrom.adapt])
            total += chrom.adapt
        average = total / len(self.population)
        self.averages.append(average)
        rows.append([generation, "Average", "", average])

        with open(self.output_csv, 'a', newline="", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def _plot_results(self):
        gens = np.arange(1, len(self.averages) + 1)
        plt.figure()
        plt.plot(gens, self.averages)
        plt.title("Evolution of Mean Traffic Flow")
        plt.xlabel("Generation")
        plt.ylabel("Average Vehicles")
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run GA to optimize traffic light timing.")
    parser.add_argument(
        "sim_id", type=int, help="Simulation identifier (used to name CSV files)"
    )
    parser.add_argument(
        "--pop-size", type=int, default=16, help="Population size (default: 16)"
    )
    parser.add_argument(
        "--generations", type=int, default=10, help="Number of generations (default: 10)"
    )
    parser.add_argument(
        "--mutation-rate", type=int, default=20, help="Mutation rate percentage (default: 20)"
    )
    args = parser.parse_args()

    ga = GeneticAlgorithm(
        sim_id=args.sim_id,
        population_size=args.pop_size,
        generations=args.generations,
        mutation_rate=args.mutation_rate
    )
    ga.run()
