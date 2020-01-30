# This is a stupidly inefficient but nevertheless funtional attempt at Battleship with fully functioning AI, no special libraries.
from random import randint
import copy
import enum
# List declarations
boardP = [["   ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
          ["A: ", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["B: ", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["C: ", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["D: ", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["E: ", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["F: ", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["G: ", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["H: ", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["I: ", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["J: ", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
          ["K: ", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]]


boardBot = [[" ", " ", " ", " ", " ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " "],
            ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#", "#", "#"],
            [" ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " "]]


# Create and set the bot display board to have '?' spots

boardBotDisplay = copy.deepcopy(boardP)
for i in range(1, 12):
    for j in range(1, 12):
        boardBotDisplay[i][j] = "?"


# Prints Player board

def printPBoard():
    for x in range(0, 12):
        for y in range(0, 12):
            if y == 0:
                print("\n")
            if x == 0 and y == 10:
                print(boardP[x][y], end="   ")
            else:
                print(boardP[x][y], end="    ")


# Prints Bot board

def printBotBoard():
    for i in range(0, 12):
        for j in range(0, 12):
            if j == 0:
                print("\n")
            if i == 0 and j == 10:
                print(boardBotDisplay[i][j], end="   ")
            else:
                print(boardBotDisplay[i][j], end="    ")


# Prints Bot hidden board for testing purposes
# Print is messed up for the moment

def printBotHidden():
    x = 5
    while x < 16:
        print("\n")
        y = 5
        while y < 16:
            print(boardBot[x][y], end="     ")
            y += 1
        x += 1


# Intro to game and instructions

def gameIntro():
    print("\n\n        Welcome to my Battleship game!\n        Each ship space is marked with it's corresponding starting letter")
    print("\n\n        If you hit the opponents space, the '?' will turn into a '!'")
    print("\n        If you destroy an opponents ship, the '!' marks each turn into a '*'")
    print("\n        Below your 4 ships are listed: a Battleship, a Cruiser, a Frigate, and a GunBoat -->")
    print("\n\n     B  C  F  G\n     B  C  F  G\n     B  C  F\n     B  C\n     B")
    print("\n\n     Enter each space for your ships by typing in the corresponding spot such as 'A5'")
    print("\n\n     DO NOT DIAGONALLY PLACE SHIP PIECES! If you do so, restart program!:")


# Initialize placement of Player ships

def placementInit(inputstring, shippiece):
    stringIn = inputstring
    length = len(inputstring)

    # If player inputs column 10 or 11, we want access to 3 string elements:

    if length == 3:
        numberIn = int(inputstring[2])
        if numberIn == 0:
            check = placement(stringIn, 10, shippiece)
            if check:
                return True
            else:
                return False
        elif numberIn == 1:
            check = placement(stringIn, 11, shippiece)
            if check:
                return True
            else:
                return False

    # If spot is in column 1-9:

    elif length == 2:
        numberIn = int(inputstring[1])
        check = placement(stringIn, numberIn, shippiece)
        if check:
            return True
        else:
            return False
    else:
        print('Invalid input length provided!')
        return False


# Handle placement of Player ships

def placement(stringinput, numberinput, shippiece):
    numberIn = numberinput

    # Convert string to character, and then use corresponding ord() value to compare
    charToInt = ord(stringinput[0])

    # For capital letters:

    if charToInt < 97:
        if boardP[charToInt - 64][numberIn] == ".":
            boardP[charToInt - 64][numberIn] = shippiece
        else:
            return False

    # For lowercase letters:

    else:
        if boardP[charToInt - 96][numberIn] == ".":
            boardP[charToInt - 96][numberIn] = shippiece
        else:
            return False

    return True

# Handles placement of AI ship spots

def botPlacement():
    x = 1
    # Extend bot board

    # Generate random initial spot for ship placement

    while x < 5:
        randRowInit = randint(5, 16)
        randColInit = randint(5, 16)

        # Place Battleship spots

        if x == 1:
            boardBot[randRowInit][randColInit] = "B"

            # Give bot a random direction (up, down, left, right) to continue spot placement

            continueCheck = True
            while continueCheck:
                randDirection = randint(1, 5)
                finalLoop = 1
                finalCheck = True

                # Check and place next 4 spots down

                if randDirection == 1:
                    while finalLoop < 5:
                        if boardBot[randRowInit + finalLoop][randColInit] != ".":
                            finalCheck = False
                            finalLoop = 5
                        else:
                             finalLoop += 1
                    if finalCheck:
                          for i in range(1, 5):
                              boardBot[randRowInit + i][randColInit] = "B"
                          continueCheck = False
                          x += 1

                # Check and place next 4 spots up

                elif randDirection == 2:
                     while finalLoop < 5:
                        if boardBot[randRowInit - finalLoop][randColInit] != ".":
                            finalCheck = False
                            finalLoop = 5
                        else:
                            finalLoop += 1
                     if finalCheck:
                        for i in range(1, 5):
                            boardBot[randRowInit - i][randColInit] = "B"
                        continueCheck = False
                        x += 1

                # Check and place next 4 spots left

                elif randDirection == 3:
                      while finalLoop < 5:
                        if boardBot[randRowInit][randColInit - finalLoop] != ".":
                            finalCheck = False
                            finalLoop = 5
                        else:
                            finalLoop += 1
                      if finalCheck:
                        for i in range(1, 5):
                            boardBot[randRowInit][randColInit - i] = "B"
                        continueCheck = False
                        x += 1

                # Check and place next 4 spots right

                elif randDirection == 4:
                    while finalLoop < 5:
                        if boardBot[randRowInit][randColInit + finalLoop] != ".":
                            finalCheck = False
                            finalLoop = 5
                        else:
                            finalLoop += 1
                    if finalCheck:
                        for i in range(1, 5):
                            boardBot[randRowInit][randColInit + i] = "B"
                        continueCheck = False
                        x += 1

        # Place Cruiser spots

        elif x == 2:
            initCheck = True
            if boardBot[randRowInit][randColInit] == ".":
                boardBot[randRowInit][randColInit] = "C"
            else:
                initCheck = False

            # Give bot a random direction (up, down, left, right) to continue spot placement

            if initCheck:
                continueCheck = True
                while continueCheck:
                    randDirection = randint(1, 5)

                    # Check and place next 3 spots down

                    finalLoop = 1
                    finalCheck = True
                    if randDirection == 1:
                        while finalLoop < 4:
                            if boardBot[randRowInit + finalLoop][randColInit] != ".":
                                finalCheck = False
                                finalLoop = 4
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 4):
                                boardBot[randRowInit + i][randColInit] = "C"
                                continueCheck = False
                                x = 3

                    # Check and place next 3 spots up

                    elif randDirection == 2:
                        while finalLoop < 4:
                            if boardBot[randRowInit - finalLoop][randColInit] != ".":
                                finalCheck = False
                                finalLoop = 4
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 4):
                                boardBot[randRowInit - i][randColInit] = "C"
                                continueCheck = False
                                x = 3

                    # Check and place next 3 spots left

                    elif randDirection == 3:
                        while finalLoop < 4:
                            if boardBot[randRowInit][randColInit - finalLoop] != ".":
                                finalCheck = False
                                finalLoop = 4
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 4):
                                boardBot[randRowInit][randColInit - i] = "C"
                                continueCheck = False
                                x = 3

                    # Check and place next 3 spots right

                    elif randDirection == 4:
                        while finalLoop < 4:
                            if boardBot[randRowInit][randColInit + finalLoop] != ".":
                                finalCheck = False
                                finalLoop = 4
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 4):
                                boardBot[randRowInit][randColInit + i] = "C"
                                continueCheck = False
                                x = 3

        # Place Frigate spots

        elif x == 3:
            initCheck = True
            if boardBot[randRowInit][randColInit] == ".":
                boardBot[randRowInit][randColInit] = "F"
            else:
                initCheck = False

            # Give bot a random direction (up, down, left, right) to continue spot placement

            if initCheck:
                continueCheck = True
                while continueCheck:
                    randDirection = randint(1, 5)

                    # Check and place next 2 spots down

                    finalLoop = 1
                    finalCheck = True
                    if randDirection == 1:
                        while finalLoop < 3:
                            if boardBot[randRowInit + finalLoop][randColInit] != ".":
                                finalCheck = False
                                finalLoop = 3
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 3):
                                boardBot[randRowInit + i][randColInit] = "F"
                                continueCheck = False
                                x = 4

                    # Check and place next 2 spots up

                    elif randDirection == 2:
                        while finalLoop < 3:
                            if boardBot[randRowInit - finalLoop][randColInit] != ".":
                                finalCheck = False
                                finalLoop = 3
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 3):
                                boardBot[randRowInit - i][randColInit] = "F"
                                continueCheck = False
                                x = 4

                    # Check and place next 2 spots left

                    elif randDirection == 3:
                        while finalLoop < 3:
                            if boardBot[randRowInit][randColInit - finalLoop] != ".":
                                finalCheck = False
                                finalLoop = 3
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 3):
                                boardBot[randRowInit][randColInit - i] = "F"
                                continueCheck = False
                                x = 4

                    # Check and place next 2 spots right

                    elif randDirection == 4:
                        while finalLoop < 3:
                            if boardBot[randRowInit][randColInit + finalLoop] != ".":
                                finalCheck = False
                                finalLoop = 3
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 3):
                                boardBot[randRowInit][randColInit + i] = "F"
                                continueCheck = False
                                x = 4

        # Place Gunboat spots

        elif x == 4:
            randRowInit = randint(5, 16)
            randColInit = randint(5, 16)
            initCheck = True
            if boardBot[randRowInit][randColInit] == ".":
                boardBot[randRowInit][randColInit] = "G"
            else:
                initCheck = False

            # Give bot a random direction (up, down, left, right) to continue spot placement

            if initCheck:
                continueCheck = True
                while continueCheck:
                    randDirection = randint(1, 5)

                    # Check and place next spot down

                    finalLoop = 1
                    finalCheck = True
                    if randDirection == 1:
                        while finalLoop < 2:
                            if boardBot[randRowInit + finalLoop][randColInit] != ".":
                                finalCheck = False
                                finalLoop = 2
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 2):
                                boardBot[randRowInit + i][randColInit] = "G"
                                continueCheck = False
                                x += 1

                    # Check and place next spot up

                    elif randDirection == 2:
                        while finalLoop < 2:
                            if boardBot[randRowInit - finalLoop][randColInit] != ".":
                                finalCheck = False
                                finalLoop = 2
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 2):
                                boardBot[randRowInit - i][randColInit] = "G"
                                continueCheck = False
                                x += 1

                    # Check and place next spot left

                    elif randDirection == 3:
                        while finalLoop < 2:
                            if boardBot[randRowInit][randColInit - finalLoop] != ".":
                                finalCheck = False
                                finalLoop = 2
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 2):
                                boardBot[randRowInit][randColInit - i] = "G"
                                continueCheck = False
                                x += 1

                    # Check and place next spot right

                    elif randDirection == 4:
                        while finalLoop < 2:
                            if boardBot[randRowInit][randColInit + finalLoop] != ".":
                                finalCheck = False
                                finalLoop = 2
                            else:
                                finalLoop += 1
                        if finalCheck:
                            for i in range(1, 2):
                                boardBot[randRowInit][randColInit + i] = "G"
                                continueCheck = False
                                x += 1



# Handles input for player ship spots

def createBoard():
    j = 1
    battleshipPiece = "B"
    cruiserPiece = "C"
    frigatePiece = "F"
    gunboatPiece = "G"
    while j < 6:
        printPBoard()
        inputstring = input("\n\nEnter spot " + str(j) + " for your Battleship -->")
        print(inputstring)
        checkSpot = placementInit(inputstring, battleshipPiece)
        if checkSpot:
            j += 1
        else:
            print(inputstring, " is not a valid spot! Choose again -->")
    j = 1
    while j < 5:
        printPBoard()
        inputstring = input("\n\nEnter spot " + str(j) + " for your Cruiser -->")
        print(inputstring)
        checkSpot = placementInit(inputstring, cruiserPiece)
        if checkSpot:
            j += 1
        else:
            print(inputstring, " is not a valid spot! Choose again -->")
    j = 1
    while j < 4:
        printPBoard()
        inputstring = input("\n\nEnter spot " + str(j) + " for your Frigate -->")
        print(inputstring)
        checkSpot = placementInit(inputstring, frigatePiece)
        if checkSpot:
            j += 1
        else:
            print(inputstring, " is not a valid spot! Choose again -->")
    j = 1
    while j < 3:
        printPBoard()
        inputstring = input("\n\nEnter spot " + str(j) + " for your GunBoat -->")
        print(inputstring)
        checkSpot = placementInit(inputstring, gunboatPiece)
        if checkSpot:
            j += 1
        else:
            print(inputstring, " is not a valid spot! Choose again -->")

# Handle bot turn

# def botTurn():


# Handle Player turn

def playerTurn(spot):
     if spot:


# def checkTurn():




# Master function

def main():
    # gameIntro()
    # createBoard()
    # printPBoard()
    botPlacement()
    printBotHidden()

   # Game loop
    gameLoop = True
    while gameLoop:
        # checkTurn()
        playerSpot = input("\nEnter spot to attack:")
        playerTurn(playerSpot)
        # checkTurn()
        # botTurn()
    printPBoard()


main()

