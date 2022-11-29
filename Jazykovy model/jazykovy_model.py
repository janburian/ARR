import os

# Nacteni souboru
def load_file(filename:str):
    with open(filename, 'r', encoding='cp1250') as file:
        lines = file.readlines()
    file.close()
    return lines

def load_training_file(filename:str):
    words_lines = []
    with open(filename, 'r', encoding='cp1250') as file:
        for line in file:
            sentence_without_newline_char = line.rstrip()
            sentence = "".join('<s> ' + sentence_without_newline_char + ' </s>')
            words_lines.append(sentence)
    file.close()

    return words_lines # list listu (list vet), kde list = 1 veta

def delete_new_lines(words:list):
    words_pomocna = []
    for word in words:
        words_pomocna.append(word.strip('\n'))
    return words_pomocna

def create_training_set(training:list):
    words_set = set()
    for sentence in training:
        for word in sentence:
            words_set.add(word)

    return words_set

def create_ngrams(text:list, n):
    n_grams = []
    for i in range(len(text)):
        n_grams.append(text[i: i + n])
    return n_grams

def create_dictionary(ngrams:list):
    dictionary = {}
    for ngram in ngrams:
        if ngram not in dictionary:
            dictionary[ngram] = 1
        else:
            dictionary[ngram] += 1
    return dictionary

def get_words_train(train_sentences:list):
    words_list = []
    for sentence in train_sentences:
        words = sentence.split(" ")
        words_list.append(words)
    return words_list # list listu slov jednotlivych vet

def get_list_from_lists(list_of_lists: list):
    result_list = []
    for sublist in list_of_lists:
        for item in sublist:
            result_list.append(item)
    return result_list

def check_words_dictionary(list_sentence_words:list, dictionary):
    for sentence_words in list_sentence_words:
        idx = -1
        for word in sentence_words:
            idx += 1
            if word not in dictionary:
                sentence_words[idx] = '<unk>'
    return list_sentence_words

def change_format_ngrams(ngrams: list):
    result_list = []
    for ngram in ngrams:
        if not '<unk>' in ngram:
            new_format = ''.join(map(str, ngram))
            result_list.append(new_format)
    return result_list

if __name__ == "__main__":
    words_list = load_file('cestina.txt')
    training_list = load_training_file('train.txt')

    words_list_final = delete_new_lines(words_list)
    words_set = set(words_list_final)

    training_list_final = get_words_train(training_list)
    #training_set = create_training_set(training_list)
    #dictionary = create_dictionary(words_set)
    list_sentence_words = check_words_dictionary(training_list_final, words_set) # zbaveni se preklepu
    words_list = get_list_from_lists(list_sentence_words)

    unigramy = create_ngrams(words_list, 1)
    bigramy = create_ngrams(words_list, 2)
    trigramy = create_ngrams(words_list, 3)

    unigramy_new_format = change_format_ngrams(unigramy)
    bigramy_new_format = change_format_ngrams(bigramy)
    trigramy_new_format = change_format_ngrams(trigramy)

    unigramy_dictionary = create_dictionary(unigramy_new_format)
    bigramy_dictionary = create_dictionary(bigramy_new_format)
    trigramy_dictionary = create_dictionary(trigramy_new_format)


    print()