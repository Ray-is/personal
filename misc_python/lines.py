def lines(numsString, Reverse=''):
    nums = [int(num) for num in numsString.split()] #List of integers
    Reverse = Reverse.lower() #Bool
    if Reverse == 't' or Reverse == 'y' or Reverse == 'true' or Reverse == 'yes' or Reverse == '1':
        Reverse = True
    else:
        Reverse = False

    pos = 0
    lowest = 0
    highest = 0
    for ind, v in enumerate(nums): #Get length of grid (width is just sum(nums))
        if ind % 2 == int(Reverse): #If Reverse is False, upward lines have even indices
            pos += v                #If Reverse is True, upward lines have odd indices
        else:
            pos -= v
        if pos < lowest:
            lowest = pos
        if pos > highest:
            highest = pos
    length = abs(lowest) + abs(highest)

    grid = [[' ' for w in range(sum(nums))] for l in range(length+1)] #Create a grid (2D list) with correct dimensions

    xPos = -1 #Set starting x and y positions on the grid
    yPos = length - abs(lowest)

    for ind, line in enumerate(nums): #For each line:
        xPos += 1 #Set its first character without changing y position
        if ind % 2 == int(Reverse):
            grid[yPos][xPos] = '/'
        else: #Ensure it is going in the right direction
            grid[yPos][xPos] = '\\'
        for _ in range(line-1): #Build the rest of the line, changing y position accordingly
            xPos += 1
            if ind % 2 == int(Reverse):
                yPos -= 1
                grid[yPos][xPos] = '/'
            else: #Ensure it is going in the right direction
                yPos += 1
                grid[yPos][xPos] = '\\'

    for row in grid: #Print the final grid
        for char in row:
            print(char, end='')
        print()

if __name__ == '__main__':
    lines(input('Enter some numbers, separated by spaces: '), input('Reverse? '))

    #Continuously generate random lines
    from random import randint as r
    lineCount = int(input('Enter line count: '))
    maxLineLength = int(input('Enter maximum line length: '))
    while True:
        randomString = str(r(1,maxLineLength))
        for _ in range(r(1,lineCount-1)):
            randomString += ' ' + str((r(1,maxLineLength)))
        lines(randomString,str(r(0,1)))