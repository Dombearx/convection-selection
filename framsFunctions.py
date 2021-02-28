from subprocess import Popen, PIPE
import json
import utils

frams = "..\\Framsticks50rc18\\frams.exe"


def parseIndividual(text):
    text = text.decode("utf-8")
    lines = text.split("\n")
    genotype = lines[2:]
    return genotype[0].strip()


def getSimpleGenotype():
    args = frams + " -Q -s -icliutils.ini \"getsimplest 1\" -q"
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return parseIndividual(stdout)


def framsMutate(individual):
    genotype = individual[0]
    args = frams + " -Q -s -icliutils.ini rnd mut -q"
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate(bytes(genotype, encoding="utf-8"))
    individual[0] = parseIndividual(stdout)


def framsEvaluate(individual):
    genotype = individual
    fileName = saveIndividualToFile(genotype)

    path_to_file = "..\\\\..\\\\framsy2\\\\"
    path = path_to_file + fileName
    args = frams + " -Q -s -icliutils.ini \"expdef standard-eval\" \"eval eval-allcriteria.sim " + path + "\" -q"

    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    with open("..\\Framsticks50rc14\\data\\scripts_output\\genos_eval.json") as f:
        data = json.load(f)
    dictionary = data[0]
    results_temp = dictionary["evaluations"]
    results = results_temp[""]
    return(results["velocity"], results["vertpos"])


def framsCrossover(individual1, individual2):
    genotype1 = individual1[0]
    genotype2 = individual2[0]

    fileName1, fileName2 = saveParentsToFiles(genotype1, genotype2)

    path_to_file = "..\\\\..\\\\framsy2\\\\"
    path1 = path_to_file + fileName1
    path2 = path_to_file + fileName2

    args = frams + " -Q -s -icliutils.ini rnd \"crossover " + \
        path1 + " " + path2 + "\" -q"
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    individual1[0] = parseIndividual(stdout)

    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    individual2[0] = parseIndividual(stdout)

    return individual1, individual2


def saveIndividualToFile(genotype):
    outputName = "toEvaluate.gen"
    file = open(outputName, "w")
    file.write("org:")
    file.write("\n")
    file.write("genotype:~")
    file.write("\n")
    file.write("".join(genotype) + "~")
    file.close()
    return outputName


def saveParentsToFiles(genotype1, genotype2):
    outputName1 = "parent1.gen"
    outputName2 = "parent2.gen"
    file = open(outputName1, "w")
    file.write(genotype1)
    file.close()

    file = open(outputName2, "w")
    file.write(genotype2)
    file.close()
    return outputName1, outputName2


if __name__ == "__main__":

    oldFrams = []
    newFrams = []
    with open("front.gen") as fg:
        for line in fg.readlines():
            oldFrams.append(line[:-1])
        for i, fram in enumerate(oldFrams):
            print(i)
            newFrams.append((fram, framsEvaluate(fram)))

    utils.saveParetoFront(newFrams)


if __name__ == "__main__":

    toolbox = prepareToolbox(
        framsCLI, '1' if parsed_args.genformat is None else parsed_args.genformat)

    POPSIZE = 10
    GENERATIONS = 100

    pop = toolbox.population(n=POPSIZE)
    hof = tools.HallOfFame(5)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("stddev", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    print('Evolution with population size %d for %d generations, optimization criteria: %s' % (
        POPSIZE, GENERATIONS, OPTIMIZATION_CRITERIA))
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.2, mutpb=0.9,
                                   ngen=GENERATIONS, stats=stats, halloffame=hof, verbose=True)
    print('Best individuals:')
    for best in hof:
        print(best.fitness, '\t-->\t', best[0])
