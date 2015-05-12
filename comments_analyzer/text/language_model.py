import enchant


class LanguageModel:
    def __init__(self, label, known_letters, dictionary):
        self.label = label
        self.known_letters = known_letters
        self.dictionary = dictionary

    def get_label(self):
        return self.label

    def get_known_letters(self):
        return self.known_letters

    def get_dictionary(self):
        return self.dictionary

# Predefined language models goes below
RUSSIAN = LanguageModel('Russian',
                        'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
                        enchant.Dict('ru_Ru'))

ENGLISH = LanguageModel('English',
                        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
                        enchant.Dict('en_En'))