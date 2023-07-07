import pandas as pd
import os
from tqdm import tqdm
from input_handler.handler import Handler


df = pd.read_csv('dataset\\wordle.csv')
df[['1', '2', '3', '4', '5']] = df['word'].apply(lambda x: pd.Series(list(x)))
possible_words = df['word'].values


def get_possible_words(df, correct_letters, partial_letters, wrong_letters):
    allowed_letters = (list(correct_letters.values()) + [x[i] for x in partial_letters.values() for i in range(len(x))])
    while None in allowed_letters:
        allowed_letters.remove(None)
    temp = df[df.apply(lambda row: 
        (
            (
                (correct_letters['1'] is None or row['1'] == correct_letters['1'])     and
                (correct_letters['2'] is None or row['2'] == correct_letters['2'])     and
                (correct_letters['3'] is None or row['3'] == correct_letters['3'])     and
                (correct_letters['4'] is None or row['4'] == correct_letters['4'])     and
                (correct_letters['5'] is None or row['5'] == correct_letters['5'])     and
                all(letter in row['word'] for letter in allowed_letters)               and 
                not any(letter in row['word'] for letter in wrong_letters)             and
                all(letter not in row['1'] for letter in partial_letters['1'])         and
                all(letter not in row['2'] for letter in partial_letters['2'])         and
                all(letter not in row['3'] for letter in partial_letters['3'])         and
                all(letter not in row['4'] for letter in partial_letters['4'])         and
                all(letter not in row['5'] for letter in partial_letters['5'])
            )
        )
        ,axis=1
    )]
    return temp['word'].values

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
    handler = Handler()
    correct_letters, partial_letters, wrong_letters = handler.get_input()
    filtered_words = get_possible_words(df, correct_letters, partial_letters, wrong_letters)
    while(None in correct_letters.values()):
        possible_words = {}
        for candidate_guess in tqdm(filtered_words):
            score = 0
            for comp_word in possible_words:
                score += validate_guess(candidate_guess, comp_word)
            possible_words[candidate_guess] = score
        possible_words = pd.DataFrame.from_dict(possible_words, orient='index', columns=['score'])
        possible_words.sort_values(by=['score'], ascending=False, inplace=True)
        print(possible_words.head(10).to_markdown())
        correct_letters, partial_letters, wrong_letters = handler.get_input()
        filtered_words = get_possible_words(df, correct_letters, partial_letters, wrong_letters)
    os.system('cls')