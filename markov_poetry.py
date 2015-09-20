import nltk
import re
from collections import defaultdict, Counter
import random
from bisect import bisect

def triples(word_list):
    if len(word_list) < 3:
        return
    for i in range(len(word_list) - 2):
        yield (word_list[i], word_list[i+1], word_list[i+2])

def markov(triples_list):
    chain = defaultdict(Counter)
    for triple in triples_list:
        chain[(triple[0], triple[1])][triple[2]] += 1
    return chain

def finalize_markov(markov_dict):
    final_chain = defaultdict(lambda: ((1,), ("the",)))
    for pair, third_word_dict in markov_dict.items():
        values = []
        total = 0
        for value in third_word_dict.values():
            total += value
            values.append(total)
        final_chain[pair] = (values, list(third_word_dict.keys()))
    return final_chain
    
def getWords(text):
    return re.compile('\w+').findall(text)

def weighted_rand_choice(cum_values, choices):
    i = bisect(cum_values, random.random() * cum_values[-1])
    return choices[i]

def generate(final_chain, num_words):
    seed = list(random.choice(list(final_chain.keys())))
    for x in range(num_words - 2):
        seed.append(weighted_rand_choice(*final_chain[(seed[-2], seed[-1])]))
    return seed

with open("test.txt") as f:
    text = f.read()
    words = [x.lower() for x in getWords(text)]
    print(generate(finalize_markov(markov(triples(words))), 100))
