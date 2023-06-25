import numpy as np
import matplotlib.pyplot as plt


class agent:
    __ID = 0
    __gamma = 0
    __EA = 0
    __Ask = 0
    __Bid = 0

    def computeAsk(self):
        return self.__Ask

    def computeBid(self):
        return self.__Bid


class utility(agent):
    def __init__(self, v1):
        self.__ID = 1
        self.__EA = np.random.uniform(low=0.1, high=2.0)
        self.__Ask = 0
        self.__lambda1 = np.random.uniform(low=0.85, high=1.0)
        self.__lambda2 = np.random.uniform(low=0.75, high=1.25)
        self.__gamma = np.random.uniform(low=0.1, high=0.25)
        self.__C = v1

    def computeAsk(self, OBid, Phl):
        Pb = 0
        Pt = 0
        Step = 0

        if self.__EA < 2.0:
            self.__EA += self.__EA * (self.__EA / 10)
        else:
            self.__EA = np.random.uniform(low=0.1, high=2.0)

        if OBid == 0:
            self.__Ask = self.__C + (self.__lambda1 * (Phl - self.__C))
        else:
            Pb = self.__C * self.__lambda2
            Pt = OBid

            if Pb > Pt:
                Step = (Pt - Pb) * self.__gamma * self.__EA
            else:
                Step = max(Pt, self.__C - Pb) * (1 - self.__EA)

            self.__Ask = Pb + Step

        return self.__Ask, Pb, Pt, Step


class Building(agent):
    def __init__(self, v1):
        self.__ID = 2
        self.__EA = np.random.uniform(low=0.1, high=1.0)
        self.__Bid = 0
        self.__lambda3 = np.random.uniform(low=0.5, high=0.85)
        self.__lambda4 = np.random.uniform(low=0.5, high=1.0)
        self.__gamma = np.random.uniform(low=0.1, high=0.25)
        self.__D = v1

    def computeBid(self, OAsk, Pll):
        Pb = 0
        Pt = 0
        Step = 0

        if self.__EA < 2.0:
            self.__EA += self.__EA * (self.__EA / 10)
        else:
            self.__EA = np.random.uniform(low=0.1, high=2.0)

        if OAsk == 0:
            self.__Bid = self.__D - (self.__lambda3 * (self.__D - Pll))
        else:
            Pb = self.__D * self.__lambda4
            Pt = OAsk

            if Pt <= Pb:
                Step = ((Pt - Pb) * self.__gamma) * self.__EA
            else:
                Step = (min(Pt, self.__D) - Pb) * self.__gamma * (1 - self.__EA)

            self.__Bid = Pb + Step

        return self.__Bid, Pb, Pt, Step


Phl = 10
Pll = 1

OA = 0
OB = 0

rounds = 100000

a1 = utility(8)
a2 = Building(8)

lAB = []
log = []

for current in range(1, rounds):
    print("Round: ", current)

    OB, PbB, PtB, StepB = a2.computeBid(OA, Pll)
    OA, PbA, PtA, StepU = a1.computeAsk(OB, Phl)

    log.append([OB, PbB, PtB, StepB, OA, PbA, PtA, StepU])
    lAB.append([OB, OA])

    if OB >= OA:
        print("Matching done")
        break

arrayAB = np.asarray(lAB)
arrayLog = np.asarray(log)

plt.plot(arrayAB)
plt.title("Asks vs Bids")
plt.show()

plt.plot(arrayLog[:, 3])
plt.plot(arrayLog[:, 7])
plt.title("Steps")
plt.show()
