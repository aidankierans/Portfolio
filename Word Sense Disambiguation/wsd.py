"""
Aidan Kierans
4/2/2020
CMSC 416: Intro to NLP
Prof. Bridget Thomas-McInnes

This program automatically performs word sense disambiguation (WSD) on instances of a word with only the context of a
few sentences for each one, using a Naive Bayes model trained on a set of tagged sentences. WSD is necessary because of
homonyms and homographs; two words can have the same spelling, but different meanings, and only context can distinguish
them. In this case, the context for each instance of a word is used to compute which meaning/sense is the most probable
given the relative frequency of each sense in general, and the important parts of the context.

In formal terms (or as formal as I can get without using special characters), this is equivalent to sense =
argmax(s within S) for P(s) * the product of P(f|s) for all features f. Multiplying lots of probabilities usually leads
to very low numbers, so we map this formula to log-space like so instead: sense = argmax(s within S) log(P(s)) + the sum
of P(f|s) for all features f. The baseline probability of a word sense (P(s)) is calculated as the frequency with which
that word sense occurs divided by the total number of occurrences of any word sense. P(f|s) is calculated as the
frequency with which a given word sense occurs with a particular value of a given feature, divided by the total number
of times that word sense occurs.

Here's the confusion matrix and accuracy for a successful run, regarding the word "line" which can either be a telephone
line or a product line:
    Predicted: 	phone	product
    Actual phone	58	14
    Actual product	18	36

    Accuracy = 94 / 126 = 74.60317460317461%

For comparison, the baseline probability of the most frequent word sense was 52.41%.

To use this program, run it from the command line with arguments in the following format, where wsd.py is the name of
this file, line-train.txt is the filename for the labelled training data, line-test.txt is the file with the words to be
disambiguated, my-model.txt is where the model will be logged as it is created, and my-line-answers.txt is the file to
which the output will be redirected:
    wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt

Note that the right-angle bracket (">") is a bash shell special character and not specific to this program. Without this
character and the filename that follows it, the program will simply print the word senses for the text from
line-test.txt to the console. If only the right-angle bracket is omitted, and the output file is still included, then
this program will write or overwrite the output file with the tagged text. To run wsd.py this way, enter something
like the following:
    wsd.py line-train.txt line-test.txt my-model.txt my-line-answers.txt

Also note that to use files that are not in the current folder, the absolute or relative paths of those files must be
included in the filename.

Here is an example of word sense data that could be used as a small part of the training file:
    <instance id="line-n.w9_10:6830:">
    <answer instance="line-n.w9_10:6830:" senseid="phone"/>
    <context>
     <s> The New York plan froze basic rates, offered no protection to Nynex against an economic downturn that sharply cut demand and didn't offer flexible pricing. </s> <@> <s> In contrast, the California economy is booming, with 4.5% access <head>line</head> growth in the past year. </s>
    </context>
    </instance>

And here is an example of ambiguous data that could be used as part of the test file:
    <instance id="line-n.w8_059:8174:">
    <context>
     <s> Advanced Micro Devices Inc., Sunnyvale, Calif., and Siemens AG of West Germany said they agreed to jointly develop, manufacture and market microchips for data communications and telecommunications with an emphasis on the integrated services digital network. </s> <@> </p> <@> <p> <@> <s> The integrated services digital network, or ISDN, is an international standard used to transmit voice, data, graphics and video images over telephone <head>lines</head> . </s>
    </context>
    </instance>

Finally, here is an example of the automatically tagged version of that test data:
    <answer instance="line-n.w8_059:8174:" senseid="phone"/>

Features used:
w_minus_1: The word at offset -1 from (i.e. in the position directly to the left of) the ambiguous word.
w_plus_1: The word at offset +1 from (i.e. in the position directly to the right of) the ambiguous word.
pair_m2_m1: The ordered pair of words at offsets -2 and -1 from the ambiguous word.
pair_m1_p1: The ordered pair of words at offsets -1 and +1 from the ambiguous word.
pair_p1_p2: The ordered pair of words at offsets +1 and +2 from the ambiguous word.
window: The "bag"/set of words that appear in the 5 word window on either side of the ambiguous word, i.e. between the
    offsets of -5 and -1 (inclusive) and/or between the offsets of +1 and +5 (inclusive) from the ambiguous word.
word: The particular spelling/form of the ambiguous word, e.g. line vs. lines vs Line vs. Lines.

The features used in this model were adapted from Yarowsky, 1994: https://arxiv.org/abs/cmp-lg/9406034
I chose the window size myself, and added the "word" feature. The window feature alone can be used for disambiguation
with an accuracy of roughly 70%, and the addition of the "word" feature to the full feature list is what brings it from
less than 73.02% to over 74.60%.

"""

