import collections
import pickle

from comments_analyzer.ai.model import Model

SEPARATOR = '\t'

WORD = 'word'
SMILE = 'smile'
PUNCTUATION = 'punctuation'


def load_model(file_name):
    file = open(file_name, mode='r', encoding='utf-8')

    words_positions = collections.defaultdict(lambda: None)
    words_weights = collections.defaultdict(lambda: None)

    smiles_positions = collections.defaultdict(lambda: None)

    punctuation_positions = collections.defaultdict(lambda: None)

    for line in file.readlines():
        chucks = line.split(SEPARATOR)
        if chucks[0] == WORD:
            words_weights[chucks[1]] = float(chucks[3])
            words_positions[chucks[1]] = int(chucks[2])

        elif chucks[0] == SMILE:
            smiles_positions[chucks[1]] = int(chucks[2])

        elif chucks[0] == PUNCTUATION:
            punctuation_positions[chucks[1]] = int(chucks[2])

    file.close()

    return Model(words_positions, words_weights, smiles_positions, punctuation_positions)


def dump_model(model, file_name):
    file = open(file_name, mode='w', encoding='utf-8')
    for word, weight in model.words_feature_weights.items():
        position = model.get_word_feature_position(word)
        file.write(WORD + SEPARATOR + word + SEPARATOR + str(position) + SEPARATOR + str(weight) + '\n')

    for smile, position in model.smile_feature_position.items():
        file.write(SMILE + SEPARATOR + smile + SEPARATOR + str(position) + SEPARATOR + '1' + '\n')

    for punctuation, position in model.punctuation_feature_position.items():
        file.write(PUNCTUATION + SEPARATOR + punctuation + SEPARATOR + str(position) + SEPARATOR + '1' + '\n')

    file.close()


def load_classifier(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


def dump_classifier(classifier, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(classifier, f)