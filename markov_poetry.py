import nltk
import re
from collections import defaultdict, Counter
import random
from bisect import bisect

ACCEPTABLE_POS = frozenset(["NOUN", "ADJ", "ADV", "VERB"])
VOWELS = frozenset("AA AE AH AO AW AY EH ER EY IH IY OW OY UH UW".split(" "))

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
    final_chain = dict()
    for pair, third_word_dict in markov_dict.items():
        values = []
        total = 0
        for value in third_word_dict.values():
            total += value
            values.append(total)
        final_chain[pair] = (values, list(third_word_dict.keys()))
    return final_chain
    
def getWords(text):
    return re.compile('[\w\']+').findall(text)

def weighted_rand_choice(A):
    (cum_values, choices) = A
    i = bisect(cum_values, random.random() * cum_values[-1])
    return choices[i]

def generate(final_chain, num_words):
    seed = list(random.choice(list(final_chain.keys())))
    for x in range(num_words - 2):
        seed.append(weighted_rand_choice(final_chain.get((seed[-2], seed[-1]), random.choice(list(final_chain.values())))))
    return seed

def ending_db(reasonable_ends):
    syllable_db = nltk.corpus.cmudict.entries()
    syllable_lookup = defaultdict(set)
    for entry in syllable_db:
        if entry[0] in reasonable_ends:
            if entry[1][-1][:2] in VOWELS and entry[1][-1][-1] in "012" and int(entry[1][-1][-1]) > 0:
                syllable_lookup[entry[1][-1]].add(entry[0])
            if len(entry[1]) >= 2 and entry[1][-2][:2] in VOWELS and entry[1][-2][-1] in "012" and int(entry[1][-2][-1]) > 0:
                syllable_lookup[(entry[1][-2][:2], entry[1][-1][:2])].add(entry[0])
            if len(entry[1]) >= 3 and entry[1][-3][:2] in VOWELS and entry[1][-3][-1] in "012" and int(entry[1][-3][-1]) > 0:
                syllable_lookup[(entry[1][-3][:2], entry[1][-2][:2], entry[1][-1][:2])].add(entry[0])
    return {key: syllable_lookup[key] for key in syllable_lookup.keys() if len(syllable_lookup[key]) >= 2}

def generate_line_pair(final_chain, num_words):
    pass # TODO

with open("moby_dick.txt") as f:
    text = f.read()
    words = [x.lower() for x in getWords(text)]
    reasonable_ends = frozenset([thing[0] for thing in nltk.pos_tag(list(set(words)), tagset="universal") if thing[1] in ACCEPTABLE_POS])
    words.reverse()
    result = generate(finalize_markov(markov(triples(words))), 100)
    result.reverse()
    #print(result)
    print(ending_db(reasonable_ends))
