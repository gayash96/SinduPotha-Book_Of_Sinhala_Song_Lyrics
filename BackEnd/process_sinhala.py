from sinling import SinhalaTokenizer
from packages.SinhalaStemming import sinhalaStemmer


def get_sn_process_setup():

    tokenizer = SinhalaTokenizer()
    stemmer = sinhalaStemmer.stemmer()

    return tokenizer, stemmer


def token_stem(sentence, tokenizer, stemmer):
    
    final_str = ''
    word_list = tokenizer.tokenize(sentence)
    stemmer.stemming(word_list)

    for word in word_list:
        final_str += word + ' '

    return word_list, final_str[:-1]
