''' (c) 2019 Kyle Cox
This script simulates an iterated Prisoner's Dilemma Game, inspired by Axelrod's Tournament.
Expriments with different heuristics:
Coop: cooperates every time
Defect: defects every time
Rand: chooses to defect or cooperate randomly
T4T: tit for tat cooperates first round, then mimics opponent's last move every other iteration
'''
#MajorityRep
#RandomRep
from __future__ import print_function
from random import randint
from random import choice
from itertools import combinations
from random import shuffle
from random import random
import sys

def matrix(d1, d2):
        # takes 2 ints as matrix indices (p1 move, p2, move)
        # returns tup of matrix outcome
        m = [[(3,3), (0,5)],
            [(5,0), (1,1)]]
        # tup[0] = p1 payoff, tup[1] = p2 payoff
        # goal is higher point value
        # [[(C, C), (C, D)],
        # [(D, C), (D, D)]]
        return m[d1][d2]

class Coop(object):
    # Coop always cooperates (return 0)
    def __init__(self):
        self.name = 'Cooperator'
        self.plays = []
        self.opp_plays = []
        self.round = 0
        self.sum = 0

    def play(self):
        move = 0
        self.plays.append(move)
        self.round += 1
        return move

class Defect(object):
    # Defect always defects (return 1)
    def __init__(self):
        self.name = 'Defector'
        self.plays = []
        self.opp_plays = []
        self.round = 0
        self.sum = 0
        
    def play(self):
        self.round += 1
        move = 1
        self.plays.append(move)
        return move

class T4T(object):
    # T4T cooperates first move, then returns the opp's last move for the rest of the game
    def __init__(self):
        self.name = 'Tit For Tat'
        self.plays = list()
        self.opp_plays = list()
        self.round = 0
        self.sum = 0
    def play(self):
        self.round += 1
        if self.round == 1:
            move = 0
            self.plays.append(move)
            return move
        else:
            move = self.opp_plays[self.round - 2]
            self.plays.append(move)
            return move

class RandomRep(object):
    # cooperates first move, then returns a random element from opp's moves
    def __init__(self):
        self.name = 'Random Reputation'
        self.plays = []
        self.opp_plays = []
        self.round = 0
        self.sum = 0
    
    def play(self):
        self.round += 1
        if self.round == 1:
            move = 0
            self.plays.append(move)
            return move
        else:
            move = choice(self.opp_plays[:self.round - 1])
            self.plays.append(move)
            return move
        
class MajorityRep(object):
    # cooperates first move, then if opp is majority defector, defects, if opp is majority cooperator, coops
    def __init__(self):
        self.name = 'Majority Reputation'
        self.plays = []
        self.opp_plays = []
        self.round = 0
        self.sum = 0
    
    def play(self):
        self.round += 1
        if self.round == 1:
            move = 0
            self.plays.append(move)
            return move
        else:
            if float(sum(self.opp_plays))/float(len(self.opp_plays)) > 0.5:
                move = 1
            else:
                move = 0
        self.plays.append(move)
        return move
# c_strength is value from 0-100, probability of rand choosing Coop
class Rand(object):
    # decides randomly between 0 and 1
    def __init__(self, c_strength=75):
        self.name = 'Random'
        self.plays = []
        self.opp_plays = []
        self.round = 0
        self.sum = 0
        # probability of choosing Coop
        self.c_strength = c_strength

    def play(self):
        self.round += 1
        if random() > self.c_strength/float(100):
            move = 1
        else:
            move = 0
        self.plays.append(move)
        return move

    
def game(p1 = Rand(), p2 = Rand(), rounds=1):
    # takes two heuristics (p1 and p2) and the number of rounds
    # returns the result payoffs from those rounds of the game (payoff_count)
    
    payoff_count = []
    p1.sum = 0
    p2.sum = 0

    for round in range(rounds):
        d1 = p1.play()
        d2 = p2.play()

        p1.opp_plays.append(d2)
        p2.opp_plays.append(d1)

        payoff = matrix(d1, d2)
        payoff_count.append(payoff)

        p1.sum += payoff[0]
        p2.sum += payoff[1]

    # print(p1.name)
    # print(p1.sum)
    # print(p2.name)
    # print(p2.sum)
    # print('\n')

def retSum(player=Rand()):
    return player.sum

