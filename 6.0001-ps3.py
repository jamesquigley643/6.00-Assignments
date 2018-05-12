# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : James Quigley
# Collaborators : none
# Time spent    : About 4 hours

import math
import random
import string
from unittest import mock
import sys

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def test_play_game(word_list, hands, replaced_letter = None):
    """
    Allows you to play a series of pre-specified hands. 
    Will allow you to play your game (i.e. your functions/code) while 
    specifying what hands you want the computer to deal, and optionally
    what letter should be "chosen" to be added in the hand
    when you call substitute_hand. This function should help you debug your
    code/any failing play_game test cases.
    
    To use this function run your ps3.py and call the function as shown
    in example usage.
    
    ----ARGUMENTS----
    word_list: list of lowercase strings of valid words
    hands: list of dictionaries of the hands you want to play in order
    ---OPTIONAL ARGUMENTS-- (if you do not wish to use these you
                              don't need to pass them in)
                              
    replaced_letter: string letter that you want substitute_hand
                     to chose as a new letter
                     
    Example usage w/o substitution:
    Suppose you want to play the game with two hands shown below.
    h1 = {'a':1, 'b':1, 'c':1, 'e':1, '%': 1}
    h2 = {'z':1, 'y':1, 'u':1, 'a':1, '%': 1}
    hands = [h1,h2]
    test_play_game(word_list, hands)

    Example usage w/ substitution:
    Suppose you want to play the game with two hands shown below and you want
    the "random" letter chosen by substitute hand to be "t".
    h1 = {'a':1, 'b':1, 'c':1, 'e':1, '%': 1}
    h2 = {'z':1, 'y':1, 'u':1, 'a':1, '%': 1}
    hands = [h1,h2]
    letter = 't'
    test_play_game(word_list, hands, letter)
    
    """
    def replace_letter_mock(hand, letter):
        """
        Replaces the chosen letter with replaced_letter
        """
        num = hand[letter]
        del hand[letter]
        hand[replaced_letter] = num
        return hand
    deal_hand_function = sys.modules[__name__].deal_hand 
    substitute_hand_function = sys.modules[__name__].substitute_hand
    sys.modules[__name__].deal_hand = mock.Mock(side_effect=hands)
    if replaced_letter:
        sys.modules[__name__].substitute_hand = mock.Mock(side_effect=replace_letter_mock)
    play_game(word_list)
    sys.modules[__name__].substitute_hand = substitute_hand_function
    sys.modules[__name__].deal_hand = deal_hand_function

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only 
    contain lowercase letters, so you will have to handle uppercase and mixed 
    case strings appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            3, or
            4 * word_length + 7 * (word_length-n), where wordlen is the length of the 
            word and n is the hand length when the word was played.

    Letters are scored as in Scrabble: A is worth 1, B is worth 3, 
    C is worth 3, D is worth 2, E is worth 1, and so on (provided in 
    SCRABBLE_LETTER_VALUES above).

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
    total = 0
    # the total score 
    for i in word:
    #iterate through the word
        if i != '%':
            if (4*len(word) + 7*(len(word) - n)) > 3:
            #check which value is largest to be the second component
                total += SCRABBLE_LETTER_VALUES[i.lower()]*(4*len(word) + 7*(len(word) - n))
            else:
                total += SCRABBLE_LETTER_VALUES[i.lower()]*3

    return total
    #return score


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    myHand = hand.copy()
    #copy hand to a new variable so we dont over write it
    for i in word:
        i = i.lower()
        #ignore caps by making all letters lower
        if i in hand.keys():
            myHand[i] = myHand[i] - 1
            #hand loses a letter if the player uses it. 
    return myHand
    #returns updated dictionary

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand (that is, there are enough of 
    each letter in the hand to construct the word). Otherwise, 
    returns False.
    Does not mutate hand or word_list.
   
    For Problem #4, returns True if replacing the wildcard % with 
    a consonant forms a word in word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    word = word.lower()
    #to ignore caps
    myHand = hand.copy()
    #same as before, new variable for copy
    
    if not "%" in word:
    #check if wildcard is used
        result = True
        for letter in word:
            if myHand.get(letter,0) < word.count(letter):
            #makes sure enough letters exist in the hand ot make the word
                result = False 
        if result and word in word_list:
            return True
        return False
    
    else:
    #for wildcard
        for i in CONSONANTS:
            if word.replace("%",i) in word_list:
            #check for all the consonants that can make a word when replaced with %
                myWord = word.replace("%",i)
                #new word that replaces the %
                otherHand = myHand.copy()
                otherHand[i] = otherHand.get(i,0)+1
                #increment 1 for value of keys of dictionary
                result = True
                for let in myWord:
                    if otherHand.get(let,0) < myWord.count(let):
                        result = False
                if myWord in word_list and result:
                    return True
                return False

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    total = 0
    for a in hand.keys():
        total = total + hand[a]
        #sum values of keys in the hand
    return total

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing 
      the string '*END*' instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    total = 0
    # Keep track of the total score
    while calculate_handlen(hand) > 0:
    # As long as there are still letters left in the hand:
        print("Current Hand:")
        display_hand(hand)
        # Display the hand
        word=input('Enter word, or "*END*" to indicate that you are finished:')
        # Ask user for input
        if word == "*END*":
        # If the input is *END*:
            break
            # End the game (break out of the loop)

        else:  
        # Otherwise (the input is not *END*):
            if is_valid_word(word, hand, word_list):
                n = calculate_handlen(hand)
                total += get_word_score(word, n)
            # If the word is valid:
                print('"'+word+'"', "earned", get_word_score(word, n), "points. Total:", total, "points")
                
                # Tell the user how many points the word earned,
                # and the updated total score
            else:
            # Otherwise (the word is not valid):
                print("The word is not valid.")
                # Reject invalid word (print a message)
            hand=update_hand(hand, word)    
            # update the user's hand by removing the letters of their inputted word
            
    
    print("Total score for this hand:", total, "points")
    # Game is over (user entered '*END*' or ran out of letters),
    # so tell user the total score
    return total
    # Return the total score



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from VOWELS if the user chooses a VOWEL and 
    CONSONANTS if the user chooses a CONSONANT). The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.
    
    You can assume that letter is in the hand. Users can not substitute
    the wildcard, so you can also assume letter is not '%'.

    If the user substitutes a VOWEL, they should only get back a VOWEL.
    If a user substitutes a CONSONANT, they should only get back a CONSONANT.

    Has no side effects: does not mutate hand.
    

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
        
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand. The new letter should not be 'a','e', 'i','o', or 'u'
    as a consonant should only be subsituted for a consonant.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    myHand = hand.copy()
    #Same as before, to protect hand we make a new variable for it
    
    if letter in VOWELS:
    #if the letter we sub is in vowels, we sub with a vowel that isnt in the hand
        myLetters=""
        #replacements for the initial letter are stored here
        for i in VOWELS:
            if not i in myHand.keys() and i != letter:
                myLetters = myLetters + i
            #checks to make sure the letter isnt already in the hand
                    
        if not len(myLetters)==0:
        #if we can sub the letter
            p = random.choice(myLetters)
            #choose a random consonant from the list of valid letters to be used
            myHand[p] = myHand.pop(letter)
            #replace the existing key with the new one, being careful to store its value so that it doesn't change
        return myHand
        #returns myHand with the new letter

    
    elif letter in CONSONANTS:
        myLetters=""
        
        for i in CONSONANTS:
            if not i in myHand.keys() and i != letter:
                    myLetters = myLetters + i
                    
        if not len(myLetters)==0:
            p = random.choice(myLetters)
            myHand[p] = myHand.pop(letter)
            
        return myHand
    #same as before but with consonants instead of vowels
