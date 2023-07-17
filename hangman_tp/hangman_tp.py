#About 90% of the lopps are original from the owner of the hangman file they just needed to be properly reordered and used well
#many problems in menu display for moderate level were seen but in this code everything is well maintained
#all of the possible issues are completely solved as much as i could
# before running the code make sure you put "pip install tabulate" in your terminal or else the tabulate library will not work for tabulationn
#3 additional lists of words are added as you can check below
#I had a lot of fun doing this assignment and debugging it hope you find this work satisfactory and make sure you understand the loops well.



import random
import sqlite3
from tabulate import tabulate
# Hangman ASCII art
HANGMAN_PICS = [ #this list of images is used for visualizing the hangman
    '''                         
     +---+
         |
         |
         |
        ===''',
    '''
     +---+
     O   |
         |
         |
        ===''',
    '''
     +---+
     O   |
     |   |
         |
        ===''',
    '''
     +---+
     O   |
    /|   |
         |
        ===''',
    '''
     +---+
     O   |
    /|\  |
         |
        ===''',
    '''
     +---+
     O   |
    /|\  |
    /    |
        ===''',
    '''
     +---+
     O   |
    /|\  |
    / \  |
        ===''',
    '''
     +---+
    [O   |
    /|\  |
    / \  |
        ===''',
    '''
     +---+
    [O]  |
    /|\  |
    / \  |
        ==='''
]

# Sets of secret words
animal_words = ['ant', 'baboon', 'badger', 'bat', 'bear', 'beaver', 'camel', 'cat', 'clam', 'cobra']
shape_words = ['square', 'triangle', 'rectangle', 'circle', 'ellipse', 'rhombus', 'trapezoid']
place_words = ['Cairo', 'London', 'Paris', 'Baghdad', 'Istanbul', 'Riyadh']
bird_names = ['Eagle', 'Robin', 'Sparrow', 'Hawk', 'Owl', 'Penguin', 'Flamingo', 'Parrot', 'Peacock', 'Swan']
car_names = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes-Benz', 'Audi', 'Tesla', 'Nissan', 'Volkswagen']
stationery_names = ['Pen', 'Pencil', 'Eraser', 'Notebook', 'Stapler', 'Highlighter', 'Ruler', 'Scissors', 'Glue Stick', 'Marker']
#birds , cars and stationery names are additionals as asked in the assignment pdf


