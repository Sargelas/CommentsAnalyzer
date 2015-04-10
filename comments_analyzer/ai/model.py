class Model:
    def __init__(self, words_feature_position, words_feature_weights,
                       smile_feature_position, punctuation_feature_position):
        self.words_feature_position = words_feature_position
        self.words_feature_weights = words_feature_weights
        self.smile_feature_position = smile_feature_position
        self.punctuation_feature_position = punctuation_feature_position

    def get_word_feature_position(self, word):
        if word not in self.words_feature_position:
            return None

        return self.words_feature_position[word]

    def get_word_feature_weight(self, word):
        if word not in self.words_feature_weights:
            return None

        return self.words_feature_weights[word]

    def get_smile_feature_position(self, smile):
        if smile not in self.smile_feature_position:
            return None

        return self.smile_feature_position[smile]

    def get_punctuation_feature_position(self, symbol):
        if symbol not in self.punctuation_feature_position:
            return None

        return self.punctuation_feature_position[symbol]

    def get_default_words_features(self):
        """
        " Get dict where all features are 0
        """
        return [0 for i in range(len(self.words_feature_position))]

    def get_default_smiles_features(self):
        """
        " Get dict where all features are 0
        """
        return [0 for i in range(len(self.smile_feature_position))]

    def get_default_punctuation_features(self):
        """
        " Get dict where all features are 0
        """
        return [0 for i in range(len(self.punctuation_feature_position))]