import sys
import re
from collections import Counter
from math import log

if len(sys.argv) > 3:  # The program should be run with arguments for the training, testing, and log files
    args = sys.argv
else:  # Prompt for arguments otherwise
    args = input("Arguments: ").split(" ")


def parse_instance(instance):
    """
    Parse each instance of the ambiguous word in its context to extract the instance ID, sense ID (if it exists), and
    features of the context/word itself.
    :param instance: An "instance" from the pseudo-XML-formatted plaintext from the training or testing file.
    :return: A tuple containing the instance_id and the sense_id, followed by the w_minus_1, w_plus_1, pair_m2_m1,
        pair_m1_p1, pair_p1_p2, window, and word features, in that order.
    """
    match = re.search(  # Use regex to extract the parts we care about from this instance
        (r'\s*<instance\s*id="([^"]+)">'  # Isolate the instance ID
         r'(.*)'  # Capture the tag with the sense ID if it exists, or just the newline character preceding the
         # <context> tag otherwise.
         r'\s*<context>\s*'  # There should be a context tag between the instance id and the actual context.
         r'.*<s>(.*)\s*<head>'  # Use .* and the <head> tag to make sure we're in the sentence with the ambiguous word.
         r'(\w+)'  # Record the word
         r'</head>\s*([^<]*)<'  # Consume the rest of the sentence, as denoted by the </s> tag.
         ), instance, re.VERBOSE | re.DOTALL)  # re.VERBOSE instructs the regex parser to ignore whitespace and comments
    # re.DOTALL ensures that the "." character can also match newlines.
    if not match and re.fullmatch(r'\s*', instance):
        # raise SyntaxError("Empty instance encountered.")
        return None
    else:
        if not match:
            return None
    #        raise SyntaxError("Instance is not in the expected format. " +
    #                          "See usage instructions for examples of the correct instance format.")
    # full_match = match.group(0)
    instance_id = match.group(1)  # The unique ID of this instance in the training data
    if instance_id in training_data:  # Make sure that the instance ID is unique.
        raise ValueError("The instance ID \"" + instance_id + "\"" +
                         " appears more than once, but instance IDs should be unique.")
    sense_id = match.group(2)  # The unambiguous sense in which the word was meant
    if sense_id:
        sense_match = re.search(r'senseid="([^"]+)"/>', sense_id)  # Extract the sense ID from the tag
        if sense_match:  # True if this is the training data
            sense_id = sense_match.group(1)
        else:
            sense_id = None
    sentence_part_1 = match.group(3)  # The part of the sentence preceding the ambiguous word
    word = match.group(4)  # The ambiguous word itself, which may or may not be plural or otherwise modified.
    sentence_part_2 = match.group(5)  # The rest of the sentence with the ambiguous word

    # Split the sentence up, ignoring whitespace, numbers, and punctuation, and removing empty strings.
    pre_w = [word for word in re.split(r'[\s.,!?"0-9]+', sentence_part_1) if word]
    post_w = [word for word in re.split(r'[\s.,!?0-9]+', sentence_part_2) if word]

    # Record collocated words as features of this word's context, if they exist.
    w_minus_1 = pre_w[len(pre_w) - 1] if pre_w else None  # The word immediately before the ambiguous word
    w_plus_1 = post_w[0] if post_w else None  # The word immediately after the ambiguous word
    # The pair of words before the ambiguous word
    pair_m2_m1 = tuple((pre_w[len(pre_w) - 2], w_minus_1)) if len(pre_w) >= 2 else None
    # The pair of words before and after the ambiguous word
    pair_m1_p1 = tuple((w_minus_1, w_plus_1)) if w_minus_1 and w_plus_1 else None
    # The pair of words after the ambiguous word
    pair_p1_p2 = tuple((w_plus_1, post_w[1])) if len(post_w) >= 2 else None

    # Record which words occur within a window of ±5 words from the ambiguous word.
    # If the ambiguous word is too close to the beginning/end of the sentence for that, just record as much as possible.
    window = [pre_w[i] for i in range(len(pre_w) - 5, len(pre_w))] if len(pre_w) >= 5 else pre_w[:]
    window += [post_w[i] for i in range(0, 5)] if len(post_w) >= 5 else post_w[:]
    window = set(window)  # We only which words occur nearby, so ignore order and duplicates

    # Record the sense_id and the contextual features as properties of this instance.
    # Also record the instance of the ambiguous word itself as a property in case the way it's written is meaningful.
    return instance_id, sense_id, w_minus_1, w_plus_1, pair_m2_m1, pair_m1_p1, pair_p1_p2, window, word


