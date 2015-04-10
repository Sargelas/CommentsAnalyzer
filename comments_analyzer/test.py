import collections

from comments_analyzer.common.constants import POSITIVE_TONALITY
from comments_analyzer.common.constants import NEUTRAL_TONALITY
from comments_analyzer.common.constants import NEGATIVE_TONALITY


def do_test(comments, answers, processor, print_statistics=False):
    mistakes = collections.defaultdict(lambda: 0)
    mistakes_total = 0

    for comment, answer in zip(comments, answers):
        prediction = processor.process(comment)
        if answer != prediction:
            mistakes_total += 1
            mistakes[(answer, prediction)] += 1

    if print_statistics:
        _print_statistics(len(answers), mistakes_total, mistakes)

    return mistakes_total, mistakes


def _print_statistics(total, mistakes_total, mistakes):
    print("################\n")
    print("#\n")
    print("# Total examples count = %s\n" % total)
    print("#\n")
    print("# Total mistakes count = %s\n" % mistakes_total)
    print("#\n")
    print("# Total mistakes percentage = %s\n" % (mistakes_total / total))
    print("#\n")

    print("# Counts by mistake type:\n")
    for key, value in mistakes.items():
        print("# " + _get_mistake_name(key) + ": " + str(value) + "\n")

    print("#\n")
    print("################\n")


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