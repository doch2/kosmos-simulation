from math import sqrt
import random

class People:
    def __init__(self):
        self.destination = [0, 0]
        self.route = []

        self.location = [
            random.randint(-50, 50),
            random.randint(-10, 10)
        ]

    def getDestination(self):
        return self.destination

    def setDestination(self, x, y):
        self.destination = [x , y]
    
    def getRoute(self):
        return self.route

    def setRoute(self, route):
        self.route = route

    def getLocation(self):
        return self.location
    
    def setLocation(self, x, y):
        self.location = [x, y]


def getRoute(a_pos,b_pos):
    weight = (a_pos[1]-b_pos[1])/(a_pos[0]-b_pos[0])
    
    x = sqrt(1/((weight)**2+1)) + a_pos[0]
    y = weight * sqrt(1/((weight)**2+1)) + a_pos[1]
    return [x,y]

def pos_a(a,b):
    k = [[0,0]]
    
    while  (k[-1][0]  < b[0] and k[-1][1] < b[1]):
        a = pos(a,b)
        k.append(a)
    del k[0]
    del k[-1]
    return k


peopleAmount = 100
roadDirection = [ #0은 왼쪽, 1은 오른쪽
    [1,0,1,1],
    [1,0,1,1],
    [1,0,1,1],
]
roadDirection = [
    {
        "centerPos": [0, 50],
        "location": [
            [-10, 10],
            [-10, 50],
            [10, 50],
            [10, 10]
        ],
    },
    {
        "centerPos": [50, 0],
        "location": [
            [10, 10],
            [50, 10],
            [50, -10],
            [10, -10]
        ],
    },
    {
        "centerPos": [0, -50],
        "location": [
            [10, -10],
            [10, -50],
            [-10, -50],
            [-10, -10]
        ],
    },
    {
        "centerPos": [-50, 0],
        "location": [
            [-10, -10],
            [-50, -10],
            [-50, 10],
            [-10, 10]
        ],
    },
]


peopleList = []
for people in range(0, peopleAmount):
    peopleModel = People()
    roadIndex = random.randint(0, len(roadDirection)-1)
    peopleModel.setDestination(roadDirection[roadIndex]["centerPos"][0], roadDirection[roadIndex]["centerPos"][1])
    peopleModel.setRoute(getRoute(peopleModel.getLocation(), peopleModel.getDestination()))

    peopleList.append(peopleModel)


for direction in roadDirection: #n번 횟수 시뮬레이션 반복
    for people in peopleList: #사람마다 계산
        if people.getDestination() == people.getLocation():
            newPos = roadDirection[random.randint(0, len(roadDirection)-1)]["centerPos"]
            people.setDestination(newPos[0], newPos[1])

            people.setRoute(getRoute(people.getLocation(), people.getDestination()))
        else:
            tempLoc = (people.getRoute())[0]
            people.setRoute((people.getRoute())[1:])
            people.setLocation(tempLoc[0], tempLoc[1])