training_text = ""
with open(args[1], 'r', encoding="utf8") as file:
    training_text += file.read()  # Add the whole file's text to a string

instances = tuple(re.split(r'\s+</instance>\s+', training_text))  # Split up the instances of words' usage
if not instances:
    raise SyntaxError("No instances found; instances may not be in the correct format. " +
                      "See usage instructions for examples of the correct instance format.")
training_instance_count = len(instances)
training_data = dict()  # This will hold the properties we note about each instance
for inst in instances:
    properties = parse_instance(inst)
    if not properties:  # True if parse_instance returned None
        continue  # The instance was apparently blank or empty, so skip it.
    training_data[properties[0]] = tuple(properties[1:])  # Populate the training dictionary with only the relevant data

# Prepare to record frequency data.
fr_basic_sense = Counter()  # This will count how often each sense occurs, regardless of context.
# Each of the following counters will have the key: value pair of (sense_id, feature's value): count of occurrences.
fr_w_minus_1 = Counter()
fr_w_plus_1 = Counter()
fr_pair_m2_m1 = Counter()
fr_pair_m1_p1 = Counter()
fr_pair_p1_p2 = Counter()
fr_window = Counter()
fr_word = Counter()
# Record frequencies with which each feature corresponds to each sense.
for inst in training_data:
    # Unpack the properties of the instance.
    sense, minus_1, plus_1, m2_m1, m1_p1, p1_p2, wndw, wrd = training_data[inst]
    # sense, minus_1, plus_1, m2_m1, m1_p1, p1_p2, wndw = training_data[inst]
    fr_basic_sense[sense] += 1  # Record that this sense has occurred.
    # Record the occurrence of each feature as associated with this sense.
    if minus_1:
        fr_w_minus_1[tuple((sense, minus_1))] += 1
    if plus_1:
        fr_w_plus_1[tuple((sense, plus_1))] += 1
    if m2_m1:
        fr_pair_m2_m1[tuple((sense, m2_m1))] += 1
    if m1_p1:
        fr_pair_m1_p1[tuple((sense, m1_p1))] += 1
    if p1_p2:
        fr_pair_p1_p2[tuple((sense, p1_p2))] += 1
    if wndw:
        for w in wndw:  # Just count that the window included a word, not the specific order or combination of words.
            fr_window[tuple((sense, w))] += 1
    if wrd:
        fr_word[tuple((sense, wrd))] += 1

# Write frequency data to the model file for logging and debugging purposes.
model_text = "Sense frequency\n"
for sense in fr_basic_sense:
    model_text += sense + "\t" + str(fr_basic_sense[sense]) + "\n"
section_headings = ("\nw_minus_1 frequency for each sense:\n",
                    "\nw_plus_1 frequency for each sense:\n",
                    "\npair_m2_m1 frequency for each sense:\n",
                    "\npair_m1_p1 frequency for each sense:\n",
                    "\npair_p1_p2 frequency for each sense:\n",
                    "\nwindow frequency for each sense:\n",
                    "\nword frequency for each sense:\n")
