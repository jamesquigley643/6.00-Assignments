# Problem Set 2
# Name: James Quigley
# Collaborators: None
# Time Spent: 4 hours
# Late Days Used: S^3 requested extension 
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    guessed_word = True
    for char in secret_word:
      if not (char in letters_guessed):
        guessed_word = False
        return guessed_word      
    
    return guessed_word



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes the letters in
      secret_word are all lowercase.
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters and asterisks (*) that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_string = ""
    for char in secret_word:
        if (char in letters_guessed):
            guessed_string += char
        else:
            guessed_string += "*"
    return guessed_string



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which 
      letters have not yet been guessed. The letters should be returned in
      alphabetical order.
    '''
    letters = string.ascii_lowercase
    not_guessed = ""
    for char in letters:
      if char not in letters_guessed:
        not_guessed += char
    return not_guessed
    
def compute_score(guesses_remaining, secret_word):
    unique_letters = []
    for letter in secret_word:
        if letter not in unique_letters:
            unique_letters.append(letter)
    unique_chars = len(unique_letters)
    score = guesses_remaining + unique_chars * len(secret_word)
    return score    

def random_letter(secret_word, get_available_letters):
    letters_guessed = []
    choose_from = ""
    for char in secret_word:
      if char in get_available_letters(letters_guessed):
          choose_from += char     
          new = random.randint(0, len(choose_from)-1) 
          exposed_letter = choose_from[new]
    return exposed_letter

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses they start with.
      
    * The user should start with 10 guesses.

    * Before each round, you should display to the user how many guesses
      they have left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''    
    letters_guessed = []
    guesses = 10
    duplicate_guesses = []
    display = "*" * len(secret_word)
    unique_letters = ""
    for char in secret_word:
        if char not in unique_letters:
            unique_letters += char
    print("Welcome to Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    print("------")
    
    while True:
#first we print the letter and ask for our guess        
        letters_left = get_available_letters(letters_guessed)
        print("You have",str(guesses),"guesses left.")
        print("Available letters: ",letters_left)
        my_guess = input("Please guess a letter: ").lower()
#now we check if the guess is legal (an alphabetic character)        
        if not my_guess.isalpha():
            print("That is not a valid input")
            print("------")
        else:
#next we remove the guess from available letters            
            if my_guess not in letters_guessed:
                letters_guessed.append(my_guess)
            end_game = is_word_guessed(secret_word, letters_guessed)
#if the guess completes the word we go to end game            
            if end_game:
                display = (get_guessed_word(secret_word, letters_guessed))
                print("Good guess: " + display)
                print("------")
                print("Congratulations, you won!")
                total_score = (guesses + 2*len(secret_word)*len(unique_letters))
                print("Your total score for this game is: ", total_score)                      
                break
#if the guess has already been made, we warn the player            
            elif my_guess in duplicate_guesses:
                print("That letter has been guessed before")
                print("------")
#if the guess is correct, we append the available letters and display                 
            elif (not(my_guess in duplicate_guesses)) and my_guess in secret_word:
                display = (get_guessed_word(secret_word, letters_guessed))
                print("Good guess: ", display)
                print("------")
#if the guess is wrong, we deduct a guess, or -2 for a wrong vowel                
            elif my_guess not in secret_word:
                if my_guess in ["a", "i", "e", "u", "o"] and guesses >1:
                    guesses = guesses - 2
                    print("Oops! That letter is not in my word: ", display)
                    print("------")
                elif guesses > 1:
                    guesses = guesses - 1
                    print("Oops! That letter is not in my word: ", display)
                    print("------")
#if the player runs out of guesses, we terminate the game                    
                else:
                    print("Oops! That letter is not in my word: ", display)
                    print("------")
                    print("Sorry, you ran out of guesses. The word was ", secret_word, ".")
                    break
            duplicate_guesses.append(my_guess)
            
                    








# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------

    
def hangman_with_help(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses they start with.
      
    * The user should start with 10 guesses.
    
    * Before each round, you should display to the user how many guesses
      they have left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make sure that
      the user puts in a letter.
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol %, you should reveal to the user one of the 
      letters missing from the word at the cost of 2 guesses. If the user does 
      not have 2 guesses remaining, print a warning message. Otherwise, add 
      this letter to their guessed word and continue playing normally.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    letters_guessed = []
    guesses = 10
    duplicate_guesses = []
    display = "*" * len(secret_word)
    unique_letters = ""
    for char in secret_word:
        if char not in unique_letters:
            unique_letters += char
    print("Welcome to Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    print("------")
    
    while True:
        letters_left = get_available_letters(letters_guessed)
        print("You have ", str(guesses), " guesses left.")
        print("Available letters: ",letters_left)
        my_guess = input("Please guess a letter: ").lower()
# This block is the help function, and represents the only difference from before        
        if my_guess == "%":
            if guesses <= 2:
                print("Oops! Not enough guesses left: ", display)
            else:
                guesses = guesses - 2
                help_letter = random_letter(secret_word, get_available_letters)
                letters_guessed.append(help_letter)
                display = (get_guessed_word(secret_word, letters_guessed))
                print("Letter revealed: ", help_letter)
                print(display)
                print("------")
                
        elif not my_guess.isalpha():
            print("That is not a valid input")
            print("------")
        else:
            if my_guess not in letters_guessed:
                letters_guessed.append(my_guess)
            end_game = is_word_guessed(secret_word, letters_guessed)
            
            if end_game:
                print("Good guess: " + display)
                print("------")
                print("Congratulations, you won!")
                total_score = (guesses + 2*len(secret_word)*len(unique_letters))
                print("Your total score for this game is: ", total_score)                      
                break
            elif my_guess in duplicate_guesses:
                print("That letter has been guessed before")
                print("------")
            elif (not(my_guess in duplicate_guesses)) and my_guess in secret_word:
                display = (get_guessed_word(secret_word, letters_guessed))
                print("Good guess: ", display)
                print("------")
            elif my_guess not in secret_word:
                if my_guess in ["a", "i", "e", "u", "o"] and guesses >1:
                    guesses = guesses - 2
                    print("Oops! That letter is not in my word: ", display)
                    print("------")
                elif guesses > 1:
                    guesses = guesses - 1
                    print("Oops! That letter is not in my word: ", display)
                    print("------")
                else:
                    print("Oops! That letter is not in my word: ", display)
                    print("------")
                    print("Sorry, you ran out of guesses. The word was ", secret_word, ".")
                    break
            duplicate_guesses.append(my_guess)


# When you've completed your hangman_with_help function, comment the two similar
# lines below that were used to run the hangman function, and then uncomment
# those two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    #pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
#    
#    secret_word = choose_word(wordlist)
#    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_help(secret_word)
