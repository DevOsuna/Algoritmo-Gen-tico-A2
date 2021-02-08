from LocationPoint import LocationPoint
from DemandPoint import DemandPoint
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from random import sample
from typing import List
import numpy as np
import random
import math
import copy

# Parametros de diseño
size_population  = 10
num_generations  = 100
size_chromosomes = None
mutation_probability = 0.3
crossover_probability = 0.6
num_selection_tournament = 2

print(f"Probabilidad de cruza {crossover_probability}")
print(f"Probabilidad de mutación {mutation_probability}")

Genome = List[DemandPoint]
Population = List[Genome]
Fitness = List[int]
Better_chrom = []
Worst_chrom  = []

DemandPoints = [] # Puntos de demanda, I.
LocationsPoint = [] # Puntos potenciales de instalación, J.
demandsCoveredForGeneration = [] # Número de demandas cubiertas por generación.


def generete_genome(length: int, locationsPoint: List):
    return sample(locationsPoint, k=length)


def generete_population(size: int, genome_length: int, locationsPoint: List):
    return [generete_genome(genome_length, locationsPoint) for _ in range(size)]


def population_fitness(population: List):
    return sum([fitness(genome) for genome in population])


def fitness(genome: Genome):
    
    global DemandPoints, LocationsPoint
 
    value = 0
    for point in DemandPoints:

        # Formula (1)
        isCover = point.isCover(genome)
        value += point.demand if isCover else 0

        # Valida restricción dada en la formula (2)
        sumxj = 0
        for j in point.possibleCoverage:
            for gen in genome:
                if j.ID == gen.ID:
                    sumxj += 1
                    break

        if not sumxj >= 1 if isCover else 0: return 0

    # Valida restrición dada en la formula (3)
    sumxj = 0
    for xj in LocationsPoint:
        for gen in genome:
            if xj.ID == gen.ID:
                sumxj += 1
                break

    if not sumxj == size_chromosomes: return 0
    return value


def best_chrom(fitness):
    return max(fitness, key = lambda i: i[1])


def worst_chrom(fitness):
    return min(fitness, key = lambda i: i[1])


def tournament_select(population, k):

    parent_best = None

    for i in range(k):
        temp = population[random.randint(0, len(population) - 1)]
        
        if(parent_best == None or fitness(temp) > fitness(parent_best)):
            parent_best = temp

    return parent_best


def mating(genomeA: List, genomeB: List):

    isPossibleToCross = random.random() <= crossover_probability

    if isPossibleToCross:

        # Generar número aleatorio para punto de cruza
        point = random.randint(0, len(genomeA) - 1)

        # Intercambiar los genes
        for i in range(point, len(genomeA)):
            genomeA[i], genomeB[i] = genomeB[i], genomeA[i]

    return genomeA, genomeB


def mutation(genome: Genome, locationsPoint: List[LocationPoint]):

    if random.random() <= mutation_probability:
        newGene = locationsPoint[random.randint(0, len(genome) - 1)]
        genome[random.randint(0, len(genome) - 1)] = newGene

    return genome


def survivors_selection(population: Population, new_population: Population):

    population.sort(key=lambda genome: fitness(genome))
    new_population.sort(reverse=True, key=lambda genome: fitness(genome))
    
    population[0] = copy.deepcopy(new_population[0])
    population[1] = copy.deepcopy(new_population[1])

    random.shuffle(population) 


def extract_data(data):
    
    global LocationsPoint, DemandPoints
   
    for latitude, longitude, ID, demand, isLocation, cover_range in data:

        lat = latitude
        lon = longitude
        dem = demand
        cov_ran = cover_range  
        
        if isLocation:
            LocationsPoint.append(LocationPoint(ID, cov_ran, dem, lat, lon))

        DemandPoints.append(DemandPoint(ID, dem, lat, lon))

    setCoverageForDemandPoints(DemandPoints[:], LocationsPoint[:])


# Establecer Ni para cada punto de demanda. 
def setCoverageForDemandPoints(demandPoints, locations):
    for demand in demandPoints:
        demand.setPossibleCoverage(locations)

    for demand in locations:
        demand.setPossibleCoverage(locations)


def getTotalNumDemands():
    global DemandPoints
    return sum([demand.demand for demand in DemandPoints])


def getDemandsCoveredForGeneration():
    global demandsCoveredForGeneration
    return demandsCoveredForGeneration[:]


def genetic_algorithm(data, num_brigades):
    
    global DemandPoints, LocationsPoint, Population, size_chromosomes
    global Better_chrom, Worst_chrom, demandsCoveredForGeneration, Fitness
    size_chromosomes = num_brigades
    extract_data(data)

    if num_brigades > len(LocationsPoint):
        return None, None, None

    # 1 Generar población
    Population = generete_population(size_population, size_chromosomes, LocationsPoint)

    # 2 Calcular Fitness
    Fitness = [(genome, fitness(genome)) for genome in Population]

    decendents = []
    for num_generation in range(num_generations):

        decendents.clear()
        for _ in range(size_population // 2):

            # 3 Selección
            parent1 = tournament_select(Population, num_selection_tournament)
            parent2 = tournament_select(Population, num_selection_tournament)
            
            # 4 Cruza de individuos
            ch1, ch2 = mating(parent1[:], parent2[:])

            # 5 Mutación
            ch1 = mutation(ch1, LocationsPoint)
            ch2 = mutation(ch2, LocationsPoint)

            decendents.append(ch1[:])
            decendents.append(ch2[:])

        # 6 Selección de supervivientes (Poda)
        survivors_selection(Population, decendents)

        # 7 Calcular Fitness
        Fitness = [(genome, fitness(genome)) for genome in Population]

        # 8 Guardar el mejor cromosoma
        Better_chrom.append(best_chrom(Fitness))

        # print('El mejor cromosoma: ', best_chrom(Fitness))

        # 9 Guardar el peor cromosoma
        Worst_chrom.append(worst_chrom(Fitness))

        numDemandsCovered = best_chrom(Fitness)[1] # (genome, fitness)
        demandsCoveredForGeneration.append(numDemandsCovered)
   
    # Mostrar mejores individuos por generación
    for i in range(num_generations):
        print(f"Mejor fitness de generación {i+1} = {Better_chrom[i][1]}")
        print(f"Peor fitness de generación  {i+1} = {Worst_chrom[i][1]}")

    return Better_chrom, Worst_chrom, num_generations