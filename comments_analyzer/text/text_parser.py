import re

from comments_analyzer.text.spell_checker import correct


class TextParser:
    def __init__(self, language_model, known_smiles=None, known_punctuation=None):
        self.language_model = language_model
        self.known_smiles = known_smiles
        self.known_punctuation = known_punctuation

        # Required regular expression initialization
        self.clear_reg_exp = re.compile('[^' + self.language_model.get_known_letters() + ']')

    def clear(self, text):
        """
        " Retain only words (punctuation/smiles/ect.
        " will be removed)
        """
        return self.clear_reg_exp.sub(' ', text).lower().strip()

    def get_words(self, text):
        """
        " Get all words from given text
        """
        words = []
        for word in re.split('\s', self.clear(text)):
            if not word:
                continue

            words.append(word)

        return words

    def get_words_pairs(self, words):
        """
        " Get all pairs of words which stands closely
        """
        pairs = []
        for i in range(len(words) - 1):
            pairs.append(words[i] + ' ' + words[i + 1])

        return pairs

    def correct_all_words(self, words):
        """
        " Get list which contains all words in correct form
        """
        corrected_words = []
        for word in words:
            word = correct(word, self.language_model)
            if not ' ' in word:
                corrected_words.append(word)
            else:
                corrected_words += re.split(' ', word)

        return corrected_words

    def get_smiles(self, text):
        """
        " Get all known smiles from given text
        """
        if self.known_smiles is None:
            return {}

        smiles = {}
        for smile in self.known_smiles:
            smile_count = text.count(smile)
            if smile_count > 0:
                smiles[smile] = smile_count

        return smiles

    def get_punctuation(self, text):
        """
        " Get all known punctuation from given text
        """
        if self.known_punctuation is None:
            return {}

        punctuation_symbols = {}
        for symbol in self.known_punctuation:
            symbol_count = text.count(symbol)
            if symbol_count > 0:
                punctuation_symbols[symbol] = symbol_count

        return punctuation_symbols