# Database connection
conn = sqlite3.connect('hangman_records.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS records
             (id INTEGER PRIMARY KEY AUTOINCREMENT, player_name TEXT, level TEXT, remaining_lives INTEGER)''')


# Function to get a random word from a word list
def getRandomWord(wordList):
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]


# Function to display the hangman board
def displayBoard(missedLetters, correctLetters, secretWord, level, maxGuesses):
    if level == 'Easy':
        print(HANGMAN_PICS[len(missedLetters)])
    elif level == 'Moderate' and len(missedLetters)<=6:
        
        print(HANGMAN_PICS[len(missedLetters)])
    elif level == 'Hard' and len(missedLetters)<=6:         #a new elif loop is used instead of the original to keep
        print(HANGMAN_PICS[len(missedLetters)])             #code understandle and easily changeable

    print()

    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i + 1:]

    for letter in blanks:
        print(letter, end=' ')
    print()
    print("Chances left:", maxGuesses - len(missedLetters))



# Function to get the user's guess
def getGuess(alreadyGuessed):
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:                                   #to keep a check for invalid inputs
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

            # Function to check if the user wants to play again



    # Function to select the set of secret words based on the chosen level

def selectWordSet(level):
    if level == 'Easy':
        print("Select a set of words: Animal, Shape, or Place.")
        set_choice = input("Enter your choice: ").capitalize()
        if set_choice == 'Animal':
            return animal_words
        elif set_choice == 'Shape':         #as per the game rules the choice menu is curated for easy and moderate levels
            return shape_words
        elif set_choice == 'Place':
            return place_words
        elif set_choice == 'Birds':
            return bird_names
        elif set_choice == 'Cars':
            return car_names
        elif set_choice == 'Stationery':
            return stationery_names
        else:
            print("Invalid choice. Defaulting to animal words.")
            return animal_words
    elif level == 'Moderate':
        print("Select a set of words: Animal, Shape, or Place.")
        set_choice = input("Enter your choice: ").capitalize()
        if set_choice == 'Animal':
            return animal_words
        elif set_choice == 'Shape':
            return shape_words
        elif set_choice == 'Place':
            return place_words
        elif set_choice == 'Birds':
            return bird_names
        elif set_choice == 'Cars':
            return car_names
        elif set_choice == 'Stationery':
            return stationery_names
        else:
            print("Invalid choice. Defaulting to animal words.")
            return animal_words
    else:  # Hard level
        return random.choice([animal_words, shape_words, place_words,bird_names,car_names,stationery_names])

    # Function to display the hall of fame records

def displayHallOfFame():
    c.execute("SELECT * FROM records ORDER BY remaining_lives DESC")
    records = c.fetchall()
    headers = ["Level", "Winner Name", "Remaining Lives"]
    table_data = []

    for record in records:
        table_data.append([record[2], record[1], record[3]])
                                                                    #tabulate helps you visualise the data in table format
    table = tabulate(table_data, headers, tablefmt="fancy_grid")
    print("\nHALL OF FAME")
    print(table)


    # Function to update the hall of fame records
def updateHallOfFame(player_name, level, remaining_lives):
    # Retrieve the current highest remaining lives for the specific level from the database
    c.execute("SELECT MAX(remaining_lives) FROM records WHERE level = ?", (level,))
    highest_remaining_lives = c.fetchone()[0]

    if highest_remaining_lives is None or remaining_lives > highest_remaining_lives:
        # Delete existing records with the same level and lower remaining lives
        c.execute("DELETE FROM records WHERE level = ? AND remaining_lives < ?", (level, remaining_lives))
        conn.commit()

        # Insert the new record
        c.execute("INSERT INTO records (player_name, level, remaining_lives) VALUES (?, ?, ?)",
                  (player_name, level, remaining_lives))
        conn.commit()



    # Function to display the introductory menu

def displayIntroMenu(player_name):
    menu = [
        ["Hi " + player_name + "."],
      [ "Welcome to HANGMAN"],
        [ "PLAY THE GAME\nEasy level 1     Moderate level 2     Hard level 3"],
        [ "Hall of fame 4"],
        [ "About the game 5"]
    ]

    
    print()
    table=(tabulate(menu, tablefmt="fancy_grid"))
    centered_table = "\n".join([line.center(len(table.split("\n")[0])) for line in table.split("\n")])
    print(centered_table)    


    # Function to display the sets of secret words menu

def displayWordSetMenu():
    print("SELECT FROM THE FOLLOWING SETS OF SECRET WORDS")
    word_sets = [
        ["Animals", "1"],
        ["Shapes", "2"],
        ["Places", "3"],
        ["Birds", "4"],
        ["Cars", "5"],
        ["Stationery", "6"]
    ]

    table = tabulate(word_sets, tablefmt="fancy_grid")
    centered_table = "\n".join([line.center(len(table.split("\n")[0])) for line in table.split("\n")])
    print(centered_table)


    # Function to display the about the game menu

def displayAboutMenu():
    about = [
        ["ABOUT THE GAME"],
        ["Easy: You can select the list from which the random word will be chosen (Animal, Shape, Place).\nThe number of trials is 8."],
        [ "Moderate: Similar to Easy, but the number of trials is 6. The last two graphics will not be displayed."],
        [ "Hard: The code will randomly select a set of words and a word from the set. You have no clue about the secret word.\nThe number of trials is 6."]
    ]

    table = tabulate(about, tablefmt="fancy_grid")
    centered_table = "\n".join([line.center(len(table.split("\n")[0])) for line in table.split("\n")])
    print(centered_table)


    # Main game loop

def playHangman():
    def gameLoop(player_name, level, secretWord, maxGuesses):
        missedLetters = ''
        correctLetters = ''
        gameIsDone = False
    
        while True:
            displayBoard(missedLetters, correctLetters, secretWord, level, maxGuesses)
    
            guess = getGuess(missedLetters + correctLetters)
    
            if guess in secretWord:
                correctLetters += guess
    
                # Check if the player has won
                foundAllLetters = True
                for i in range(len(secretWord)):
                    if secretWord[i] not in correctLetters:
                        foundAllLetters = False
                        break
    
                if foundAllLetters:
                    print(f"\nCongratulations, {player_name}! You won!")
                    gameIsDone = True
    
            else:
                missedLetters += guess
    
                # Check if the player has lost
                if len(missedLetters) == maxGuesses:
                    displayBoard(missedLetters, correctLetters, secretWord, level, maxGuesses)
                    print(f"\nSorry, {player_name}, you have run out of guesses!")
                    print(f"The secret word was '{secretWord}'. Better luck next time!")
                    gameIsDone = True
    
            if gameIsDone:
                # Update the hall of fame records if the player won
                if len(missedLetters) < maxGuesses:
                    updateHallOfFame(player_name, level, maxGuesses - len(missedLetters))
                break
    
    def playAgain():
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')
    
    print('H A N G M A N')

    player_name = input("Enter your name: ")
    displayIntroMenu(player_name)
    game=False
    while True:
        
        choice = input("Enter your choice from the Menu : ")

        if choice == '1':
            game=True
            level = 'Easy'
            displayWordSetMenu()
            wordSetChoice = input("Enter your choice: ")

            if wordSetChoice == '1':
                wordSet = animal_words
            elif wordSetChoice == '2':
                wordSet = shape_words
            elif wordSetChoice == '3':
                wordSet = place_words
            elif wordSetChoice == '4':
                wordSet = bird_names
            elif wordSetChoice == '5':
                wordSet = car_names
            elif wordSetChoice == '6':
                wordSet = stationery_names
            else:
                print("Invalid choice. Defaulting to animal words.")
                wordSet = animal_words

            secretWord = getRandomWord(wordSet)
            maxGuesses = 8

            gameLoop(player_name, level, secretWord, maxGuesses)

        elif choice == '2':
            game=True
            level = 'Moderate'
            displayWordSetMenu()
            wordSetChoice = input("Enter your choice: ")

            if wordSetChoice == '1':
                wordSet = animal_words
            elif wordSetChoice == '2':
                wordSet = shape_words
            elif wordSetChoice == '3':
                wordSet = place_words
            elif wordSetChoice == '4':
                wordSet = bird_names
            elif wordSetChoice == '5':
                wordSet = car_names
            elif wordSetChoice == '6':
                wordSet = stationery_names
            else:
                print("Invalid choice. Defaulting to animal words.")
                wordSet = animal_words

            secretWord = getRandomWord(wordSet)
            maxGuesses = 6

            gameLoop(player_name, level, secretWord, maxGuesses)

        elif choice == '3':
            game=True
            level = 'Hard'
            wordSet = selectWordSet(level)
            secretWord = getRandomWord(wordSet)
            maxGuesses = 6

            gameLoop(player_name, level, secretWord, maxGuesses)

        elif choice == '4':
            displayHallOfFame()
            return
        elif choice == '5':
            displayAboutMenu()
            return
        else:
            print("Invalid choice. Please try again.")
            
        
        if(game):
            again=playAgain()
            if (again): 
                playHangman()                
            else:       
                print ("Thank you for playing!")            #this is the last message if you wish to exit the game after playing
                game=False              #the game bool variable keeps a check that play again dialogue does not come up again
                return
                
        
    conn.close()
        
# Start the game
playHangman()
