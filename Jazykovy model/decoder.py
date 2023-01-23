# Modules import
import math
from pathlib import Path
import copy

# Methods
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


def viterbi(observations: list, leaves: dict, phonemes_net: list, words_list: list, unigrams: dict, L_gamma: float, beta: int):
    phi_net = copy.deepcopy(phonemes_net)
    token_net = copy.deepcopy(phonemes_net)
    # observations: lines = times; columns = phonemes

    # Initialization (t = 0)
    for i in range(len(phi_net)):  # word = mnozina stavu  # stav = jeden char ve slove
        viterbi_initialize(phi_net, token_net, i, leaves, observations)

    # Recursion (t >= 1)
    tokens_list = []
    for t in range(1, len(observations)):
        prices_end_phonemes_penalties = calculate_prices_end_penalties(beta, L_gamma, phi_net, phonemes_net, unigrams,
                                                                       words_list)

        min_price_end_phoneme_value = min(prices_end_phonemes_penalties)
        min_price_end_phoneme_index = prices_end_phonemes_penalties.index(min_price_end_phoneme_value)

        token_tuple = (words_list[min_price_end_phoneme_index], token_net[min_price_end_phoneme_index][-1])  # eg. ('a', 3)
        tokens_list.append(token_tuple)
        min_price_token = len(tokens_list) - 1

        viterbi_iterative(leaves, min_price_end_phoneme_value, min_price_token, observations, phi_net, phonemes_net, t,
                          token_net)

    return [phi_net, token_net, tokens_list]


def viterbi_initialize(phi_net, token_net, index, leaves, observations):
    phoneme_list = phi_net[index]
    first_phoneme = phoneme_list[0]
    idx = list(leaves.keys()).index(first_phoneme)
    obs_t1 = observations[0]  # beru pouze prvni radek
    first_value = obs_t1[idx]
    phi_net[index][0] = first_value
    token_net[index][0] = 0
    if len(phoneme_list) > 1:
        for i in range(1, len(phoneme_list)):
            phi_net[index][i] = math.inf
            token_net[index][i] = 0


def calculate_prices_end_penalties(beta, L_gamma, phi_net, phonemes_net, unigrams, words_list):
    prices_ends_phonemes_penalties = []
    for i in range(len(phonemes_net)):
        phi = phi_net[i][-1]  # price of word's end
        end_phoneme = phonemes_net[i][-1]
        word = words_list[i] # key to dictionary
        prob_language_model = unigrams.get(word, 0)
        trans_prob = leaves_dict[end_phoneme][1]

        penalty = - beta * prob_language_model + L_gamma
        prices_ends_phonemes_penalties.append(phi + trans_prob + penalty)  # -log p(O|W) - beta * log p(W) - L_gamma

    return prices_ends_phonemes_penalties

def viterbi_iterative(leaves, min_price_end_value, min_price_token, observations, phi_net, phonemes_net, t, token_net):
    for w in range(len(phi_net)):
        last_phi = phi_net[w].copy()
        last_token = token_net[w].copy()

        phonemes_list = phonemes_net[w]  # transcript of word in form of list of Strings

        viterbi_iterative_first_phoneme(last_phi, last_token, leaves, min_price_end_value, min_price_token,
                                        observations, phi_net, phonemes_list, t, token_net, w)

        for j in range(1, len(phonemes_list)):
            viterbi_iterative_next_phonemes(j, last_phi, last_token, leaves, observations, phi_net, phonemes_list, t,
                                            token_net, w)


def viterbi_iterative_first_phoneme(last_phi, last_token, leaves, min_price_end_value, min_price_token, observations,
                                    phi_net, phonemes_list, t, token_net, w):
    first_phoneme = phonemes_list[0]
    prob = leaves_dict[first_phoneme][0]
    price = min(min_price_end_value, last_phi[0] + prob)
    if price == min_price_end_value:
        token = min_price_token
    else:
        token = last_token[0]
    first_phoneme_idx = list(leaves.keys()).index(first_phoneme)
    phi_net[w][0] = price + observations[t][first_phoneme_idx]
    token_net[w][0] = token


def viterbi_iterative_next_phonemes(j, last_phi, last_token, leaves, observations, phi_net, phonemes_list, t, token_net,
                                    w):
    previous_phoneme = phonemes_list[j - 1]
    current_phoneme = phonemes_list[j]
    previous_phi = last_phi[j - 1] + leaves_dict[previous_phoneme][1]
    current_phi = last_phi[j] + leaves_dict[previous_phoneme][0]
    previous_token = last_token[j - 1]
    current_token = last_token[j]
    price = min(previous_phi, current_phi)
    if price == previous_phi:
        token = previous_token
    else:
        token = current_token
    current_phoneme_idx = list(leaves.keys()).index(current_phoneme)
    phi_net[w][j] = price + observations[t][current_phoneme_idx]
    token_net[w][j] = token


def get_minimal_price(phi_net, phonemes_net, words_list, unigrams, L_gamma, beta, leaves_dict):
    prices_ends_phonemes_penalties = []
    for i in range(len(phonemes_net)):
        phi = phi_net[i][-1]
        phoneme = phonemes_net[i][-1]
        word = words_list[i]
        prob_language_model = unigrams.get(word, 0)
        penalty = L_gamma - beta * prob_language_model
        prob = leaves_dict[phoneme][1]
        prices_ends_phonemes_penalties.append(phi + prob + penalty)

    final_min_price = min(prices_ends_phonemes_penalties)

    return [final_min_price, prices_ends_phonemes_penalties]


def get_spoken_words(final_min_price, prices_ends_phonemes_penalties: list, tokens: list, words_list: list):
    final_min_index = prices_ends_phonemes_penalties.index(final_min_price)
    final_min_token = token_net[final_min_index][-1]

    previous_token_index = final_min_token
    spoken_words = [words_list[final_min_index]]
    while (previous_token_index != 0):
        spoken_words.append(tokens[previous_token_index][0])
        previous_token_index = tokens[previous_token_index][1]
    spoken_words.reverse()

    return spoken_words


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
    L_gamma = -math.log10(0.05)
    beta = 5

    # Viterbi algorithm
    [phi_net, token_net, tokens] = viterbi(obs, leaves_dict, phonemes_net, words_list, unigrams, L_gamma, beta)
    [final_min_price, prices_ends_phonemes_penalties] = get_minimal_price(phi_net, phonemes_net, words_list, unigrams, L_gamma, beta, leaves_dict)
    spoken_words = get_spoken_words(final_min_price, prices_ends_phonemes_penalties, tokens, words_list)

    # Printing result
    print(f"Minimal price: {final_min_price}")
    print(f"Spoken words: {spoken_words}")
