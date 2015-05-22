from math import log


class Feature:
    def __init__(self, plain_text, position, weight):
        self.plain_text = plain_text
        self.position = position
        self.weight = weight


class Text:
    def __init__(self, plain_text, words, smiles, punctuation):
        self.plain_text = plain_text
        self.words = words
        self.smiles = smiles
        self.punctuation = punctuation

    def get_vector(self, model):
        return get_features_vector(self.words, self.smiles, self.punctuation, model)


def parse_text(text, text_parser, model):
    words = []
    smiles = []
    symbols = []

    plain_words = text_parser.correct_all_words(text_parser.get_words(text)) # TODO:
    for plain_word in plain_words:
        words.append(Feature(plain_word,
                             model.get_word_feature_position(plain_word),
                             model.get_word_feature_weight(plain_word)))

    for plain_smile, count in text_parser.get_smiles(text).items():
        smiles.append(Feature(plain_smile, model.get_smile_feature_position(plain_smile), 1 + log(count)))

    for plain_symbol, count in text_parser.get_punctuation(text).items():
        symbols.append(Feature(plain_symbol, model.get_punctuation_feature_position(plain_symbol), 1 + log(count)))

    return Text(text, words, smiles, symbols)


def get_features_vector(words, smiles, punctuation, model):
    return get_vector_for_one_feature(smiles, model.get_default_smiles_features()) \
           + get_vector_for_one_feature(punctuation, model.get_default_punctuation_features()) \
           + get_vector_for_one_feature(words, model.get_default_words_features(), True)


def get_vector_for_one_feature(features, default_vector, add_average=False):
    if len(features) == 0:
        return [0] + default_vector if add_average else default_vector

    total = 0
    for feature in features:
        if feature.position is None or feature.weight is None:
            continue

        total += feature.weight
        default_vector[feature.position] += feature.weight

    return [total / len(features)] + default_vector if add_average else default_vector