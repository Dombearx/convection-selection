# RAW ALGORITHM
from copy import deepcopy
import utils
import nsga2_alg
import os
import frams_conf as fc
import random
import sys
import pickle
import numpy
import migration as mig
import time
from deap import creator, base, tools, algorithms, benchmarks
from FramsticksCLI import FramsticksCLI
from FramsticksEvolution import prepareToolbox

# Przetwarzanie parametrów
# argv[0] to nazwa programu - tak jest domyślnie
# NAZWA BENCHMARKA - argv[1]
# LICZBA WYSP - argv[2]
# MNOŻNIK MIGRACJI - argv[3]
# MAX LICZBA WYWOŁAŃ BEZ POPRAWY - argv[4]
# MODEL - argv[5]

if(len(sys.argv) != 6):
    print("Wrong number of arguments!")
    print("Usage:", sys.argv[0],
          "EXPERIMENT_NAME NUM_OF_ISLANDS MIGRATIONS_RATIO max_iterations_wo_improvement MODEL")
    sys.exit()


# nazwa benchmarka
EXPERIMENT_NAME = sys.argv[1]

# Początkowa liczba wysp
NUM_OF_ISLANDS = int(sys.argv[2])

# Mnożnik migracji
MIGRATION_RATIO = float(sys.argv[3])

# max liczba wywołań bez poprawy
max_iterations_wo_improvement = int(sys.argv[4])

# model
MODEL = sys.argv[5]


POPULATION_SIZE = 5
ISLAND_POPULATION_SIZE = int(POPULATION_SIZE / NUM_OF_ISLANDS)
FREQ = int(MIGRATION_RATIO * POPULATION_SIZE)
CXPB, MUTPB = 0.1, 1.0

path = "..\\\Framsticks50rc18"
framsCLI = FramsticksCLI(path, "frams.exe")

if(EXPERIMENT_NAME == "vh"):
    #toolbox = fc.getVelocityHeightToolBox(framsCLI)
    toolbox = prepareToolbox(framsCLI, '1')


toolbox.register("map", map)


# Migrate method
if(MODEL == "convection_const"):
    toolbox.register("migrate", mig.migSelFrontsContsInslands,
                     numOfIslands=NUM_OF_ISLANDS)

if(MODEL == "convection_front"):
    toolbox.register("migrate", mig.migSelOneFrontOneIsland)

# Statistics
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean, axis=0)
stats.register("std", numpy.std, axis=0)
stats.register("min", numpy.min, axis=0)
stats.register("max", numpy.max, axis=0)


# Zapisuje n najlepszych osobników (tutaj n = 1)
hallOfFame = nsga2_alg.myParetoFront(100)

# ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
toolbox.register("algorithm", nsga2_alg.nsga2Algorithm, toolbox=toolbox,
                 stats=stats, cxpb=CXPB, mutpb=MUTPB, ngen=FREQ, verbose=False, halloffame=hallOfFame)

logbooks = []

bestIndividuals = []
start_time = time.time()
iterations_wo_improvement = 0

# Początkowa populacja
islands = [toolbox.population(n=ISLAND_POPULATION_SIZE)
           for i in range(NUM_OF_ISLANDS)]

toolbox.migrate(islands)


first = True
previous_pareto_front = None


print("Running:", EXPERIMENT_NAME)
print("Islands number:", NUM_OF_ISLANDS)
print("Migration every", FREQ, "steps")
print("Max iterations without improvement:", max_iterations_wo_improvement)
print("Model:", MODEL)
print("----------START---------")
iters = 0
while(iterations_wo_improvement <= max_iterations_wo_improvement / FREQ):

    results = toolbox.map(toolbox.algorithm, islands)

    ziped = list(map(list, zip(*results)))
    islands = ziped[0]

    iters += 1

    print(iters)

    if iters >= 2:
        break

    # Jeżeli znajdzie lepszego osobnika niż najlepszy obecnie, to nadpisuje go
'''
    if previous_pareto_front == None:
        previous_pareto_front = deepcopy(hallOfFame)

    
    for previous, new in zip(previous_pareto_front, hallOfFame):
        if previous != new:
            print("improvement after:", (iterations_wo_improvement + 1)
                  * FREQ, "Fitness:", hallOfFame[0].fitness.values)
            iterations_wo_improvement = -1
            previous_pareto_front = deepcopy(hallOfFame)
            break

    print("w/o improvement:", iterations_wo_improvement)
    iterations_wo_improvement += 1

    if(iterations_wo_improvement * FREQ == int(max_iterations_wo_improvement / 2)):
        print(iterations_wo_improvement * FREQ,
              "iterations without improvement...")
    
    bestInMigration = []
    for ind in hallOfFame:
        bestInMigration.append(ind.fitness.values)

    bestIndividuals.append(bestInMigration)

    utils.saveParetoFront(hallOfFame)
    
    if first:
        for logbook in ziped[1]:
            logbooks.append(logbook)
        first = False
    else:
        for k, logbook in enumerate(ziped[1]):
            logbooks[k] += logbook
'''
toolbox.migrate(islands)


print("----------END---------")
print("Hall of fame[0]:", hallOfFame[0], hallOfFame[0].fitness)
print("time:", time.time() - start_time)
'''
# Save results
pickleOut = open("./out/" + EXPERIMENT_NAME + "_" + str(NUM_OF_ISLANDS) +
                 "_" + str(MIGRATION_RATIO) + "_" + MODEL + ".pickle", "wb")
pickle.dump(utils.result(
    logbooks, bestIndividuals, time.time() - start_time), pickleOut)
pickleOut.close()
'''
print("\n")
