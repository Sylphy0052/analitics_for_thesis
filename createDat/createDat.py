import math
import os
import sys

ALPHA = 2.8
BETA = 0.6
GAMMA = 0.34
L_M = 10.2
L_H = 0.0204

MEDIAN = {"30": 5322.5, "50": 33906.5, "70": 132015.5, "90": 263186.0}
STD = {"30": 9248.0, "50": 47013.5, "70": 151205.9, "90": 280603.0}

class Recursive:
    def __init__(self):
        # self.dats = []
        self.dataValues = []
        self.dataKeys = []
        self.dataNum = 1
        self.num = 0

    def addDat(self, key, dat):
        self.dataKeys.append(key)
        self.dataValues.append(dat)
        self.num += 1
        self.dataNum *= len(dat)

    def setDats(self, dats):
        self.dats = dats
        dataNum = len(self.dats)
        if self.dataNum != dataNum:
            print("Error")
            sys.exit(1)

    def setFirst(self):
        self.index = 0
        self.currentLength = self.dataNum
        # for i in range(self.dataNum):
        #     self.dats.append(Dat())

    def setParam(self):
        val = self.dataValues[self.index]
        length = int(self.currentLength / len(val))
        self.currentLength = length
        for i in range(self.dataNum):
            for j in range(len(val)):
                for k in range(length):
                    index = i * len(val) * length + j * length + k
                    self.dats[index].setParam(self.dataKeys[self.index], val[j])
                    # print("{} - {}: {}".format(self.index, index, val[j]))
                    # self.dats[index].add(val[j])
            if index + 1 == self.dataNum:
                # print("fin")
                break
        self.index += 1
        if self.index == self.num:
            return
        else:
            self.setParam()

    def execute(self):
        self.setFirst()
        self.setParam()
        # for i in range(self.dataNum):
        #     self.dats[i].printValues()

class FECPacket:
    def __init__(self, dc, n, rate):
        # packet length
        self.l_p = dc.getLength() / int(n) + L_H
        self.dc = DC(ALPHA * pow(self.l_p, -1 * BETA))

        self.d_p = self.dc.getDiameter()
        self.stepLength_p = self.dc.getStepLength()

        # self.testPrint()

    def getDC(self):
        return self.dc

    def getDiameter(self):
        return self.d_p

    def getStepLength(self):
        return self.stepLength_p

    def testPrint(self):
        payloadSize = self.l_p / 4 / 0.00034
        print(payloadSize)
        print(self.dc.getDC())
        print(self.d_p)
        print(self.stepLength_p)

class Dat:
    def __init__(self):
        self.params = {}

    def setParam(self, name, params):
        self.params[name] = params

    def getParam(self, name):
        return self.params[name]

    def printParams(self):
        for k, v in self.params.items():
            print(k, v)

class DC:
    def __init__(self, dc):
        self.dc = float(dc)
        self.calcParams()

        # self.testPrint()

    def calcParams(self):
        self.diameter = 2 * GAMMA / self.dc
        self.stepLength = pow(2 * self.dc, 0.5)
        self.length = pow(self.dc / ALPHA, -1 / BETA)

    def getDC(self):
        return self.dc

    def getDiameter(self):
        return self.diameter

    def getStepLength(self):
        return self.stepLength

    def getLength(self):
        return self.length

    def testPrint(self):
        payloadSize = self.length / 4 / 0.00034
        print(payloadSize)
        print(self.dc)
        print(self.diameter)
        print(self.stepLength)

def calcRWT(type, d):
    median = MEDIAN[d]
    std = STD[d]
    if type == "0":
        return 25000000
    elif type == "1":
        return (int)(2 * median)
    elif type == "2":
        return (int)(median + std / 3)
    elif type == "3":
        return (int)(median + std / 2)
    elif type == "4":
        return (int)(median + std)

