"""
Aidan Kierans
2/15/2020
CMSC 416: Intro to NLP
Prof. Bridget Thomas-McInnes

This program generates sentences using statistical data about the orders in which words are used, without any
understanding of the words' meaning. Language is complicated and always evolving, so it's easier to generate
somewhat plausible sounding text by looking at which words follow which other words than it is to construct a complete
logical representation of how we communicate. This program uses the ngram model to collect these statistics, which is
described in more detail below.

To use this program, run it from the command line with arguments in the following format, where ngram.py is the name of
the file, n is the length of the ngrams, m is the number of sentences to generate, and an arbitrary positive number of
arguments following them are file paths:
    ngram.py n m file1 file2 file3 ...
For example, the following command would generate 10 sentences using a trigram model and a training dataset composed
of 1399-0.txt, 2554-0.txt, and 2600-0.txt:
    ngram.py 3 10 1399-0.txt 2554-0.txt 2600-0.txt
Note that for best results, the total training set should contain over one million tokens. In this project, a token is
considered to be one word or instance of stopping punctuation, and stopping punctuation is considered one of ".", "?",
and "!".

Here is an example output, with some line breaks applied manually for word wrapping:
    This program generates random sentences based on an Ngram model.
    Arguments: ngram.py 3 10 1399-0.txt 2554-0.txt 2600-0.txt
    Command line settings: ngram.py 3 10
    You look after the carriage talking loudly and busily filled his eyes fixed on her elbow the expression of the
    guilty wife would be an effort sideways down the steps seemed to deprive me of the forest and the magnate had
    proposed to her with marked respect and even little nicholas said nothing of what was happening and that will help
    to get back do spend the time the roof was so frightened that she in her eyes.

    And why do you recognize him.

    As if they wont face the brilliance of her disabilities.

    But just a small cloud rose from the chase?

    The rapidity of her distress and annoyance that method of observation is subject cannot be that he was singing to
    dress your ranks on the twentyfifth in the house.

    At that moment he was.

    But im not one said anything extreme or unpleasant memories.

    Didnt i go to greet her and those who were to abandon the hope of glory had come up with anything?

    Damn it all!

    Raskolnikov followed him trying to attract his attention in spite of much that might be fully convinced not by a
    letter asking him in.


The ngram model consists of information about how probable any token is to occur after the n-1 tokens preceding it in a
sentence (which is also called the history). To get an accurate idea of the posterior probability of a token given some
history, we divide the frequency (count) of co-occurrence by the frequency of just the history occurring on its own.
Thus, a 1-gram/unigram (which has no history) just picks random tokens based on how often they occur overall, and a
big-ram or tri-gram chooses them relative to a one or two token history, and so on. My implementation combs through all
all of the documents with a deque to record the occurrences of each token and its history. Then, choosing words in a
proportionally random way as described above, it displays the sentences it generates.
"""
import sys
import re
import random
from itertools import islice, filterfalse
from collections import Counter, deque

print("This program generates random sentences based on an Ngram model.")
if len(sys.argv) > 3:  # The program should be run with arguments n, m, and at least one file
    args = sys.argv
else:  # Prompt for arguments otherwise, for debugging purposes
    args = input("Arguments: ").split(" ")
n = int(args[1])  # Length of the -grams
assert n >= 1  # No such thing as a 0-gram
m = int(args[2])  # m is the number of sentences to generate
print("Command line settings: " + args[0] + " " + args[1] + " " + args[2])


start = "<s> "  # The start tag is "<s>"
if n > 2:  # Pad with additional start tags for longer ngrams so we can still predict the first word of a sentence
    for i in range(0, n-2):
        start += "<s> "
corpus = ""
for arg_index in range(3, len(args)):  # Iterate through the remaining args
    with open(args[arg_index], 'r', encoding="utf8") as file:
        corpus += file.read()  # Add the whole file to a string
        corpus += " "
corpus = re.sub(r'[^a-zA-Z0-9.?!\s\n]', "", corpus)  # Remove all special characters
corpus = corpus.lower()  # Convert all words to lowercase
corpus = re.sub(r'\.\s?\.\s?\.', ".", corpus)  # Replace all ellipses with periods
corpus = re.sub(r'(?<=[a-zA-Z0-9])(?=[.?!])', " ", corpus)  # Add spaces between words and punctuation
corpus = re.sub(r'(?<=[.?!])(?=[a-zA-Z0-9])', " ", corpus)  # Add spaces between punctuation and words
corpus = re.sub(r'^\s*i\s*$', "I", corpus)  # Capitalize any solitary letter "i", since it's always a personal pronoun
corpus = start[:] + corpus  # Make sure to include start tags for the first sentence
if n != 1:  # This step is only necessary if we plan to record any history
    corpus = re.sub(r'(?<=[.?!])\s', " <e> <sep> " + start,
                    # The "<e>" tag and the "<sep>" tag indicate the end of the sentence's info
                    corpus)  # Lookbehind assertion: insert start and end tags after sentences
