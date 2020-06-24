import itertools
import math
from scipy.special import comb
import matplotlib.pyplot as plt
import sys
import random as rand
from argparse import ArgumentParser
import copy
import operator

def interactions_producer(t, k, v): #t will be 3, k will be 5, v will be 4
    interactions_list = []
    alpha = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    otherarray = list(itertools.combinations(range(k), t)) #use these to generate p
   # print("otherarray = " + str(otherarray))
    permpossib = list(itertools.product(range(v), repeat = t))
    #print("PermPossib = " + str(permpossib))
    for position in otherarray:
        for voption in permpossib:
            whattoadd = ""
            for i in position:
                whattoadd = whattoadd + alpha[i]
            for i in voption:
                whattoadd = whattoadd + alpha[i]
            interactions_list.append(whattoadd)
    return interactions_list

def initial_rand_can(num, k, v):
    rand_can = []
    alpha = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(num):
        toadd = ""
        for j in range(k):
            toadd = toadd + alpha[rand.randint(0, v-1)]
        rand_can.append(toadd)
    return rand_can

def remove_interactions(interactions_list, can): #can list of numbers
    return_list = []
    halfway = len(interactions_list[0])//2
    for item in interactions_list:
        willremove = True
        for i in range(halfway):
            if int(can[int(item[i])]) != int(item[halfway+i]):
                willremove = False
        if willremove == False:
            return_list.append(copy.deepcopy(item))
    return return_list
    
def mutation_candidate_producer_0(previous_candidates, v):  #This seems to work
    #Emphasis on low # of mutations - standard algorithm
    #We begin with adding the new mutations off the back of the algorithm
    alpha = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    new_candidates = copy.deepcopy(previous_candidates)
    for i in range(len(previous_candidates)): # number new needs to be the same
        num_mutation = rand.randint(0, len(previous_candidates[i])-1)
        candidate_new = copy.deepcopy(previous_candidates[i])
        test = list(candidate_new)
        for j in range(num_mutation): #This is a simple case so dont worry if something deleted twice
            test[rand.randint(0, len(candidate_new)-1)] = alpha[rand.randint(0, v-1)]
        new_candidates.append("".join(test))
    return new_candidates

def get_cand_score(can, uncovered_interactions):
    score = 0
    halfway = len(uncovered_interactions[0])//2
    for item in uncovered_interactions:
        willremove = True
        for i in range(halfway):
            if int(can[int(item[i])]) != int(item[halfway+i]):
                willremove = False
        if willremove != False:
            score += 1
    return score
        

def candidates_fitness(offspring, uncovered_interactions, offspringNum):
#best must be in index 0
    valuecan = {}
    returnlist = []
    print("Offspring len: " + str(len(offspring)))
    for child in offspring:
        childfitness = get_cand_score(child, uncovered_interactions)
        valuecan[child] = childfitness
    #now sort in order
    sortedlist = sorted(valuecan.items(), key=operator.itemgetter(1))

    for j in sortedlist:
        print("value = " + str(j[1]) + " can is : " + j[0])
        returnlist.insert(0, copy.deepcopy(j[0]))
    return returnlist[:offspringNum]

def main():
    arg_parser = ArgumentParser(description='Genetic Algorithm', add_help=False)
    arg_parser.add_argument('-t', dest='t', action='store',
            type=int, required=True, help='''The t value for the array''')
    arg_parser.add_argument('-k', dest='k', action='store',
            type=int, required=True, help='''The k value for the array''')
    arg_parser.add_argument('-v', dest ='v', action='store', type=int, required=True, help='''The v action for the array''')
    settings = arg_parser.parse_args()
    t = settings.t  # equal to 3
    k = settings.k  # equal to 5
    v = settings.v  # equal to 4
    
    offspringNum = 10

    print("Welcome to a Genetic Algorithm trial")
    #t k and v are stored as integers
    results = {}
    for i in range(1):  #change later on
        uncovered_reduction = [] # this is how it goes down for the plotting
        uncovered_interactions = interactions_producer(t, k, v)
        uncovered_reduction.append(len(uncovered_interactions))
        #print(len(uncovered_interactions))
        #We now need to generate the initial random candidates
        candidates = initial_rand_can(offspringNum, k, v) #lets start with 10 random candidates, maybe test the effectiveness of size
        covering_array = [candidates[0]]
        uncovered_interactions = remove_interactions(uncovered_interactions, candidates[0])
        uncovered_reduction.append(len(uncovered_interactions))
        
        
        while(len(uncovered_interactions) > 0):
            if i == 0:
                candidates = candidates_fitness(mutation_candidate_producer_0(candidates, v), uncovered_interactions, offspringNum)
            #have other if statements to change up the code
            covering_array.append(candidates[0])
            uncovered_interactions = remove_interactions(uncovered_interactions, candidates[0])
            uncovered_reduction.append(len(uncovered_interactions))
            print("Number Left = " + str(len(uncovered_interactions)))
            
        plt.plot(range(len(uncovered_reduction)), uncovered_reduction, 'ro')
        plt.xlabel("Row of CA Added")
        plt.ylabel("Uncovered Interactions Left")
        plt.suptitle("Single Run: t = " + str(t) + " k = " + str(k) + "v = " + str(v))
        plt.show()

        print(covering_array)

if __name__ == '__main__':
    main()