def evolution(numCoop,numDef,numT4T,randPlayers,numMajRep,numRandRep,numEvolutions, numEachRound):
    totPlayers = []
    totNumPlayers = numCoop+numDef+numT4T+len(randPlayers)+numMajRep+numRandRep

    randObj = []
    
    #Put players in list
    if(totNumPlayers%2 !=0):
        sys.exit("Total number of players must be an even number")
    for i in range(numCoop):
        totPlayers.append(Coop())
    for i in range(numDef):
        totPlayers.append(Defect())
    for i in range(numT4T):
        totPlayers.append(T4T())
    for i in range(numMajRep):
        totPlayers.append(MajorityRep())
    for i in range(numRandRep):
        totPlayers.append(RandomRep())

    for num in randPlayers:
        newRand = Rand(num)
        randObj.append(newRand)
        totPlayers.append(newRand)
    
    for i in range(numEvolutions):

        coopSum = 0
        defSum = 0
        T4TSum = 0
        majRepSum = 0
        randRepSum = 0
        randomSum = 0

        numRand = len(randObj)
        
        #Play each matchup
        shuffle(totPlayers)
        it = iter(totPlayers)
        matchups = zip(it,it)
        for matchup in matchups:
            game(matchup[0], matchup[1],numEachRound)
    #Calculate total points for each heuristic
        for player in totPlayers:
            if player.name =="Cooperator":
                coopSum+=player.sum
            elif player.name=="Defector":
                defSum+=player.sum
            elif player.name=="Tit For Tat":
                T4TSum+=player.sum
            elif player.name =="Majority Reputation":
                majRepSum+=player.sum
            elif player.name =="Random Reputation":
                randRepSum+=player.sum
            else:
                randomSum+=player.sum

        #Add players based on results of last round

        totSum = coopSum+defSum+T4TSum+randomSum+majRepSum+randRepSum
        
        numCoop = int(round(((numCoop+coopSum)/float(totSum+totNumPlayers))*60))
        numDef = int(round(((numDef+defSum)/float(totSum+totNumPlayers))*60))
        numT4T = int(round(((numT4T+T4TSum)/float(totSum+totNumPlayers))*60))
        numMajRep= int(round(((numMajRep+majRepSum)/float(totSum+totNumPlayers))*60))
        numRandRep = int(round(((numRandRep+randRepSum)/float(totSum+totNumPlayers))*60))
        numRand = int(round(((numRand+randomSum)/float(totSum+totNumPlayers))*60))

        # print(coopSum)
        # print(totSum)
        # print(totNumPlayers)
        # print(numCoop)
        # numCoop = int(round(float(coopSum)/float(totSum)*totNumPlayers*float(numCoop)/float(60)))
        # numDef = int(round(float(defSum)/float(totSum)*totNumPlayers*float(numDef)/float(60)))
        # numT4T = int(round(float(T4TSum)/float(totSum)*totNumPlayers*float(numT4T)/float(60)))
        # numMajRep = int(round(float(majRepSum)/float(totSum)*totNumPlayers*float(numMajRep)/float(60)))
        # numRandRep = int(round(float(randRepSum)/float(totSum)*totNumPlayers*float(numRandRep)/float(60)))
        # numRand = int(round(float(randomSum)/float(totSum)*totNumPlayers*float(numRand)/float(60)))

        # prevNumRand = numRand
        # numRand = int(round(((numRand+randomSum)/float(totSum+totNumPlayers))*totNumPlayers))       
    
        totNumPlayers = numCoop + numDef + numT4T+numRand+numMajRep+numRandRep
        totPlayers = []

        for i in range(numCoop):
            totPlayers.append(Coop())
        for i in range(numDef):
            totPlayers.append(Defect())
        for i in range(numT4T):
            totPlayers.append(T4T())
        for i in range(numMajRep):
            totPlayers.append(MajorityRep())
        for i in range(numRandRep):
            totPlayers.append(RandomRep())
        for i in range(numRand):
            totPlayers.append(Rand(randint(0,100)))

        # #Random:
        # randObj.sort(key=retSum,reverse=True)
        # newRandObj=[]
        # if numRand > prevNumRand:
        #         for obj in randObj:
        #                 newObj = Rand(obj.c_strength)
        #                 totPlayers.append(newObj)
        #                 newRandObj.append(newObj)
                        
        #         while prevNumRand<numRand:
        #                 newObj = Rand(randObj[0].c_strength)
        #                 totPlayers.append(newObj)
        #                 newRandObj.append(newObj)
        #                 prevNumRand+=1
        # else:
        #         count = 0
        #         for i in range(numRand):
        #                 newObj = Rand(randObj[count].c_strength)
        #                 totPlayers.append(newObj)
        #                 newRandObj.append(newObj)
        #                 count+=1
        # randObj = newRandObj

    print("Coop: ", numCoop, " Defect: ", numDef, " T4T: ", numT4T, " Rand: ", numRand, " MajRep: ", numMajRep, " RandRep: ", numRandRep, end=' ')
    # print(" Random Params: ", end = '')
    # for obj in randObj:
    #         print(obj.c_strength,end= ' ')
    print('')
for i in range(10):
    evolution(10,10,10,[25,25,25,50,50,50,50,75,75,75],10,10,20,20)

# l = [20, 40, 60, 80]
# for obj in l:
#     game(p1=RandomRep(), p2=Rand(c_strength=obj), rounds=2000)