tokens = tuple(re.split(r'\s+', corpus))  # Punctuation and words are counted as separate tokens

# Build the word dictionary
token_freqs = dict(Counter(tokens))  # tdict has the key: value pair of token: frequency
if n == 1:  # For unigrams, all we have to do is print random words based on their frequencies
    # Remove tags from the dictionary
    token_freqs.pop('<s>', None)
    token_freqs.pop('<e>', None)
    for i in range(0, m):  # We want to print m "sentences"
        sentence = ""
        while True:  # Make sure the first randomly chosen token is not punctuation
            first_word = random.choices(tuple(token_freqs.keys()), weights=tuple(token_freqs.values()), k=1)  # Pick a random word
            first_word = first_word[0]
            if not re.match(r'[.?!]', first_word):  # If the token is a word, print it and exit the loop
                sentence += first_word.title()
                break
        while True:  # Keep printing words until we encounter punctuation
            # Randomly choose a word based on their frequencies
            token = random.choices(tuple(token_freqs.keys()), tuple(token_freqs.values()))
            token = token[0]
            if re.match(r'[.?!]', token):
                print(sentence + token + "\n")  # Print the sentence with its ending punctuation
                break
            else:
                sentence += " " + token  # Add the random word to the sentence
    quit()  # After generating m unigrams, an instance with n = 1 should end here.

sentences = tuple(re.split(r'<sep>', corpus))  # split sentences up based on the separator tag, removing only that tag

# Build the main dictionary and the history dictionary
ngram_freqs = Counter()  # ngram_freqs[ngrams][freq]
shorter_ngram_freqs = Counter()  # shorter_ngram_freqs[n-1grams][freq]
for sentence in sentences:  # This loop is based on the moving_average example in python's collections documentation
    tokens = tuple(re.split(r'\s+', sentence))  # Punctuation and words are counted as separate tokens
    if len(tokens) < n:  # Only consider sentences with at least n tokens (including tags)
        continue
    it = iter(tokens)  # Make our list of tokens an iterable so that our loop starts in the right place
    local_history = deque(islice(it, n-1))  # Consume the first n-1 tokens and store them as a deque
    for token in it:
        shorter_ngram_freqs[tuple(local_history)] += 1  # Record this occurrence of this n-1gram
        local_history.append(token)  # Add the new token to the right side of the history
        ngram_freqs[tuple(local_history)] += 1  # Record this occurrence of this ngram
        local_history.popleft()  # Remove the leftmost token in the history (the oldest history)
ngram_freqs = dict(ngram_freqs)
if n == 2:
    # shorter_ngram_freqs = token_freqs  # If our ngrams are bigrams, our n-1grams are unigrams, which we already made
    shorter_ngram_freqs = dict(shorter_ngram_freqs)
    # flatten ngrams
    # ngrams = {tuple(history[0], token) for (history, token) in tuple(ngram_freqs.keys())}
    # ngram_freqs = {ngram: }
else:
    shorter_ngram_freqs = dict(shorter_ngram_freqs)

# Make a dict that says the probability of some token given some other token
token_probs = {ngram: ngram_freqs[ngram]/shorter_ngram_freqs[ngram[:len(ngram)-1]]
               for ngram in tuple(ngram_freqs.keys())}
# token_probs = dict()
# for ngram in list(ngram_freqs.keys()):
#    history = str(ngram[0])
#    token_probs[ngram] = ngram_freqs[ngram] / shorter_ngram_freqs[history]


def random_token_using_ngram(history):
    """
    Generate a random token using an Ngram model.
    :param history: A tuple of the n-1 tokens preceding the token to be generated
    :return: A string token chosen randomly based on the history
    """
    # Pick only the ngrams with the same history
    matches = filterfalse(lambda ngram_key: ngram_key[:len(ngram_key)-1] != history, tuple(token_probs.keys()))
    options = dict()  # options has the key: value pair of token: probability
    for ngram in matches:
        options[ngram[len(ngram)-1:]] = token_probs[ngram]
    # new_token is a random choice from options' tokens, weighted by the probability of each token given the history
    new_token = random.choices(tuple(options.keys()), tuple(options.values()))
    return new_token[0][0]  # random.choices returns a single-element nested list, so unpack the string from that list


# Generate sentences based on ngrams
for i in range(0, m):
    local_history = start.split(" ")  # Pad local_history like the sentences are padded
    local_history.remove("")  # Remove empty strings left over from the split
    token = random_token_using_ngram(tuple(local_history))
    sentence = token.title()  # Use the token as the start of the sentence we're going to print

    # Keep generating tokens and advancing the ngram to include the new tokens, until we encounter punctuation.
    local_history = deque(local_history)
    while True:
        local_history.popleft()
        local_history.append(token)
        token = random_token_using_ngram(tuple(local_history))
        if re.match(r'[.?!]', token):  # Check whether the new token is punctuation
            print(sentence + token + "\n")  # Print the ending punctuation
            break
        else:
            sentence += " " + token  # Print the new word
