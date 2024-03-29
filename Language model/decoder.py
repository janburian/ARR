# Modules import
import math
from pathlib import Path
import copy


# Methods
def load_vocab_file(filename: Path):
    """
    Reads vocabulary file
    :param filename:
    :return: [list of lists of phonemes, list of words] eg. [[['a'], ['a', 'b', 'i'], ...], ['a', 'aby']]
    """
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
    """
    Reads observations
    :param filename:
    :return: list of lists
    """
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
    """
    Reads leaves file (e. g. a prob prob; b prob prob)
    :param filename:
    :return: dictionary_phonemes {'a' = [prob, prob], 'b' = [prob, prob], ...}
    """
    dictionary_phonemes = {}
    list_probs = []
    index = 0
    with open(filename, 'r', encoding='cp1250') as file:
        for line in file:
            line_final = (line.rstrip("\n")).split()

            phoneme = line_final[0]
            probabilities_list_str = line_final[1:]
            probabilities_tuple_float = tuple(-math.log10(float(i)) for i in probabilities_list_str)

            dictionary_phonemes[phoneme] = index  # dictionary: key - phonem; value - index of phoneme's probabilities in probs_list
            list_probs.append(probabilities_tuple_float) # list of tuples [(prob, prob), (prob, prob), ...]
            index += 1
    file.close()

    return [dictionary_phonemes, list_probs]


def load_language_model(filename: Path):
    """
    Reads language model
    :param filename:
    :return: dictionary
    """
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


def create_language_model_dictionaries(sections: dict):
    """
    Creates certain n-gram dictionaries
    :param sections:
    :return: dictionary of n-gram dictionaries
    """
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


def viterbi(observations: list, phonemes_dict: dict, probs_list, phonemes_net: list, words_list: list, unigrams: dict,
            L_gamma: float, beta: int):
    phi_net = copy.deepcopy(phonemes_net)
    token_net = copy.deepcopy(phonemes_net)

    # Initialize (t = 1)
    for i in range(len(phi_net)):  # state = 1 phonem in word
        viterbi_initialize(phi_net, token_net, i, phonemes_dict, observations)

    # Iterative (t > 1)
    tokens_tuples_list = []
    for t in range(1, len(observations)):
        prices_end_phonemes = calculate_end_states_prices(phonemes_net, phi_net, words_list, unigrams, phonemes_dict,
                                                          probs_list, beta, L_gamma)

        min_price_end_phoneme_value = min(prices_end_phonemes)
        min_price_end_phoneme_index = prices_end_phonemes.index(min_price_end_phoneme_value)

        token_word = words_list[min_price_end_phoneme_index]
        token_pointer = token_net[min_price_end_phoneme_index][-1]

        token_tuple = (token_word, token_pointer)  # eg. ('word', 3)
        tokens_tuples_list.append(token_tuple)
        min_price_token = len(tokens_tuples_list) - 1

        viterbi_iterative(phonemes_dict, probs_list, min_price_end_phoneme_value, min_price_token, observations, phi_net,
                          phonemes_net, t, token_net)

    return [phi_net, token_net, tokens_tuples_list]


def viterbi_initialize(phi_net: list, token_net: list, index: int, phonemes_dict: dict, observations: list):
    phoneme_list = phi_net[index]
    first_phoneme = phoneme_list[0]
    idx = phonemes_dict.get(first_phoneme)
    obs_t1 = observations[0]  # only first line (t = 1)
    first_value = obs_t1[idx]
    phi_net[index][0] = first_value
    token_net[index][0] = 0

    for i in range(1, len(phoneme_list)):  # if len(phoneme_list) > 1
        phi_net[index][i] = math.inf
        token_net[index][i] = 0


def calculate_end_states_prices(phonemes_net: list, phi_net: list, words_list: list, unigrams: dict, phonemes_dict: dict, probs_list: list, beta, L_gamma):
    prices_ends_phonemes = []
    for i in range(len(phonemes_net)):
        phi = phi_net[i][-1]  # price of word's end
        end_phoneme = phonemes_net[i][-1]
        word = words_list[i]  # key to dictionary
        prob_language_model = unigrams.get(word, 0)
        idx_prob = phonemes_dict.get(end_phoneme)
        trans_prob = probs_list[idx_prob][1]

        penalty = - beta * prob_language_model + L_gamma
        prices_ends_phonemes.append(phi + trans_prob + penalty)  # -log p(O|W) - beta * log p(W) + (-L_gamma)

    return prices_ends_phonemes


