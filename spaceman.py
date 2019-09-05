import random
import re
from os import system

def load_word():
    '''
    A function that reads a text file of words and randomly selects one to use as the secret word
        from the list.
    Returns: 
           string: The secret word to be used in the spaceman guessing game
    '''
    f = open('./words.txt', 'r')
    words_list = f.readlines()
    f.close()

    words_list = words_list[0].split(' ')
    secret_word = random.choice(words_list)
    return secret_word

def is_word_guessed(secret_word, letters_guessed):
    '''
    A function that checks if all the letters of the secret word have been guessed.
    Args:
        secret_word (string): the random word the user is trying to guess.
        letters_guessed (list of strings): list of letters that have been guessed so far.
    Returns: 
        bool: True only if all the letters of secret_word are in letters_guessed, False otherwise
    '''
    word = []
    for s_letter in secret_word:
        for g_letter in letters_guessed:
            if s_letter == g_letter:
                word.append(g_letter);
    return True if len(word) == len(secret_word) else False

def get_guessed_word(secret_word, letters_guessed):
    '''
    A function that is used to get a string showing the letters guessed so far in the secret word and underscores for letters that have not been guessed yet.
    Args: 
        secret_word (string): the random word the user is trying to guess.
        letters_guessed (list of strings): list of letters that have been guessed so far.
    Returns: 
        string: letters and underscores.  For letters in the word that the user has guessed correctly, the string should contain the letter at the correct position.  For letters in the word that the user has not yet guessed, shown an _ (underscore) instead.
    '''
    word = []
    for s_letter in secret_word: word.append('_')
    for index, s_letter in enumerate(secret_word):
        for g_letter in letters_guessed:
            if s_letter == g_letter:
                word[index] = g_letter
    return ' '.join(word)


def is_guess_in_word(guess, secret_word):
    '''
    A function to check if the guessed letter is in the secret word
    Args:
        guess (string): The letter the player guessed this round
        secret_word (string): The secret word
    Returns:
        bool: True if the guess is in the secret_word, False otherwise
    '''
    return True if secret_word.find(guess) != -1 else False

def has_been_guessed(guess, letters_guessed):
    '''
    A function to check if the guessed letter is in letters_guessed
    Args:
        guess (string): The letter the player guessed this round
        letters_guessed (string): The list of letters the user has guessed
    Returns:
        bool: True if the guess is in letters_guessed, False otherwise
    '''
    for letter in letters_guessed:
        if letter == guess:
            return True
    return False

def spaceman(secret_word):
    '''
    A function that controls the game of spaceman. Will start spaceman in the command line.
    Args:
      secret_word (string): the secret word to guess.
    '''
    letters_guessed = []
    guesses_left = len(secret_word)
    prompt = 'Welcome to Spaceman!'

    is_playing = True;
    while is_playing:
        current_word = get_guessed_word(secret_word, letters_guessed)

        system('clear')
        print(prompt)
        print(f'Current word: {current_word}')
        print(f'Letters guessed: {letters_guessed}')
        print(f'You have {guesses_left} guesses left, please enter one letter per round')
        print('---------------------------------------')

        if is_word_guessed(secret_word, letters_guessed):
            user_input = input('You Won! Want to play agian? Y/n ')
            if user_input == 'Y' or user_input == 'y' or user_input == '' or re.match('\s+', user_input):
                letters_guessed = []
                secret_word = load_word()
                guesses_left = len(secret_word)
            elif user_input == 'N' or user_input == 'n':
                is_playing = False

        user_guess = input('Enter a letter: ')
        while len(user_guess) > 1 or user_guess == '' or user_guess == ' ' or re.match('[a-z]', user_guess) == None:
            user_guess = input('Enter only one letter: ') 
        
        if has_been_guessed(user_guess, letters_guessed):
            prompt = f'You already guessed {user_guess}'
        elif is_guess_in_word(user_guess, secret_word):
            prompt = f'Correct! {user_guess} in the the secret word.'
            letters_guessed.append(user_guess)
        else:
            prompt = f'Incorrect. {user_guess} is not in the secret word'
            letters_guessed.append(user_guess)
            guesses_left -= 1
    
        if guesses_left == 0:
            print(f'The word was {secret_word}')
            user_input = input('You Lost! Want to try agian? Y/n ')
            if user_input == 'Y' or user_input == 'y' or user_input == '' or re.match('\s+', user_input):
                prompt = 'Welcome back to Spaceman!'
                letters_guessed = []
                secret_word = load_word()
                guesses_left = len(secret_word)
            elif user_input == 'N' or user_input == 'n':
                is_playing = False
        if is_word_guessed(secret_word, letters_guessed):
            current_word = re.sub('\s', '', current_word)

#These function calls that will start the game
secret_word = load_word()
spaceman(load_word())