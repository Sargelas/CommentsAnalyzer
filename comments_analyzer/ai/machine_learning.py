from math import log


def get_features_vector(text, text_parser, model):
    """
    " Get features vector from text
    """
    return get_smile_features(text, text_parser, model) + \
           get_punctuation_features(text, text_parser, model) + \
           get_words_features(text, text_parser, model)


def get_smile_features(text, text_parser, model):
    features = model.get_default_smiles_features()
    for smile, count in text_parser.get_smiles(text).items():
        index = model.get_smile_feature_position(smile)
        features[index] = 1 + log(count)

    return features


def get_punctuation_features(text, text_parser, model):
    features = model.get_default_punctuation_features()
    for symbol, count in text_parser.get_punctuation(text).items():
        index = model.get_punctuation_feature_position(symbol)
        features[index] = 1 + log(count)

    return features


def get_words_features(text, text_parser, model):
    features = model.get_default_words_features()

    weight_summary = 0

    words = text_parser.correct_all_words(text_parser.get_words(text))
    for word in words:
        index = model.get_word_feature_position(word)
        if index is not None:
            weight = model.get_word_feature_weight(word)

            weight_summary += weight
            features[index] += weight

    pairs = text_parser.get_words_pairs(words)
    for pair in pairs:
        index = model.get_word_feature_position(pair)
        if index is not None:
            weight = model.get_word_feature_weight(pair)

            weight_summary += weight
            features[index] += weight

    detected_features_count = len(words) + len(pairs)
    average_weight = [weight_summary / detected_features_count] if detected_features_count != 0 else [0]

    return average_weight + features