def viterbi_iterative(phonemes_dict: dict, probs_list: list, min_price_end_value, min_price_token, observations: list,
                      phi_net: list, phonemes_net: list, t: int, token_net: list):
    for w in range(len(phi_net)):
        last_phi = phi_net[w].copy()
        last_token = token_net[w].copy()

        phonemes_list = phonemes_net[w]  # transcript of word in form of list of strings

        viterbi_iterative_first_phoneme(last_phi, last_token, phonemes_dict, probs_list, min_price_end_value, min_price_token,
                                        observations, phi_net, phonemes_list, t, token_net, w)

        for j in range(1, len(phonemes_list)):
            viterbi_iterative_next_phonemes(j, last_phi, last_token, phonemes_dict, probs_list, observations, phi_net,
                                            phonemes_list, t, token_net, w)


def viterbi_iterative_first_phoneme(last_phi, last_token, phonemes_dict: dict, probs_list: list, min_price_end_value,
                                    min_price_token, observations: list, phi_net: list, phonemes_list: list, t: int,
                                    token_net: list, w: int):
    first_phoneme = phonemes_list[0]
    first_phoneme_idx = phonemes_dict.get(first_phoneme)
    loop_prob = probs_list[first_phoneme_idx][0]
    price = min(min_price_end_value, last_phi[0] + loop_prob)
    if price == min_price_end_value:
        token = min_price_token
    else:
        token = last_token[0]
    phi_net[w][0] = price + observations[t][first_phoneme_idx]
    token_net[w][0] = token


def viterbi_iterative_next_phonemes(j: int, last_phi, last_token, phonemes_dict: dict, probs_list: list, observations: list,
                                    phi_net: list, phonemes_list: list, t: int, token_net: list, w: int):

    previous_phoneme = phonemes_list[j - 1]
    current_phoneme = phonemes_list[j]

    current_phoneme_idx = phonemes_dict.get(current_phoneme)
    previous_phoneme_idx = phonemes_dict.get(previous_phoneme)

    previous_phi = last_phi[j - 1] + probs_list[previous_phoneme_idx][1]  # previous + transition probability
    current_phi = last_phi[j] + probs_list[current_phoneme_idx][0]  # current + loop probability
    previous_token = last_token[j - 1]
    current_token = last_token[j]
    price = min(previous_phi, current_phi)
    if price == previous_phi:
        token = previous_token
    else:
        token = current_token

    phi_net[w][j] = price + observations[t][current_phoneme_idx]
    token_net[w][j] = token


def count_minimal_price(phi_net: list, phonemes_net: list, words_list: list, unigrams: dict, phonemes_dict: dict, probs_list: list, L_gamma, beta):
    res = calculate_end_states_prices(phonemes_net, phi_net, words_list, unigrams, phonemes_dict, probs_list, beta, L_gamma)
    final_min_price = min(res)

    return [final_min_price, res]


def get_spoken_words(final_min_price, prices_ends_phonemes: list, tokens_tuples_list: list, words_list: list):
    """
    Returns list of the words, which were spoken
    :param final_min_price:
    :param prices_ends_phonemes:
    :param tokens_tuples_list:
    :param words_list:
    :return: spoken words - list
    """
    spoken_words_list = []

    final_min_index = prices_ends_phonemes.index(final_min_price)
    final_min_token = token_net[final_min_index][-1]

    previous_token_index = final_min_token
    last_word = words_list[final_min_index]
    spoken_words_list.append(last_word)
    while previous_token_index != 0:
        token_tuple = tokens_tuples_list[previous_token_index]
        spoken_words_list.append(token_tuple[0])  # spoken word
        previous_token_index = token_tuple[1]  # previous token index
    spoken_words_list.reverse()

    return spoken_words_list


if __name__ == "__main__":
    # Paths to files
    path_vocab_file = Path(r'.\vocab')
    path_leaves_file = Path(r'.\leaves.txt')
    path_obs_file = Path(r'.\00170005_14.txt')
    path_language_model_file = Path(r'.\language_model_arpa')

    # Reading files
    [phonemes_net, words_list] = load_vocab_file(path_vocab_file)
    observations = load_observations(path_obs_file)
    [phonemes_dict, probs_list] = load_leaves(path_leaves_file)

    # Formatting language model
    language_model_sections = load_language_model(path_language_model_file)
    language_model_dictionary = create_language_model_dictionaries(language_model_sections)

    # Extracting unigrams
    unigrams = language_model_dictionary["\\1-grams:"]

    # Initializing penalty parameters
    L_gamma = -math.log10(0.01)
    beta = 5

    # Viterbi algorithm
    [phi_net, token_net, tokens_tuples_list] = viterbi(observations, phonemes_dict, probs_list, phonemes_net, words_list,
                                                       unigrams, L_gamma, beta)

    # Counting result
    [final_min_price, prices_ends_phonemes] = count_minimal_price(phi_net, phonemes_net, words_list, unigrams, phonemes_dict, probs_list, L_gamma,
                                                                  beta)
    spoken_words = get_spoken_words(final_min_price, prices_ends_phonemes, tokens_tuples_list, words_list)

    # Printing result
    print(f"Minimal price: {final_min_price}")
    print(f"Spoken words: {spoken_words}")
