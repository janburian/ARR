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

# TODO nacist leaves.txt

if __name__ == "__main__":
    vocab_filename = "vocab"

    mesh = load_vocab_file(vocab_filename)
    print()


