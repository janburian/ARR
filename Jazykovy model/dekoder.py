def load_vocab_file(filename: str):
    '''
    Loads vocab file
    :param filename:
    :return: list of lists, e.g. [['a'], ['a, b, i']]
    '''
    list_final = []
    with open(filename, 'r', encoding='cp1250') as file:
        for line in file:
            line_final = (line.rstrip("\n")).split()
            transcript = line_final[1:]

            list_transcript = list(transcript)
            list_final.append(list_transcript)
    file.close()

    return list_final

def load_leaves(filename: str):
    '''
    Loads from leaves file (e. g. a prob prob; b prob prob)
    :param filename:
    :return:
    '''
    dictionary = {}
    with open(filename, 'r', encoding='cp1250') as file:
        for line in file:
            line_final = (line.rstrip("\n")).split()

            char = line_final[0]
            probabilities = line_final[1:]

            dictionary[char] = probabilities
    file.close()

    return dictionary


if __name__ == "__main__":
    vocab_filename = "vocab"
    leaves_filename = "leaves.txt"

    mesh = load_vocab_file(vocab_filename)
    leaves_dict = load_leaves(leaves_filename)
    print()


