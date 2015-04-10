__author__ = 'Zaycev Denis'

import collections

from sklearn.ensemble import RandomForestClassifier

from comments_analyzer.common.constants import POSITIVE_TONALITY
from comments_analyzer.common.constants import NEUTRAL_TONALITY
from comments_analyzer.common.constants import NEGATIVE_TONALITY
from comments_analyzer.common.constants import HAS_EMOTION
from comments_analyzer.common.constants import NEUTRAL
from comments_analyzer.sentiment_estimation import calculate_weights
from comments_analyzer.ai.machine_learning import get_features_vector
from comments_analyzer.ai.model import Model


class Teacher:
    def __init__(self, comments, answers, model, text_parser):
        self.comments = comments
        self.answers = answers
        self.model = model
        self.text_parser = text_parser

        # To be prepared while training
        self.classifier = None

    def teach(self, count_of_features):
        self.classifier = RandomForestClassifier()
        self.classifier.fit(self._get_training_set(), self.answers)

    def get_classifier(self):
        return self.classifier

    def get_model(self):
        return self.model

    def _get_training_set(self):
        x = []
        for comment in self.comments:
            x.append(get_features_vector(comment, self.text_parser, self.model))

        return x


def do_training(comments, answers, text_parser, features_count):
    model = _prepare_model(calculate_weights(comments, answers, text_parser), features_count)

    n_e_comments, n_e_answers = _get_neutral_emotional_data(comments, answers)
    p_n_comments, p_n_answers = _get_positive_negative_data(comments, answers)

    n_e_teacher = Teacher(n_e_comments, n_e_answers, model, text_parser)
    n_e_teacher.teach(features_count)

    p_n_teacher = Teacher(p_n_comments, p_n_answers, model, text_parser)
    p_n_teacher.teach(features_count)

    return n_e_teacher.classifier, p_n_teacher.classifier, model


def _get_neutral_emotional_data(comments, answers):
    n_e_comments = []
    n_e_answers = []

    for comment, answer in zip(comments, answers):
        if answer == NEUTRAL_TONALITY:
            n_e_comments.append(comment)
            n_e_answers.append(NEUTRAL)
        else:
            n_e_comments.append(comment)
            n_e_answers.append(HAS_EMOTION)

    return n_e_comments, n_e_answers


def _get_positive_negative_data(comments, answers):
    p_n_comments = []
    p_n_answers = []

    for comment, answer in zip(comments, answers):
        if answer == POSITIVE_TONALITY:
            p_n_comments.append(comment)
            p_n_answers.append(POSITIVE_TONALITY)
        else:
            p_n_comments.append(comment)
            p_n_answers.append(NEGATIVE_TONALITY)

    return p_n_comments, p_n_answers


def _prepare_model(weights, count_of_features):
    words_positions = collections.defaultdict(lambda: None)
    words_weights = collections.defaultdict(lambda: None)

    # Needs to retain only maximum weights
    weights = sorted(weights.items(), key=lambda x: (abs(x[1]), x[0]), reverse=True)

    counter = 0
    for data_chunk in weights:
        if counter >= count_of_features:
            break

        words_positions[data_chunk[0]] = counter
        words_weights[data_chunk[0]] = data_chunk[1]
        counter += 1

    # hard coded by now
    smiles_positions = {":)" : 0, ":(" : 1, ":'(" : 2}
    punctuation_positions = {"?!" : 0}

    return Model(words_positions, words_weights, smiles_positions, punctuation_positions)