import random
import re
from os import system

def load_words_list():
    '''
    A function that reads a text file of words and returns an array of words
    Returns: 
           array: Reads from a text file to get the avaiable words to be selected as the secret word
    '''
    f = open('./words.txt', 'r')
    words_list = f.readlines()
    f.close()

    words_list = words_list[0].split(' ')
    return words_list

def load_word(words_list):
    '''
    A function that selects a random word from a list of words to be used as the secret word
    Args:
        array: A list of words
    Returns:
        string: A randomly selected word from the words list to be used as the secret word
    '''
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

def changed_word(current_word, secret_word, words_list):
    '''
    A function to get a new word with the same characters as the current guessed word
    Args:
        current_word (array): The characters of the current guessed word
        secret_word: The current secret word
    Returns:
        array: A list that has the same amount of letters and letters in the same index as current_word
    '''
    current_word_list = current_word.split()
    matched_expression = []
    for character in current_word_list: matched_expression.append('.')
    for i, char in enumerate(current_word_list): 
        if char != '_': 
            matched_expression[i] = char
    matched_expression = ''.join(matched_expression)

    for word in words_list:
        matched_word = re.match(matched_expression, word)
        if matched_word and re.match(f'{secret_word}', word) == None:
            return word
    return secret_word

def spaceman(secret_word, spaceman_words_list):
    '''
    A function that controls the game of spaceman. Will start spaceman in the command line.
    Args:
      secret_word (string): the secret word to guess.
    '''
    letters_guessed = []
    guesses_left = len(secret_word)
    prompt = 'Welcome to Spaceman!'
    original_secret_word = secret_word

    is_playing = True;
    while is_playing:
        current_word = get_guessed_word(secret_word, letters_guessed)
        
        system('clear')
        print(prompt)
        print(f'Current word: {current_word}')
        print(f'Letters guessed: {letters_guessed}')
        print(f'You have {guesses_left} guesses left, please enter one letter per round')
        print('---------------------------------------')

        user_guess = input('Enter a letter: ')
        user_guess = user_guess.replace(' ', '')
        while len(user_guess) > 1 or user_guess == '' or user_guess == ' ' or re.match(r'([a-z]|[A-Z])', user_guess) == None:
            user_guess = input('Enter only one letter: ') 
        user_guess = user_guess.lower()

        if has_been_guessed(user_guess, letters_guessed):
            prompt = f'You already guessed {user_guess}'
        elif is_guess_in_word(user_guess, secret_word):
            prompt = f'Correct! {user_guess} in the the secret word.'
            letters_guessed.append(user_guess)
            current_word = get_guessed_word(secret_word, letters_guessed)
            secret_word = changed_word(current_word, secret_word, spaceman_words_list)
        else:
            prompt = f'Incorrect. {user_guess} is not in the secret word'
            letters_guessed.append(user_guess)
            guesses_left -= 1
    
        if is_word_guessed(secret_word, letters_guessed):
            user_input = input('You Won! Want to play agian? Y/n ')
            if user_input == 'Y' or user_input == 'y' or user_input == '' or re.match(r'\s+', user_input):
                letters_guessed = []
                secret_word = load_word(spaceman_words_list)
                original_secret_word = secret_word
                guesses_left = len(secret_word)
            elif user_input == 'N' or user_input == 'n':
                is_playing = False
        elif guesses_left == 0:
            print(f'The word was {secret_word}')
            user_input = input('You Lost! Want to try agian? Y/n ')
            if user_input == 'Y' or user_input == 'y' or user_input == '' or re.match(r'\s+', user_input):
                prompt = 'Welcome back to Spaceman!'
                letters_guessed = []
                secret_word = load_word(spaceman_words_list)
                original_secret_word = secret_word
                guesses_left = len(secret_word)
            elif user_input == 'N' or user_input == 'n':
                is_playing = False
        if is_word_guessed(secret_word, letters_guessed):
            current_word = re.sub(r'\s', '', current_word)

def test_load_owrds_list():
    words_list = load_words_list()
    assert type(words_list) == list, 'load_words list did not return a list'

def test_load_word():
    words_list = load_words_list()
    secret_word = load_word(words_list)
    assert type(secret_word) == str, 'load_word did not return string'

def test_is_word_guessed():
    words_list = load_words_list()
    letters_guessed = ['a', 'i', 'p']
    secret_word = load_word(words_list)
    guessed = is_word_guessed(secret_word, letters_guessed)
    assert guessed == False, 'is_word_guessed did not return false'

def test_get_guessed_word():
    words_list = load_words_list()
    letters_guessed = ['a', 'i', 'p']
    secret_word = load_word(words_list)
    current_word = get_guessed_word(secret_word, letters_guessed)
    assert type(current_word) == str, 'get_guessed_word did not return a string'

def test_is_guess_in_word():
    words_list = load_words_list()
    secret_word = load_word(words_list)
    correct_guess = is_guess_in_word('r', secret_word)
    assert type(correct_guess) == bool, 'is_guess_in_word did not return a bool'

def test_has_been_guessed():
    letters_guessed = ['a', 'i', 'p']
    already_guessed = has_been_guessed('a', letters_guessed)
    assert already_guessed == True, 'has_been_guessed did not return true'

def test_changed_word():
    words_list = load_words_list()
    letters_guessed = ['a', 'i', 'p']
    secret_word = load_word(words_list)
    current_word = get_guessed_word(secret_word, letters_guessed)
    new_word = changed_word(current_word, secret_word, words_list)
    assert type(new_word) == str, 'changed_word did not return a string'

#These function calls that will start the game
if __name__ == '__main__':
    gloabal_words_list = load_words_list()
    secret_word = load_word(gloabal_words_list)
    spaceman(secret_word, gloabal_words_list)