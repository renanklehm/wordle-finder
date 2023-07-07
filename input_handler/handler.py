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
        self.get_correct_letters()
        if None not in self.correct_letters.values():
            return self.correct_letters, self.partial_letters, self.wrong_letters
        self.get_partial_letters()
        self.get_wrong_letters()
        
        _correct_letters = self.correct_letters
        _partial_letters = self.partial_letters
        _wrong_letters = self.wrong_letters
        
        return _correct_letters, _partial_letters, _wrong_letters
    
    def get_correct_letters(self):
        try:
            _input = str(input('Correct Letters (unknowns should be "-"): '))
            if len(_input) != 5:
                raise ValueError('Incorrect number of letters')
            if any(c in self.special_characters for c in _input):
                raise ValueError('Invalid character')
        except ValueError as e:
            print(e)
            return self.get_correct_letters()
        
        for idx, letter in enumerate(_input):
            if letter != '-':
                self.correct_letters[str(idx+1)] = letter
            else:
                self.correct_letters[str(idx+1)] = None

    def get_partial_letters(self):
        for i in range(5):
            try:
                if i == 0: _input = str(input(f'Partial letter for {i+1}st spot: '))
                elif i == 1: _input = str(input(f'Partial letter for {i+1}nd spot: '))
                elif i == 2: _input = str(input(f'Partial letter for {i+1}rd spot: '))
                else: _input = str(input(f'Partial letter for {i+1}th spot: '))
                
                if _input == '':
                    continue
                if len(_input) != 1:
                    raise ValueError('Only one letter per guess allowed')
                if any(c in self.special_characters for c in self.partial_letters):
                    raise ValueError('Invalid character')
            except ValueError as e:
                print(e)
                return self.get_partial_letters()
            self.partial_letters[f'{i+1}'].append(_input)


    def get_wrong_letters(self):
        try:
            _input = str(input('Wrong letters: '))
            if len(_input) > 5:
                raise ValueError('Incorrect number of letters')
            if any(c in self.special_characters for c in _input):
                raise ValueError('Invalid character')
        except ValueError as e:
            print(e)
            return self.get_wrong_letters()
        for letter in _input:
            self.wrong_letters.append(letter)
        for letter in self.correct_letters.values():
            while letter in self.wrong_letters:
                self.wrong_letters.remove(letter)
        for letter_list in self.partial_letters.values():
            for letter in letter_list:
                while letter in self.wrong_letters:
                    self.wrong_letters.remove(letter)