"""
Aidan Kierans
4/14/2020
CMSC 416: Intro to NLP
Prof. Bridget Thomas-McInnes

This program automatically analyzes the sentiment of tweets, e.g. to classify them as either "positive" or "negative" in
tone. Using a Naive Bayes model trained on a set of tagged tweets, this program determines which sentiment is the most
probable given the relative frequency of each sentiment in general, and the tokens (i.e. words and some punctuation)
that appear in the tweet.

In formal terms (or as formal as I can get without using special characters), this is equivalent to sentiment =
argmax(s within S) for P(s) * the product of P(w|s) for all words w. Multiplying lots of probabilities usually leads
to very low numbers, so we map this formula to log-space like so instead: sense = argmax(s within S) log(P(s)) + the sum
of P(t|s) for all tokens t. The baseline probability of a sentiment (P(s)) is calculated as the frequency with which
that sentiment occurs divided by the total number of occurrences of any sentiment. P(t|s) is calculated as the frequency
with which a given sentiment occurs with a particular token, divided by the total number of times that the sentiment
occurs. All frequency information is determined using the training dataset.

In the course of analyzing each tweet, stop words (words that are so common in English that they just make data more
noisy) and basic punctuation (periods and commas) and URLs beginning with "http" are removed, and all letters are made
lowercase. Also, since the model only considers


Here's the confusion matrix and accuracy for a successful run, distinguishing tweets with a "positive" sentiment from
tweets with a "negative" sentiment:
    Predicted: 	negative	positive
    Actual negative	26	46
    Actual positive	27	133

    Accuracy = 159 / 232 = 68.53448275862068%

For comparison, the baseline probability of the most frequent sentiment was 68.37%, so I only beat the baseline by a
small amount. This is a satisfactory result for a minimum viable product. It could be improved by treating some specific
features of tweets, such as hashtags, @ mentions, etc. differently.

To use this program, run it from the command line with arguments in the following format, where sentiment.py is the name
of this file, sentiment-train.txt is the filename for the labelled training data, sentiment-test.txt is the file with
the test data, my-model.txt is where the model will be logged as it is created, and my-sentiment-answers.txt is the file
to which the output will be redirected:
    sentiment.py sentiment-train.txt sentiment-test.txt my-model.txt > my-sentiment-answers.txt

Note that the right-angle bracket (">") is a bash shell special character and not specific to this program. Without this
character and the filename that follows it, the program will simply print the sentiments for the tweets from
sentiment-test.txt to the console. If only the right-angle bracket is omitted, and the output file is still included,
then this program will write or overwrite the output file with the tagged text. To run sentiment.py this way, enter
something like the following:
    sentiment.py sentiment-train.txt sentiment-test.txt my-model.txt my-sentiment-answers.txt

Also note that to use files that are not in the current folder, the absolute or relative paths of those files must be
included in the filename.

Here is an example of sentiment data that could be used as a small part of the training file:
    <instance id="620821002390339585">
    <answer instance="620821002390339585" sentiment="negative"/>
    <context>
    Does @macleansmag still believe that Ms. Angela Merkel is the "real leader of the free world"?  http://t.co/isQfoIcod0 (Greeks may disagree
    </context>

And here is an example of ambiguous data that could be used as part of the test file:
    <instance id="621351052047028224">
    <context>
    Amazon Prime Day Disappoints Some Shoppers: Amazon Prime Day promised 24 hours with "more deals than Black Fri... http://t.co/IC2k72pSXV
    </context>

Finally, here is an example of the automatically tagged version of that test data:
    <answer instance="621351052047028224" sentiment="negative"/>

"""

import sys
import re
from collections import Counter
from math import log

# Initialize variables
fr_basic_sents = Counter()
fr_word = Counter()
training_instance_count = 0
training_data = dict()


# Define functions for use in the main program and other functions


