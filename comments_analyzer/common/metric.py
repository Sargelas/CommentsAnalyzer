class Metric:
    def __init__(self):
        self.key_words = {}             # map of words and it's tonality
        self.text_tonality = None       # full text tonality
        self.sentence_tonality = {}     # map of sentence and it's tonality

    def add_key_word(self, key_word, tonality):
        self.key_words[key_word] = tonality

    def set_text_tonality(self, tonality):
        self.text_tonality = tonality

    def add_sentence_tonality(self, sentence, tonality):
        self.sentence_tonality[sentence] = tonality