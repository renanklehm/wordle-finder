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
        self.wrong_letters = {
            '1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': []
        }
        self.allowed_letters = []
    
    def get_input(self):
        word, colors = self.read_word(), self.read_colors()
        for i in range(5):
            if self.correct_letters[str(i+1)] is None:
                if colors[i] == 'g':
                    self.correct_letters[str(i+1)] = word[i]
                    self.allowed_letters.append(word[i])
                elif colors[i] == 'y':
                    for key in self.wrong_letters.keys():
                        while word[i] in self.wrong_letters[key]:
                            self.wrong_letters[key].remove(word[i])
                    self.wrong_letters[str(i+1)].append(word[i])
                    self.allowed_letters.append(word[i])
                else:
                    should_skip = any(word[j] == word[i] and j != i and colors[j] == 'y' for j in range(5))
                    if should_skip:
                        continue
                    for key in self.wrong_letters.keys():
                        if self.correct_letters[key] is None: 
                            self.wrong_letters[key].append(word[i])
        
        for key in self.correct_letters.keys():
            if self.correct_letters[key] is not None:
                self.wrong_letters[key] = []
        
        return self.correct_letters, self.wrong_letters, self.allowed_letters
    
    def read_word(self):
        word = input("Enter word: ")
        if self.special_characters in word or word is None or len(word) != 5:
            print("Invalid word")
            return self.read_word()
        return word

    def read_colors(self):
        colors = input("Enter colors: ")
        if all(letter not in ['g', 'y', 'n'] for letter in colors) or colors is None:
            print("Invalid colors")
            return self.read_colors()
        return colors