def writeDatFile(dats):
    # print(len(dats))
    for dat in dats:
        distance = dat.getParam("distance")
        duplication = dat.getParam("duplication")
        noiseNum = dat.getParam("noise")
        moleculeType = dat.getParam("moleculeType")
        rtoType = dat.getParam("rtoType")
        dc = DC(dat.getParam("dc"))
        if dat.getParam("decomposingType") != "0":
            decomposing = "_decomposing{}".format(dat.getParam("decomposingType"))
        else:
            decomposing = ""
        if dat.getParam("FEC") == "1":
            fec = "_FEC{}-{}".format(dat.getParam("numPacket"), dat.getParam("rateFEC").replace('.', ''))
        else:
            fec = ""

        if dat.getParam("adaptive") != "0":
            adaptive = "_adaptive{}".format(dat.getParam("adaptive"))
        else:
            adaptive = ""

        messages = "_{}messages".format(dat.getParam("numMessages"))

        fileName = "dat/TxRx{}_ARQ{}-{}_{}-{}{}_RTO{}_DC{}{}{}{}".format(distance, duplication, duplication, moleculeType, moleculeType, adaptive, rtoType, str(dc.getDC()).replace('.', ''), messages, decomposing, fec)
        print(fileName)
        rwt = calcRWT(rtoType, distance)

        with open(fileName + ".dat", 'w') as f:
            f.write("***From Distance\n")
            f.write("mediumDimensionX {}\n".format((int)(distance) * 4))
            f.write("mediumDimensionY {}\n".format((int)(distance) * 4))
            f.write("mediumDimensionZ {}\n".format((int)(distance) * 4))
            f.write("transmitter (-{}, 0, 0) 3 (-{}, 0, 0)\n".format((int)((int)(distance) / 2), (int)((int)(distance) / 2)))
            f.write("receiver ({}, 0, 0) 3 ({}, 0, 0)\n".format((int)((int)(distance) / 2), (int)((int)(distance) / 2)))

            f.write("\n***Constant Value\n")
            f.write("maxSimulationStep 25000000\n")
            f.write("velRail 1\n")
            f.write("probDRail 0.5\n")

            f.write("\n***From numMessages\n")
            f.write("numMessages {}\n".format(dat.getParam("numMessages")))

            f.write("\n***From numRetransmissions\n")
            f.write("numRetransmissions {}\n".format(dat.getParam("numRetransmissions")))

            f.write("\n***From rtoType\n")
            f.write("retransmitWaitTime {}\n".format(rwt))

            f.write("\n***From DC\n")
            f.write("stepLengthX {}\n".format(dc.getStepLength()))
            f.write("stepLengthY {}\n".format(dc.getStepLength()))
            f.write("stepLengthZ {}\n".format(dc.getStepLength()))

            f.write("\n***Molecule Params\n")
            f.write("moleculeParams {} INFO {} {} {}\n".format(duplication, moleculeType, dat.getParam("adaptive"), dc.getDiameter()))
            f.write("moleculeParams {} ACK {} {} {}\n".format(duplication, moleculeType, dat.getParam("adaptive"), dc.getDiameter()))
            f.write("moleculeParams {} NOISE 0\n".format(noiseNum))

            f.write("\n***Decomposing Type\n")
            f.write("decomposing {}\n".format(dat.getParam("decomposingType")))

            f.write("\n***useCollisions\n")
            f.write("useCollisions {}\n".format(dat.getParam("useCollisions")))

            f.write("\n***useAcknowledgements\n")
            f.write("useAcknowledgements {}\n".format(dat.getParam("ack")))

            f.write("\n***From FEC or not\n")
            f.write("assembling {}\n".format(dat.getParam("FEC")))
            if dat.getParam("FEC") == "1":
                f.write("FEC PARITYCHECK {} {}\n".format(dat.getParam("numPacket"), dat.getParam("rateFEC")))
                f.write("\n***FEC Setting\n")
                p = FECPacket(dc, dat.getParam("numPacket"), dat.getParam("rateFEC"))
                f.write("packetStepLengthX {}\n".format(p.getStepLength()))
                f.write("packetStepLengthY {}\n".format(p.getStepLength()))
                f.write("packetStepLengthZ {}\n".format(p.getStepLength()))
                f.write("packetDiameter {}\n".format(p.getDiameter()))

            f.write("\n***Output File Name\n")
            f.write("outputFile {}\n".format(fileName.split("/")[1] + ".txt"))

# def makeMultipleDat(dats, datNum, multipleValues, index, startPoint):
#     if index >= 0:
#         count = 0
#         for k, v in multipleValues.items():
#             if count != index:
#                 count += 1
#             else:
#                 v_len = (int)(datNum / len(v))
#                 for i in range(len(v)):
#                     for j in range(v_len):
#                         buf = startPoint + i * v_len + j
#                         try:
#                             dats[buf].setParam(k, v[i])
#                         except IndexError:
#                             return
#                 count += 1
#         if index == 0:
#             return
#         for a in range(len(v)):
#             makeMultipleDat(dats, v_len, multipleValues, index - 1, startPoint + a * v_len)
#
#     else:
#         return

def createDats(params):
    datNum = 1
    for v in params.values():
        datNum *= len(v)
    dats = []
    for i in range(datNum):
        dats.append(Dat())

    multipleValues = {}
    r = Recursive()

    for k, v in params.items():
        if len(v) == 1:
            for i in range(datNum):
                dats[i].setParam(k, v[0])

        else:
            # multipleValues[k] = v
            r.addDat(k, v)

    r.setDats(dats)
    r.execute()
    # makeMultipleDat(dats, datNum, multipleValues, len(multipleValues) - 1, 0)
    return dats

def readParam(line):
    name, param = line.split(" ")
    param = param.rstrip()
    params = []
    if ',' in param:
        params = param.split(",")
    else:
        params.append(param)

    return [name, params]

def main():
    file_name = "dat.txt"
    if not os.path.exists("dat"):
        os.mkdir("dat")
    params = {}
    with open(file_name, 'r') as f:
        for line in f:
            name, param = readParam(line)
            params[name] = param

    dats = createDats(params)
    writeDatFile(dats)

if __name__ == '__main__':
    main()
