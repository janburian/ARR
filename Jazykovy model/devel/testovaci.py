def create_ngrams(text:list, n):
    n_grams = []
    for i in range(len(text)):
        n_grams.append(text[i: i + n])
    return n_grams


unigramy = create_ngrams(training_list_final, 1)
bigramy = create_ngrams(training_list_final, 2)
trigramy = create_ngrams(training_list_final, 3)