def makelogFile(lines, outputName):
    file = open(outputName, "w")
    for line in lines:
        for value in line:
            file.write(str(value) + "\t")
        file.write("\n")
    file.close()


def saveParetoFront(front):
    outputName = "newFront.gen"
    file = open(outputName, "w")
    for individual in front:
        file.write(individual[0] + "\t" + str(individual[1]))
        file.write("\n")

    file.close()


def readParetoFront(filename):
    file = open(filename, "r")
    lines = file.readlines()
    fitnessess = []
    for line in lines:
        fitnessess.append(line[line.index("\t"): len(line)])

    file.close()

    return fitnessess


class result:

    def __init__(self, logbooks, hallOfFamers, time):
        self.logbooks = logbooks
        self.hallOfFamers = hallOfFamers
        self.time = time

    def getLogbooks(self):
        return self.logbooks

    def getHallOfFamers(self):
        return self.hallOfFamers

    def getTime(self):
        return self.time
