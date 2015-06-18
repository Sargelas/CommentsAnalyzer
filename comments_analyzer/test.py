import collections

from comments_analyzer.common.constants import POSITIVE_TONALITY
from comments_analyzer.common.constants import NEUTRAL_TONALITY
from comments_analyzer.common.constants import NEGATIVE_TONALITY


def do_test(comments, answers, processor, print_statistics=False):
    confusion_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]] # collections.defaultdict(lambda: 0)
    mistakes_total = 0

    for comment, answer in zip(comments, answers):
        metric = processor.process(comment)
        if answer != metric.text_tonality:
            mistakes_total += 1
        confusion_matrix[metric.text_tonality + 1][answer + 1] += 1

    if print_statistics:
        _print_statistics(len(answers), mistakes_total, confusion_matrix)

    return mistakes_total, confusion_matrix


def _print_statistics(total, mistakes_total, cm):
    print("################")
    print("#")
    print("# Total examples count = %s" % total)
    print("#")
    print("# Total mistakes count = %s" % mistakes_total)
    print("#")
    print("# Total mistakes percentage = %s" % (mistakes_total / total))
    print("#")

    print("# Confusion matrix:")
    for i in range(3):
        print("# " + str(cm[i][0]) + "\t" + str(cm[i][1]) + "\t" + str(cm[i][2]))

    precision_negative = 0 if cm[0][0] == 0 else cm[0][0] / (cm[0][0] + cm[0][1] + cm[0][2])
    precision_neutral  = 0 if cm[1][1] == 0 else cm[1][1] / (cm[1][0] + cm[1][1] + cm[1][2])
    precision_positive = 0 if cm[2][2] == 0 else cm[2][2] / (cm[2][0] + cm[2][1] + cm[2][2])

    recall_negative = 0 if cm[0][0] == 0 else cm[0][0] / (cm[0][0] + cm[1][0] + cm[2][0])
    recall_neutral  = 0 if cm[1][1] == 0 else cm[1][1] / (cm[0][1] + cm[1][1] + cm[2][1])
    recall_positive = 0 if cm[2][2] == 0 else cm[2][2] / (cm[0][2] + cm[1][2] + cm[2][2])

    f_negative = 0 if cm[0][0] == 0 else 2 * (precision_negative * recall_negative / (precision_negative + recall_negative))
    f_neutral  = 0 if cm[1][1] == 0 else 2 * (precision_neutral * recall_neutral / (precision_neutral + recall_neutral))
    f_positive = 0 if cm[2][2] == 0 else 2 * (precision_positive * recall_positive / (precision_positive + recall_positive))

    f_measure = (f_negative + f_neutral + f_positive) / 3

    precision_avg = (precision_positive + precision_neutral + precision_negative) / 3
    recall_avg = (recall_positive + recall_neutral + recall_negative) / 3

    print("#")
    print("# Precision: " + str(precision_avg))
    print("# Recall: " + str(recall_avg))

    print("#")
    print("# F measure: " + str(f_measure))

    print("#")
    print("################")


def _get_mistake_name(expected_to_current):
    return _get_tonality_name(expected_to_current[0]) + " recognized as " + _get_tonality_name(expected_to_current[1])


def _get_tonality_name(tonality):
    if tonality == POSITIVE_TONALITY:
        return "positive"
    elif tonality == NEUTRAL_TONALITY:
        return "neutral"
    elif tonality == NEGATIVE_TONALITY:
        return "negative"

    raise Exception("Unknown tonality!")