def parse_tweet(tweet):
    """
    Turn a tweet into a bag of its most important words, ignoring most punctuation.
    :param tweet: A string extracted from an instance.
    :return: A set of tokens.
    """
    # Separate highly expressive punctuation from words so that they can be recorded separately (if that helps).
    # tweet = re.sub(r'(?P<punc>[!?])', r' \g<punc>', tweet)
    tweet = re.sub(r'https?://[\S]*', r'<url_here>', tweet)  # Recognize URLs and replace them with <url_here>
    # Recognize emoticons and replace them so the parentheses don't get removed
    tweet = re.sub(r':\(', r'<frown>', tweet)
    tweet = re.sub(r':\)', r'<smile>', tweet)
    # Split the tweet up around whitespace, regular punctuation, and numbers. Also make all of the words lowercase.
    tokens = set([token.lower() for token in re.split(r'[\s.,0-9()!?"]+', tweet) if token])

    stop_words = {"and", "the", "also", "a", "i", "to", "of", "on", "my", "do", "have", "just", "this", "be", "so",
                  "is", "for", "in", "it", "you", "at", "th", "an", "if", "has", "are", "st"}
    tokens = tokens - stop_words  # Remove stop words from the list of tokens

    return tokens


def parse_instance(instance):
    """
    Parse each instance of the ambiguous word in its context to extract the instance ID, sentiment ID (if it exists),
    and the tweet itself.
    :param instance: An "instance" from the pseudo-XML-formatted plaintext from the training or testing file.
    :return: A tuple containing the instance_id and the sentiment, followed by the set of words in the tweet.
    """
    match = re.search(  # Use regex to extract the parts we care about from this instance
        (r'\s*<instance\s*id="([^"]+)">\s*'  # Isolate the instance ID
         r'(.*)'  # Capture the tag with the sentiment if it exists, or just the newline character preceding the
         # <context> tag otherwise.
         r'\s*<context>\s*'  # There should be a "<context>" tag between the instance id and the actual context.
         r'(.+)'  # Record the tweet
         r'\s*</context>\s*\Z'  # The instance should end with a "</context>" tag.
         ), instance, re.VERBOSE)  # re.VERBOSE instructs the regex parser to ignore whitespace and comments
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
    sent_label = match.group(2)  # The labelled sentiment of the tweet
    if sent_label:
        s_match = re.search(r'sentiment="([^"]+)"/>', sent_label)  # Extract the sentiment from the tag
        if s_match:  # True if this is the training data
            sent_label = s_match.group(1)
        else:
            sent_label = None  # The sentiment wasn't labeled; this must be the testing data.

    tweet = match.group(3)  # The full text of the tweet.
    bag_of_words = parse_tweet(tweet)
    # Record the sentiment and the set of words in the tweet as properties of this instance.
    # Also record the instance of the ambiguous word itself as a property in case the way it's written is meaningful.
    return instance_id, sent_label, bag_of_words


# P(a|b) = freq(a and b) / freq(b)
# P(sentiment) * Product of the P(feature|sentiment) for all features
# But we want to map everything to log space, so actually it's:
# log(P(sentiment)) + Sum of the log(P(feature|sentiment)) for all features, which is equivalent to:
# log(P(sentiment)) + Sum of the log(freq(feature and sentiment)/freq(sentiment)) for all features
def analyze(bag):
    """
    Using a Naive Bayes probability model and information about the frequency of various sentiment and feature
    combinations in the training data, predict the most probable sentiment given the bag of words.
    :param bag: The set of words that were pulled out of the testing dataset for this instance.
    :return: The most probable sentiment of the tweet given the features.
    """
    # fb = fr_basic_sents
    # fw = fr_word
    bag = bag[0]  # Unpack set from tuple
    log_sent_probs = dict()
    for s in fr_basic_sents:
        log_prob = log(fr_basic_sents[s] / training_instance_count)  # log(P(sentiment))
        for each in bag:  # Consider the words in the bag separately.
            if fr_word[s, each]:
                log_prob += log(fr_word[s, each] / fr_basic_sents[s])
            # else:
            #    not_found_in_training.append(each)
        log_sent_probs[s] = log_prob

    # Return the most probable sentiment
    return min(log_sent_probs, key=lambda k: log_sent_probs[k])


