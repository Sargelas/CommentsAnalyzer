class Metric:
    def __init__(self, text_tonality=None, key_words={}):
        self.key_words = key_words                     # map of words and it's tonality
        self.text_tonality = text_tonality             # full text tonality

    def add_key_word(self, key_word, tonality):
        self.key_words[key_word] = tonality

    def set_text_tonality(self, tonality):
        self.text_tonality = tonality

