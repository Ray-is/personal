#The prime factors of 13195 are 5, 7, 13 and 29.
#What is the largest prime factor of the number 600851475143?
#sqrt(600851475143)+1 = 775147
#------------------------------------

facs = []
for x in range(2, 775147): #Determine all unique factors of the number
    if 600851475143 % x == 0:
        facs.append(x)
print(facs, '\n')

for i in facs[:]: #Discard the ones that aren't prime
    for j in range(2, int(i ** 0.5 + 1)):
        if i % j == 0:
            facs.remove(i)
            
print(max(facs))

ZeroDivisionError