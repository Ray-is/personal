#2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
#What is the smallest positive number that is evenly divisible by all the numbers from 1 to 20?
#--------------------------------------
N = int(input())

def isPrime(num):
    for fac in range(2,int(num ** 0.5)+1):
        if num % fac == 0:
            return False
    return True
        
def prime_factorization_dict(num):
    primeFactorsDict = {}
    if isPrime(num): #If num is already prime:
        primeFactorsDict[num] = 1 #Add it as key to dict and return dict
        return primeFactorsDict
            
    for fac in range(2,int(num ** 0.5)+10): #Else:
        if num % fac == 0 and isPrime(fac): #add prime factors as keys to dictionary
                primeFactorsDict[fac] = 1
                
    for primeFac in primeFactorsDict.keys():
        degree = 0   #Determine degrees of those prime factors
        tempNum = num  #And set those degrees to the values of the respective keys
        while tempNum % primeFac == 0:
           tempNum /= primeFac
           degree += 1
        primeFactorsDict[primeFac] = degree

    return primeFactorsDict

freqDict = {}      #freqDict has all the unique prime factors of all the numbers 0 to N as keys,
for x in range(2,N+1): #and the highest frequency of that key as its value
    D = (prime_factorization_dict(x))

    for primeFac in D.keys():
        if primeFac not in freqDict.keys():
            freqDict[primeFac] = 0
            
    for primeFac in D.keys():
        if D[primeFac] > freqDict[primeFac]: #If this is higher than what we currently have:
            freqDict[primeFac] = D[primeFac]

answer = 1 #Finally, we have the answer. 
for uniquePrimeFac, highestDegree in freqDict.items():
    answer *= uniquePrimeFac ** highestDegree
print(answer)
    
    


    