# Treasure Hunt

import random 
import sys
import math

def createNewBoard():
    # Creates a new 60 x 15 board
    board = []
    # There are a total of 60 columns
    for x in range(60): 
        board.append([])
        # There are a total of 15 rows
        for y in range (15):
            board[x].append('~')
    return board

def drawBoard(board):
    # Draw the board
    rowSpace = '    '
    for i in range(1,6):
        rowSpace += (' ' * 9) + str(i)

    # Print the numbers at the top
    print(rowSpace)
    print('   ' + ('0123456789' * 6))
    print()

    # Print all 15 rows
    for row in range(15):
        # Added space for numbers
        if row < 10:
            extraSpace = ' '
        else:
            extraSpace = ''

        # Create string for row
        boardRow = ''
        for column in range(60):
            boardRow += board[column][row]

        print('%s%s %s %s' % (extraSpace, row, boardRow, row))

    # Print the numbers across bottom
    print()
    print(' ' + ('0123456789' * 6))
    print(rowSpace)

def getRandomChests(numChests):
    # Create a list of chest data structures (two-item lists put into x, y coordinates)
    chests = []
    while len(chests) < numChests:
        newChest = [random.randint(0, 59), random.randint(0,14)]
        # Make sure chest is not in same place
        if newChest not in chests:
            chests.append(newChest)
    return chests
    
def isOnBoard(x, y):
    # Find if coordinates entered are on board
    return x >= 0 and x <= 59 and y >= 0 and y <= 14

def makeMove(board, chests, x, y):
    # Change the board when placing devices. Remove chest when found
    # Return False if an invalid move occurs
    # Otherwise, return the string result of this move.
    smallestDistance = 100 # Any chest will be closer than 100
    for cx, cy in chests:
        distance = math.sqrt((cx - x) * (cx -x) + (cy - y) * (cy - y))

        if distance < smallestDistance:
            smallestDistance = distance

    smallestDistance = round(smallestDistance)

    if smallestDistance == 0:
        # xy is directly on a treasure chest
        chests.remove([x, y])
        return 'You have found a treasure chest!'
    else:
        if smallestDistance < 10:
            board[x][y] = str(smallestDistance)
            return 'Treasure detected at a distance of %s from the device.' % (smallestDistance)
        else:
            board[x][y] = 'X'
            return 'Device did not detect anything. All treasure out of range.'
        
def enterPlayerMove(previousMoves):
    # Let the player enter their move. Return a two-tem list of int xy coordinates.
    print('Where do you want to drop the next device? (0-59 0-14) (or type quit)')
    while True:
        move = input()
        if move.lower() == 'quit':
            print('Thanks for playing!')
            sys.exit()

        move = move.split()
        if len(move) == 2 and move[0].isdigit() and move[1].isdigit() and isOnBoard(int(move[0]), int(move[1])):
            if [int(move[0]), int(move[1])] in previousMoves:
                print('You already moved there.')
                continue
            return [int(move[0]), int(move[1])]
        
        print('Enter a number from 0 to 59, a space, then a number from 0 to 14.')

def showInstructions():
    print('''Instructions:
You are the cpatain of the Simon, a treasure-hunting ship. Your current mission
is to use devices to find three sunken treasure chest at the bottom of 
the ocean. But you only have cheap devices that find distance, not direction.
          
Enter the coordinates to drop a device. The ocean map will be marked with
how far away the nearest chest is, or an X if it is beyond the device's
range. For example, the C marks are where the chests are. The device shows a
3 because the closest chest is 3 spaces away.
          
                1         2         3
      012345678901234567890123456789012
          
    0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 0
    1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 1
    2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2
    3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
    4 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
          
      012345678901234567890123456789012
                1         2         3
(In the real game, the chests are not visible in the ocean.)
          
Press enter to continue...''')
    input()

    print('''When you drop a device directly on a chest, you retrieve it and the other 
devices update to show how far away the next nearest chest is. The chests
are beyond the range of the sonar device on the left, so it shows an X.
          
                1         2         3
      012345678901234567890123456789012
          
    0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 0
    1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 1
    2 ~~~X~~7~~~~~~C~~~~~~~~~~~~~~~~~~~ 2
    3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
    4 ~~~~~~~~~~~~~C~~~~~~~~~~~~~~~~~~~ 4
          
      012345678901234567890123456789012
                1         2         3
          
The treasure chest don't move around. Devices can detect treasure chests
up to a disrance of 9 spoaces. Try to collect all 3 chests before running 
out of devices. Good luck!
          
Press enter to continue...''')
    input()



print()
print('Would you like to view the instructions? (yes/no)')
if input().lower().startswith('y'):
    showInstructions()

while True:
    # Game setup
    devices = 20
    theBoard = createNewBoard()
    theChests = getRandomChests(3)
    drawBoard(theBoard)
    previousMoves = []

    while devices > 0:
        # Show device and chest statuses.
        print('You have %s device(s) left. %s treasure chest(s) remaining.' % (devices, len(theChests)))

        x, y = enterPlayerMove(previousMoves)
        previousMoves.append([x, y]) #Tracl all moves

        moveResult = makeMove(theBoard, theChests, x, y)
        if moveResult == False:
            continue
        else:
            if moveResult == 'You have found a sunken treasure chest!':
                # Update all the devices on the map
                for x, y in previousMoves:
                    makeMove(theBoard, theChests, x, y)
            drawBoard(theBoard)
            print(moveResult)

        # Game win message
        if len(theChests) == 0:
            print('You have found all the sunken treasure chests! Congratulations and good game!')
            break
        
        devices -= 1

    # Game lose message
    if devices == 0:
        print('We\'ve run out of devices! Now we have to turn the ship around and head')
        print('for home with treasure chests still out there! Gameover.')
        print('    The remaining chests were here:')
        for x, y in theChests:
            print('    %s, %s' % (x, y))

    # Ask user to play again
    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        sys.exit()

    