def main(training_file: str, testing_file: str, model_file: str, output_file=""):
    """
    Learn a Naive Bayes model from training_file's data to classify the sentiments of tweets in testing_file. Record
    the model in model_file as it's created and applied, and record the results to output_file (or the console if no
    output_file is supplied).
    :param training_file: The name (with path if necessary) of the file with the training data in an xml-like format.
    :param testing_file: The name (with path if necessary) of the file with the testing data in an xml-like format.
    :param model_file: The name (with path if necessary) of the file to which the model should be logged.
    :param output_file: The name (with path if necessary) of the file to which the test answers should be recorded. If
        omitted, the output will be printed to the console instead.
    """
    # Process the training data
    training_text = ""
    with open(training_file, 'r', encoding="utf8") as file:
        training_text += file.read()  # Add the whole file's text to a string

    instances = tuple(re.split(r'\s+</instance>\s+', training_text))  # Split up the instances of words' usage
    if not instances:
        raise SyntaxError("No instances found; instances may not be in the correct format. " +
                          "See usage instructions for examples of the correct instance format.")
    global training_instance_count
    training_instance_count = len(instances)
    global training_data  # This will hold the properties we note about each instance
    for inst in instances:
        properties = parse_instance(inst)
        if not properties:  # True if parse_instance returned None
            continue  # The instance was apparently blank or empty, so skip it.
        training_data[properties[0]] = tuple(properties[1:])  # Populate the training dictionary

    # Prepare to record frequency data.
    global fr_basic_sents  # This will count how often each sentiment occurs, regardless of context.
    # fr_word will have the key: value pair of (sentiment, word): count of occurrences.
    global fr_word
    # Record frequencies with which each feature corresponds to each sentiment.
    for inst in training_data:
        # Unpack the properties of the instance.
        sent, words = training_data[inst]
        fr_basic_sents[sent] += 1  # Record that this sentiment has occurred.
        for word in words:
            fr_word[tuple((sent, word))] += 1  # Record that this word occurred with this sentiment.
    assert fr_basic_sents and fr_word  # If there's no information in these, the training data was in the wrong format.

    # Write frequency data to the model file for logging and debugging purposes.
    model_text = "sentiment frequency\n"
    for sentiment in fr_basic_sents:
        model_text += sentiment + "\t" + str(fr_basic_sents[sentiment]) + "\n"
    model_text += "\nword frequency for each sentiment:\n"
    word_counts = Counter()
    for sentiment, feature in fr_word.keys():
        model_text += sentiment + "\t" + str(feature) + "\t" + str(fr_word[tuple((sentiment, feature))]) + "\n"
        word_counts[feature] += fr_word[tuple((sentiment, feature))]  # Record total occurrences of this word
    model_text += "\ntotal number of occurrences of each word:\n"
    # word_counts = word_counts.most_common()
    for word in word_counts.most_common():
        model_text += str(word) + "\t" + str(word_counts[word]) + "\n"
    with open(model_file, 'w+', encoding="utf8") as model:
        model.write(model_text + "\n")

    test_text = ""
    with open(testing_file, 'r', encoding="utf8") as file:
        test_text += file.read()  # Add the whole file's text to a string

    output = ""
    instances = tuple(re.split(r'\s+</instance>\s+', test_text))  # Split the test data into instances for parsing.
    if not instances:
        raise SyntaxError("No instances found; instances may not be in the correct format. " +
                          "See usage instructions for examples of the correct instance format.")
    with open(model_file, 'a', encoding="utf8") as model:  # Describe the model as we use it, for logging purposes
        model.write("instance_id\tsentiment_id\tbag_of_words\n")  # Write the header for the next section of the model
        for inst in instances:
            # Parse the instance
            properties = parse_instance(inst)
            if not properties:  # True if parse_instance returned None
                continue  # The instance was apparently blank or empty, so skip it.
            # The sentiment_id property (properties[1]) will be blank (because this is a test), so we will ignore it.
            inst_id = properties[0]
            sentiment = analyze(properties[2:])  # Skip over properties[1], which is the blank sentiment_id.
            model.write("\t".join([inst_id, sentiment, str(properties[2])]) + "\n")
            output += "<answer instance=\"" + inst_id + "\" sentiment=\"" + sentiment + "\"/>\n"

    if output_file and output_file != ">":  # If the output file was included in the arguments, write the output there
        with open(output_file, 'w+', encoding="UTF8") as file:
            file.write(output)  # Write the entire output to the file
    else:
        print(output)


if __name__ == "__main__":
    # Prompt for arguments if they aren't supplied initially
    main_args = sys.argv[1:] if len(sys.argv) > 1 else input("Arguments: ").split(" ")
    if len(main_args) > 4:
        main_args = main_args[:4]  # If there are too many arguments, only use the first four.

    main(*main_args) # Run the main function with the (unpacked) list of arguments
