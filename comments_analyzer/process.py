from comments_analyzer.common.constants import POSITIVE_TONALITY
from comments_analyzer.common.constants import NEUTRAL_TONALITY
from comments_analyzer.common.constants import NEGATIVE_TONALITY
from comments_analyzer.common.constants import HAS_EMOTION

from comments_analyzer.common.metric import Metric

from comments_analyzer.ai.machine_learning import parse_text


class Processor:
    def __init__(self, has_emotions_classifier, emotions_classifier, model, text_parser):
        self.has_emotions_classifier = has_emotions_classifier
        self.emotions_classifier = emotions_classifier
        self.model = model
        self.text_parser = text_parser

    def process(self, comment):
        text = parse_text(comment, self.text_parser, self.model)

        x = text.get_vector(self.model)
        if not _has_detected_features(x):
            return Metric(NEUTRAL_TONALITY)

        if self.has_emotions_classifier.predict(x) == HAS_EMOTION:
            # Do emotions processing
            if self.emotions_classifier.predict(x) == POSITIVE_TONALITY:
                tonality = POSITIVE_TONALITY
            else:
                tonality = NEGATIVE_TONALITY
        else:
            tonality = NEUTRAL_TONALITY

        key_words = {}
        for word in text.words:
            if not word.weight:
                continue

            key_words[word.plain_text] = word.weight

        if len(key_words) == 0:
            # just for double check
            return Metric(tonality)

        average_weight = 0
        for word, weight in key_words.items():
            average_weight += abs(weight)

        average_weight /= len(key_words)

        reduced_key_words = {}
        for word, weight in key_words.items():
            if abs(weight) >= average_weight:
                reduced_key_words[word] = weight

        return Metric(tonality, reduced_key_words)


def _has_detected_features(x):
    for value in x:
        if value != 0:
            return True

    return False

