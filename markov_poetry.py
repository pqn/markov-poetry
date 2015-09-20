import nltk, re, random
from collections import defaultdict, Counter
from bisect import bisect

ACCEPTABLE_POS = frozenset(["NOUN", "ADJ", "ADV", "VERB"])
VOWELS = frozenset("AA AE AH AO AW AY EH ER EY IH IY OW OY UH UW".split(" "))
syllable_db = {thing[0] : thing[1] for thing in nltk.corpus.cmudict.entries()}

def triples(word_list):
    if len(word_list) >= 3:
        for i in range(len(word_list) - 2):
            yield (word_list[i], word_list[i+1], word_list[i+2])

def markov(triples_list):
    chain = defaultdict(Counter)
    for triple in triples_list:
        chain[(triple[0], triple[1])][triple[2]] += 1
    return chain

def finalize_markov(markov_dict):
    final_chain = dict()
    second_words = defaultdict(set)
    for pair, third_word_dict in markov_dict.items():
        values = []
        total = 0
        for value in third_word_dict.values():
            total += value
            values.append(total)
        final_chain[pair] = (values, list(third_word_dict.keys()))
        second_words[pair[0]].add(pair[1])
    return final_chain, second_words
    
def getWords(text):
    return re.compile('[\w\']+').findall(text)

def weighted_rand_choice(A):
    (cum_values, choices) = A
    i = bisect(cum_values, random.random() * cum_values[-1])
    return choices[i]

def generate(final_chain, num_words, word=None, second_words=None):
    if word is None:
        seed = list(random.choice(list(final_chain.keys())))
    else:
        seed = [word, random.choice(list(second_words[word]))]
    for x in range(num_words - 2):
        seed.append(weighted_rand_choice(final_chain.get((seed[-2], seed[-1]), random.choice(list(final_chain.values())))))
    return seed

def ending_db(reasonable_ends):
    syllable_lookup = defaultdict(set)
    for word in reasonable_ends:
        if word in syllable_db:
            entry = syllable_db[word]
            if entry[-1][:2] in VOWELS and entry[-1][-1] in "012" and int(entry[-1][-1]) > 0:
                syllable_lookup[entry[-1]].add(word)
            if len(entry) >= 2 and entry[-2][:2] in VOWELS and entry[-2][-1] in "012" and int(entry[-2][-1]) > 0:
                syllable_lookup[(entry[-2][:2], entry[-1][:2])].add(word)
            if len(entry) >= 3 and entry[-3][:2] in VOWELS and entry[-3][-1] in "012" and int(entry[-3][-1]) > 0:
                syllable_lookup[(entry[-3][:2], entry[-2][:2], entry[-1][:2])].add(word)
    return {key: syllable_lookup[key] for key in syllable_lookup.keys() if len(syllable_lookup[key]) >= 2}

def generate_line_pair(final_chain, endings, num_words, second_words):
    pair = random.sample(endings[random.choice(list(endings.keys()))], 2)
    result1 = generate(final_chain, 10, word=pair[0], second_words=second_words)
    result1.reverse()
    result2 = generate(final_chain, 10, word=pair[1], second_words=second_words)
    result2.reverse()
    return [result1, result2]

def punctuate(lines):
    if random.random() < 0.2:
        first = "-"
        second = "?"
    elif random.random() < 0.4:
        first = ","
        second = "!"
    else:
        first = ","
        second = "."
    return " ".join(lines[0]).capitalize() + first + "\n" + " ".join(lines[1]).capitalize() + second + "\n"

def markov_poem(text):
    words = [x.lower() for x in getWords(text)]
    reasonable_ends = frozenset([thing[0] for thing in nltk.pos_tag(list(set(words)), tagset="universal") if thing[1] in ACCEPTABLE_POS])
    words.reverse()
    (final_chain, second_words) = finalize_markov(markov(triples(words)))
    endings = ending_db(reasonable_ends)
    return "\n".join([punctuate(generate_line_pair(final_chain, endings, 10, second_words)) for x in range(5)])

if __name__ == "__main__":
    with open("moby_dick.txt") as f:
        text = f.read()
        print(markov_poem(text))