def play_game(word_list):
    """
    Allow the user to play a series of hands.

    * Asks the user to input a total number of hands to play.

    * Accumulates the score for each hand into a total score for the 
      entire series.
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done ONCE during the entire game. Once 
      the substitute option is used, the user should not be asked if they want 
      to substitute letters for the rest of the game.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand (i.e. the better of the two
      is added to the total score for the game).  This can only be done ONCE 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

    * NOTE: if you replay a hand, you do NOT get the option to substitute
      a letter - you must play whatever hand you just had. If you subsitute a 
      letter before you replay, you must use the updated hand with the
      subsituted letter when replaying.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    myScore = []
    #initialize my score
    
    howManyHands = int(input("Enter total number of hands:"))
    #input for how long to play
    for i in range(howManyHands):
    #as long as the nomber of hands is greater than one, the user will be able to play hands
        firstHand = deal_hand(HAND_SIZE)
        #to retrieve a hand by calling deal_hand
        count = 1
        #count for substitutions 
        print("Current hand:")
        display_hand(firstHand)
        #display firstHand by calling display_hand
        if count == 1:
            myAnswer = input("Would you like to substitute a letter?")
            if myAnswer == "yes":
                letter = input("Which letter would you like to replace:")
                hand = substitute_hand(firstHand, letter)
                #substitute the hand (can only use once)
                count = 0
            else:
                hand = firstHand
                #otherwise the hand doesn't change
                
        myScore.append(play_hand(hand, word_list))
        #change myScoure by calling play_hand
        print("----------")
    
        count2 = 1
        #counter for replaying a hand
        if count2 == 1:
            myAnswer2 = input("Would you like to replay the hand?")
            if myAnswer2 == "yes":
                otherScore = play_hand(hand, word_list)
                myScore[-1] = max(myScore[-1], otherScore)
                #player gets the best score out of the two hands if replayed

    print("----------")
    print("Total score over all hands:", sum(myScore))
    return sum(myScore)

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
# While debugging, you may want to TEMPORARILY comment out play_game(word_list)

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
