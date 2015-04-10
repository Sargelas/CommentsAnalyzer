from comments_analyzer.common.constants import POSITIVE_TONALITY
from comments_analyzer.common.constants import NEUTRAL_TONALITY
from comments_analyzer.common.constants import NEGATIVE_TONALITY

from comments_analyzer.common.constants import HAS_EMOTION

from comments_analyzer.ai.machine_learning import get_features_vector


class Processor:
    def __init__(self, has_emotions_classifier, emotions_classifier, model, text_parser):
        self.has_emotions_classifier = has_emotions_classifier
        self.emotions_classifier = emotions_classifier
        self.model = model
        self.text_parser = text_parser

    def process(self, comment):
        x = get_features_vector(comment, self.text_parser, self.model)
        if self.has_emotions_classifier.predict(x) == HAS_EMOTION:
            # Do emotions processing
            if self.emotions_classifier.predict(x) == POSITIVE_TONALITY:
                return POSITIVE_TONALITY
            else:
                return NEGATIVE_TONALITY
        else:
            return NEUTRAL_TONALITY