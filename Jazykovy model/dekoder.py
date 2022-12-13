import math


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

def load_probabilities(filename: str):
    list_final = []
    with open(filename, 'r', encoding='cp1250') as file:
        for line in file:
            line_final = (line.rstrip("\n")).split()

            line_final_list = list(line_final)
            list_final.append(line_final_list)
        file.close()

    return list_final

def viterbi(probs: list, leaves: dict, mesh: dict):
    prices_init = []

    # Inicializace (radky = casy, sloupce = fonemy)
    N = len(leaves.keys())
    T = len(probs)

    values = []

    for word in mesh:
        values = []
        for j in range(0, N):
            first_char = word[0]
            idx = list(leaves.keys()).index(first_char)
            if j == 0:
                list_stavu = probs[j] # prvni radka
                first_value = float(list_stavu[idx])
                log = -math.log10(first_value)
                values.append(log)
            else:
                values.append(math.inf)

        prices_init.append(values)

    print()
    prices_init = []


    # Iterativni vypocet
    '''
    min = 50

    for list in prices_init:
        tmp = min(list)
        if tmp < min:
            min = tmp
        continue
    '''


    for t in range(1, T):
        word = mesh[t]
        N = len(word)

        for j in range(0, N):
            first_char = word[j]
            char_idx = list(leaves.keys()).index(first_char)
            prices = prices_init[j]







if __name__ == "__main__":
    vocab_filename = "vocab"
    leaves_filename = "leaves.txt"
    probs_filename = "00170005_14.txt"

    mesh = load_vocab_file(vocab_filename)
    probs = load_probabilities(probs_filename)
    leaves_dict = load_leaves(leaves_filename)
    viterbi(probs, leaves_dict, mesh)
    print()


