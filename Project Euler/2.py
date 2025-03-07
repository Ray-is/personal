#Each new term in the Fibonacci sequence is generated by adding the previous two terms. By starting with 1 and 2, the first 10 terms will be:
#1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...
#By considering the terms in the Fibonacci sequence whose values do not exceed four million, find the sum of the even-valued terms.
#-----------------------------------------
fibSequence = [1,2]
newNum = 0


for ind, num in enumerate(fibSequence):
    if num == fibSequence[-1]:
        newNum = fibSequence[ind] + fibSequence[ind-1]
        print(newNum)
        fibSequence.append(newNum)
    if newNum > 4000000:
        break

evenSum = 0
for num in fibSequence:
    if num % 2 == 0:
        evenSum += num
print('---------\nEven Sum:', evenSum)