frequencies = (fr_w_minus_1, fr_w_plus_1, fr_pair_m2_m1, fr_pair_m1_p1, fr_pair_p1_p2, fr_window, fr_word)
for sec, freq in zip(section_headings, frequencies):
    model_text += sec
    for sense, feature in freq.keys():
        model_text += sense + "\t" + str(feature) + "\t" + str(freq[tuple((sense, feature))]) + "\n"

with open(args[3], 'w+', encoding="utf8") as model:
    model.write(model_text + "\n")


# P(a|b) = freq(a and b) / freq(b)
# P(sense) * Product of the P(feature|sense) for all features
# But we want to map everything to log space, so actually it's:
# log(P(sense)) + Sum of the log(P(feature|sense)) for all features, which is equivalent to:
# log(P(sense)) + Sum of the log(freq(feature and sense)/freq(sense)) for all features
def disambiguate(features):
    """
    Using a Naive Bayes probability model and information about the frequency of various sense and feature combinations
    in the training data, predict the most probable sense given these specific features.
    :param features: The tuple of features that were pulled out of the testing dataset for this instance.
    :return: The most probable sense for the ambiguous word given the features.
    """
    # Organize the features and frequency information so it can be traversed easily
    w_minus_1, w_plus_1, pair_m2_m1, pair_m1_p1, pair_p1_p2, window, word = features
    # Omit window and fr_window from the following lists because it they have to be traversed differently.
    features = w_minus_1, w_plus_1, pair_m2_m1, pair_m1_p1, pair_p1_p2, word
    freq_lists = fr_w_plus_1, fr_w_minus_1, fr_pair_m2_m1, fr_pair_m1_p1, fr_pair_p1_p2, fr_word

    log_sense_probs = dict()
    for s in fr_basic_sense:  # TODO: figure out how, if at all, this stuff should be logged to the model file
        log_prob = log(fr_basic_sense[s] / training_instance_count)  # log(P(sense))
        for feat, freq_list in zip(features, freq_lists):
            if freq_list[s, feat] > 0:  # Ignore this feature if it will lead to an undefined logarithm.
                log_prob += log(freq_list[s, feat] / fr_basic_sense[s])
        for each in window:  # Consider the words in the window separately.
            if fr_window[s, each]:
                log_prob += log(fr_window[s, each] / fr_basic_sense[s])
        log_sense_probs[s] = log_prob

    word_sense = min(log_sense_probs, key=lambda k: log_sense_probs[k])
    return word_sense


test_text = ""
with open(args[2], 'r', encoding="utf8") as file:
    test_text += file.read()  # Add the whole file's text to a string

output = ""
instances = tuple(re.split(r'\s+</instance>\s+', test_text))  # Split the test data into instances so we can parse them.
if not instances:
    raise SyntaxError("No instances found; instances may not be in the correct format. " +
                      "See usage instructions for examples of the correct instance format.")
with open(args[3], 'a', encoding="utf8") as model:  # Describe the model as we use it, for logging purposes
    model.write("instance_id\tsense_id\tw_minus_1\tw_plus_1\tpair_m2_m1\tpair_m1_p1\tpair_p1_p2\twindow\tword\n")
    for inst in instances:
        # Parse the instance. Note that the sense_id property (properties[1]) will be blank, so we will ignore it.
        properties = parse_instance(inst)
        if not properties:  # True if parse_instance returned None
            continue  # The instance was apparently blank or empty, so skip it.
        inst_id = properties[0]
        sense = disambiguate(properties[2:])  # Skip over properties[1], which is the blank sense_id.
        model.write(inst_id + "\t" + sense + "\t" + str(properties[2]) + "\t" + str(properties[3]) + "\t" +
                    str(properties[4]) + "\t" + str(properties[5]) + "\t" + str(properties[6]) + "\t" +
                    str(properties[7]) + "\t" + str(properties[8]) + "\n")
        output += "<answer instance=\"" + inst_id + "\" senseid=\"" + sense + "\"/>\n"

if len(args) > 4 and args[4] != ">":  # If the output file was included in the arguments, write the output to the file
    with open(args[4], 'w+', encoding="UTF8") as file:
        file.write(output)  # Write the entire output to the file
else:
    print(output)
# print(output, file=sys.stdout)
