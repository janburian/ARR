import math
from pathlib import Path
import copy


def load_vocab_file(filename: Path):
    list_final_phonemes = []
    list_words = []

    with open(filename, 'r', encoding='cp1250') as file:
        for line in file:
            line_final = (line.rstrip("\n")).split()
            word = line_final[0]
            transcript = line_final[1:]

            list_transcript = list(transcript)
            list_final_phonemes.append(list_transcript)

            list_words.append(word)
    file.close()
    list_final_phonemes.append(["#"])
    list_words.append("#")  # silence not in vocab

    return [list_final_phonemes, list_words]


def load_leaves(filename: Path):
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
            probabilities_list_str = line_final[1:]
            probabilities_list_float = [-math.log10(float(i)) for i in probabilities_list_str]

            dictionary[char] = probabilities_list_float
    file.close()

    return dictionary


def load_language_model(filename: Path):
    with open(filename, 'r', encoding='cp1250') as file:
        language_model_list = file.read().splitlines()

        sections = {}
        current_list = []

        for line in language_model_list:
            if line == "":
                continue
            if line[0] == '\\':
                current_list = []
                sections[line] = current_list
            else:
                current_list.append(line)

    return sections


def get_language_model_dictionaries(sections: dict):
    ngrams_dictionaries = {}  # dictionary of dictionaries
    n = 1
    for section in sections:
        current_dict = {}
        if section == "\\" + str(n) + "-grams: ":
            ngrams_list = sections[section]

            for ngram in ngrams_list:
                ngram_split = ngram.split()
                prob = float(ngram_split[0])
                key = " ".join(ngram_split[1:(n + 1)])
                current_dict[key] = prob

            section = section.replace(" ", "")  # deleting whitespace in section
            ngrams_dictionaries[section] = current_dict
            n += 1

    return ngrams_dictionaries


def load_observations(filename: Path):
    list_final = []
    with open(filename, 'r', encoding='cp1250') as file:
        for line in file:
            line_final = (line.rstrip("\n")).split()
            line_final_str_list = list(line_final)
            line_final_float_list = [-math.log10(float(i)) for i in line_final_str_list]
            list_final.append(line_final_float_list)
        file.close()

    return list_final


def get_minimal_price(phi_net, phonemes_net, words_list, unigrams, leaves_dict, LGAMMA, BETA):
    ends = []
    for i in range(len(phonemes_net)):
        phi = phi_net[i][-1]
        phoneme = phonemes_net[i][-1]
        word = words_list[i]
        prob_language_model = unigrams.get(word, 0)
        penalty = LGAMMA - BETA * prob_language_model
        prob = leaves_dict[phoneme][1]
        ends.append(phi + prob + penalty)

    final_min_price = min(ends)

    return [final_min_price, ends]


def get_spoken_words(final_min_price, ends: list, tokens: list, words_list: list):
    final_min_index = ends.index(final_min_price)
    final_min_token = token_net[final_min_index][-1]

    previous_token_index = final_min_token
    spoken_words = [words_list[final_min_index]]
    while (previous_token_index != 0):
        spoken_words.append(tokens[previous_token_index][0])
        previous_token_index = tokens[previous_token_index][1]
    spoken_words.reverse()

    return spoken_words


def viterbi(obs: list, leaves: dict, phonemes_net: list, words_list: list, unigrams: dict, LGAMMA, BETA):
    phi_net = copy.deepcopy(phonemes_net)
    token_net = copy.deepcopy(phonemes_net)
    # obs: radky = casy, sloupce = fonemy

    # Inicializace (t == 0)
    t = 0
    counter = 0
    for phoneme_list in phi_net:  # word = mnozina stavu  # stav = jeden char ve slove
        first_char = phoneme_list[t]
        idx = list(leaves.keys()).index(first_char)
        obs_t1 = obs[t]  # beru pouze prvni radek
        first_value = obs_t1[idx]
        phi_net[counter][0] = first_value
        token_net[counter][0] = 0

        if len(phoneme_list) > 1:
            for i in range(1, len(phoneme_list)):
                phi_net[counter][i] = math.inf
                token_net[counter][i] = 0

        counter += 1

    # Iterativni vypocet (t >= 1)
    tokens = []
    T = len(obs)
    for t in range(1, T):
        ends = []
        for i in range(len(phonemes_net)):
            phi = phi_net[i][-1]  # price of word's end
            end_phoneme = phonemes_net[i][-1]
            key = words_list[i]
            prob_language_model = unigrams.get(key, 0)
            trans_prob = leaves_dict[end_phoneme][1]

            penalty = LGAMMA - BETA * prob_language_model
            ends.append(phi + trans_prob + penalty)

        min_price_value = min(ends)
        min_price_index = ends.index(min_price_value)
        tokens.append((words_list[min_price_index], token_net[min_price_index][-1]))
        min_price_token = len(tokens) - 1

        for w in range(len(phi_net)):
            last_phi = phi_net[w].copy()
            last_token = token_net[w].copy()

            word = phonemes_net[w]
            first_char = word[0]
            prob = leaves_dict[first_char][0]
            price = min(min_price_value, last_phi[0] + prob)

            if price == min_price_value:
                token = min_price_token
            else:
                token = last_token[0]

            idx = list(leaves.keys()).index(first_char)

            phi_net[w][0] = price + obs[t][idx]
            token_net[w][0] = token
            for j in range(1, len(word)):
                prev_char = word[j-1]
                current_char = word[j]

                prev_phi = last_phi[j-1] + leaves_dict[prev_char][1]
                current_phi = last_phi[j] + leaves_dict[prev_char][0]
                prev_token = last_token[j-1]
                current_token = last_token[j]

                price = min(prev_phi, current_phi)

                if price == prev_phi:
                    token = prev_token
                else:
                    token = current_token

                current_char_idx = list(leaves.keys()).index(current_char)
                phi_net[w][j] = price + obs[t][current_char_idx]
                token_net[w][j] = token

    return [phi_net, token_net, tokens]


if __name__ == "__main__":
    # Paths to files
    path_vocab_file = Path(r'.\vocab')
    path_leaves_file = Path(r'.\leaves.txt')
    path_obs_file = Path(r'.\00170005_14.txt')
    path_language_model_file = Path(r'.\language_model_arpa')

    # Reading files
    [phonemes_net, words_list] = load_vocab_file(path_vocab_file)
    obs = load_observations(path_obs_file)
    leaves_dict = load_leaves(path_leaves_file)

    # Formatting language model
    language_model_sections = load_language_model(path_language_model_file)
    language_model_dictionary = get_language_model_dictionaries(language_model_sections)

    # Extracting unigrams
    unigrams = language_model_dictionary["\\1-grams:"]

    # Initializing parameters
    LGAMMA = -math.log10(0.01)
    BETA = 5

    # Viterbi algorithm
    [phi_net, token_net, tokens] = viterbi(obs, leaves_dict, phonemes_net, words_list, unigrams, LGAMMA, BETA)
    [final_min_price, ends] = get_minimal_price(phi_net, phonemes_net, words_list, unigrams, leaves_dict, LGAMMA, BETA)
    spoken_words = get_spoken_words(final_min_price, ends, tokens, words_list)

    # Printing result
    print(f"Minimal price: {final_min_price}")
    print(f"Spoken words: {spoken_words}")
