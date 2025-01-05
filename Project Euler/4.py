#A palindromic number reads the same both ways. 
#The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.
#Find the largest palindrome made from the product of two 3-digit numbers.
#---------------------------------------------------

def palindrome(wholeNum):
    i = 0
    palindromeNum = 0
    
    for digit in str(wholeNum):
        palindromeNum += 10 ** i * int(digit)
        i += 1
    return palindromeNum

def isPalindrome(wholeNum):
    if palindrome(wholeNum) == wholeNum:
        return True
    return False
    
start = 100
palindromeList = []
while start < 1000:
    for x in range(100,1000):
        for y in range(start, 1000):
            if isPalindrome(x*y):
                palindromeList.append(x*y)
                
        start += 1

print(max(palindromeList))
#----------------------------------------------------

def shorterIsPalindrome(num):
    return str(num) == str(num[::-1])

def recursiveIsPalindrome(string):
    if len(string) == 1:
        return True
        
    if string[0] == string[-1]:
        return recursiveIsPalindrome(string[1:-1])
    return False