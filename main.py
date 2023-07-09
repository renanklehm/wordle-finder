import pandas as pd
import os
from input_handler.handler import Handler


df = pd.read_csv('dataset\\wordle.csv')
df[['1', '2', '3', '4', '5']] = df['word'].apply(lambda x: pd.Series(list(x)))
possible_words = df['word'].values


def get_possible_words(df, correct_letters, wrong_letters, allowed_letters):

    temp1 = df[df.apply(lambda row: 
        (
            (correct_letters['1'] is None or row['1'] == correct_letters['1']) and
            (correct_letters['2'] is None or row['2'] == correct_letters['2']) and
            (correct_letters['3'] is None or row['3'] == correct_letters['3']) and
            (correct_letters['4'] is None or row['4'] == correct_letters['4']) and
            (correct_letters['5'] is None or row['5'] == correct_letters['5'])
        )
        ,axis=1
    )]
    
    temp2 = df[df.apply(lambda row: 
        (
            all(letter in row['word'] for letter in allowed_letters)
        )
        ,axis=1
    )]
    
    temp3 = df[df.apply(lambda row: 
        (
            all(letter != row['1'] for letter in wrong_letters['1']) and
            all(letter != row['2'] for letter in wrong_letters['2']) and
            all(letter != row['3'] for letter in wrong_letters['3']) and
            all(letter != row['4'] for letter in wrong_letters['4']) and
            all(letter != row['5'] for letter in wrong_letters['5'])
        )
        ,axis=1
    )]
    
    intersection = temp1.merge(temp2, on='word').merge(temp3, on='word')
    intersection.dropna(inplace=True)
    intersection.drop_duplicates(inplace=True)
    
    return intersection['word'].values

def validate_guess(guess_word, comp_word):
    score = 0
    for idx, letter in enumerate(guess_word):
        if letter in comp_word:
            if guess_word[idx] == comp_word[idx]:
                score += 1
            else:
                score += 0.5
        else:
            score -= 1
    return score


while True:
    os.system('cls')
    print('Enter the word you guessed when prompted. After that, enter the colors as g, y, n for green, yellow and none respectively.')
    handler = Handler()
    correct_letters, wrong_letters, allowed_letters = handler.get_input()
    filtered_words = get_possible_words(df, correct_letters, wrong_letters, allowed_letters)
    while(None in correct_letters.values()):
        possible_words = {}
        for candidate_guess in filtered_words:
            score = 0
            for comp_word in possible_words:
                score += validate_guess(candidate_guess, comp_word)
            possible_words[candidate_guess] = score
        possible_words = pd.DataFrame.from_dict(possible_words, orient='index', columns=['score'])
        possible_words.sort_values(by=['score'], ascending=False, inplace=True)
        print(possible_words.head(10).to_markdown())
        print('\n')
        correct_letters, wrong_letters, allowed_letters = handler.get_input()
        filtered_words = get_possible_words(df, correct_letters, wrong_letters, allowed_letters)