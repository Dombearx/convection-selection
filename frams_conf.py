#  benchmarks
from deap import creator, base, tools, algorithms, benchmarks
import framsFunctions as ff
import FramsticksEvolution as fe
import time
import numpy
import pickle
import sys
import random

from itertools import repeat
try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequenc


def registerStandard(attributes, creator, evalFrams, frams_cli):

    toolbox = base.Toolbox()

    toolbox.register("attr_frams", fe.frams_getsimplest)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_frams, attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evalFrams, frams_cli)
    toolbox.register("mate", fe.frams_crossover, frams_cli)
    toolbox.register("mutate", fe.frams_mutate, frams_cli)

    toolbox.register("select", tools.selNSGA2)

    return toolbox


def getVelocityHeightToolBox(frams_cli):

    creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    attributes = 1

    def evalFrams(frams_cli, individual):
        return fe.frams_evaluate(frams_cli, individual)

    toolbox = registerStandard(attributes, creator, evalFrams, frams_cli)

    return toolbox
