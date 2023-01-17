import math
from pathlib import Path

def load_vocab_file(filename:Path):
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

def load_leaves(filename:Path):
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

def load_observations(filename:Path):
    list_final = []
    with open(filename, 'r', encoding='cp1250') as file:
        for line in file:
            line_final = (line.rstrip("\n")).split()

            line_final_list = list(line_final)
            list_final.append(line_final_list)
        file.close()

    return list_final

def viterbi(obs: list, leaves: dict, mesh: dict):
    prices_init = []

    # obs: radky = casy, sloupce = fonemy
    N = len(leaves.keys())
    T = len(obs)

    # Inicializace (t == 0)
    for word in mesh: # word = mnozina stavu
        values = []
        for char in word:
            idx = list(leaves.keys()).index(char)
            list_stavu = obs[0] # beru pouze prvni radek
            first_value = float(list_stavu[idx])
            log = -math.log10(first_value)
            values.append(log)
        prices_init.append(values)

    print()

    # Iterativni vypocet (t >= 1)
    min = get_min(prices_init)

    prices_it = []

    '''
    for word in mesh:
        for t in range(1, T):
            word = mesh[t]
            length_word = len(word)
            for char in word:
                first_char = word[j]
                char_idx = list(leaves.keys()).index(first_char)
                prices = prices_init[j]
                transitions = leaves[first_char]

                if j == 0:
                    value_1 = min
                    value_2 = prices[t-1] - math.log10(transitions[j])

                else:
                    prices_1 = prices[j-1]
                    price_2 = prices[j]

                    value_1 = prices_1[t-1] - math.log10(transitions[j-1])
                    value_2 = price_2[t] - math.log10(transitions[j])

                    res = min(value_1, value_2)
    '''



def get_min(prices_init):
    res = []
    for list in prices_init:
       last_element = list[-1]
       res.append(last_element)

    return min(res)


if __name__ == "__main__":
    # Paths to files
    path_vocab_file = Path('vocab')
    path_leaves_file = Path('leaves.txt')
    path_obs_file = Path('00170005_14.txt')
    path_language_model_file = Path('') # TODO

    # Loading files
    mesh = load_vocab_file(path_vocab_file)
    obs = load_observations(path_obs_file)
    leaves_dict = load_leaves(path_leaves_file)

    # Viterbi algorithm
    viterbi(obs, leaves_dict, mesh)
    print()


