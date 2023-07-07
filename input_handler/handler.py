class Handler:
    
    def __init__(
        self, 
        special_characters: str = "!\"#$%&'()*+,./:;<=>?@[\]^_`{|}~"
    ) -> None:
        
        self.special_characters = special_characters
        self.correct_letters = {
            '1': None,
            '2': None,
            '3': None,
            '4': None,
            '5': None
        }
        self.partial_letters = {
            '1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': []
        }
        self.wrong_letters = []
    
    def get_input(self):
        for i in range(1, 6):
            print(f"Input for letter {i}")
            letter, color = self.read_letter()
            if color == 'g':
                if self.correct_letters[str(i)] is not None and self.correct_letters[str(i)] != letter:
                    overwrite = input(f"Green letter already set to {self.correct_letters[str(i)]} at position {i}, do you want to overwrite it? [y/Y]")[0]
                    if overwrite == 'y' or overwrite == 'Y':
                        self.correct_letters[str(i)] = letter
                self.correct_letters[str(i)] = letter
            elif color == 'y':
                self.partial_letters[str(i)].append(letter)
            else:
                self.wrong_letters.append(letter)
            print('\n')
        
        for letter in self.correct_letters.values():
            while letter in self.wrong_letters:
                self.wrong_letters.remove(letter)
        for letter_list in self.partial_letters.values():
            for letter in letter_list:
                while letter in self.wrong_letters:
                    self.wrong_letters.remove(letter)
        
        return self.correct_letters, self.partial_letters, self.wrong_letters

    def read_letter(self):
        letter = input("Enter letter: ")[0]        
        if letter in self.special_characters or letter is None:
            print("Invalid letter")
            return self.read_letter()
        color = input("Enter color [g = Green | y = Yellow | n = Neutral]: ")[0]
        if color not in ['g', 'y', 'n']:
            print("Invalid color")
            return self.read_letter()
        return letter, color