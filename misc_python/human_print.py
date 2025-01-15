from time import sleep
import random

def human_print(string):
    wordLength = 0
    for ind, char in enumerate(string[0:-1]):

        print(char, end = '', flush = True)
        prev = string[ind - 1]
        Next = string[ind + 1]
        sleep(random.uniform(0.05, 0.08))

        if char.lower() or char.upper(): #If char is a letter:
            wordLength += 1

        if char == ' ': #If char is a space, check all the following:
            if prev == '.' or prev == '?' or prev == '!':    
                sleep(random.uniform(0, 0.2))
                wordLength = 0
                continue
            if prev == ',':
                sleep(random.uniform(0, 0.1))     
            if wordLength > 7:
                sleep(random.uniform(0, 0.1))
            wordLength = 0

    print(string[-1])

human_print(input())