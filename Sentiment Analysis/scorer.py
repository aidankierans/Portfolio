"""
Aidan Kierans
4/14/2020
CMSC 416: Intro to NLP
Prof. Bridget Thomas-McInnes

This program automatically assesses the accuracy of a file's sense tags overall, which is calculated (True Positive +
True Negative) / (True Positive + True Negative + False Positive + False Negative). The output is the accuracy and the
confusion matrix.

To use this program, run it from the command line with arguments in the following format, where scorer.py is the name of
this file, my-sentiment-answers.txt is the filename for the automatically tagged data, sentiment-test-key.txt is the
file with the manually tagged data (the gold standard), and pos-tagging-report.txt is the file to which the output will
be redirected:
    scorer.py my-sentiment-answers.txt sentiment-test-key.txt

Also note that to use files that are not in the current folder, the absolute or relative
paths of those files must be included in the filename.

Here is an example of automatically tagged data that could be used in the input file:
    <answer instance="line-n.w8_059:8174:" senseid="phone"/>

And here is an example of the human-tagged version of that data:
    <answer instance="line-n.w8_059:8174:" senseid="phone"/>

This output would look something like this (assuming there are many additional examples):
    Predicted: 	negative	positive
    Actual negative	24	48
    Actual positive	30	130

    Accuracy = 154 / 232 = 66.37931034482759%

"""
import sys
import re
from collections import Counter


def parse_answers(answer_text):
    """
    Assume that the list of answers is in the same order for both the automatically generated results and the gold
    standard. Accordingly, pull out the sequence of word senses from whichever file's text is currently being looked at,
    and return that list so it can be directly compared to the other one.
    :param answer_text: The full text of a file with answers in the following format:
    '<answer instance="line-n.w8_059:8174:" senseid="phone"/>'
    :return: A list of all of the sense ID's from the text, still in their original order.
    """
    answers = answer_text.split("\n")
    # answer_dict = dict()
    answer_list = []
    for answer in answers:
        match = re.search(r'answer\s*instance="(.*)"[\s\w]+="(.*)"', answer)
        if match:
            # answer_dict[str(match.group(1))] = answer_dict(str(match.group(2)))
            s = match.group(2)
            answer_list.append(s)
    return answer_list


def main(automatic_file, gold_standard_file, output_file=""):
    """
    Traverse automatic_file and gold_standard_file to count the true positives, false positives, true negatives, and
    false negatives. Then, report the confusion matrix and accuracy to output_file, or straight to the console if no
    output_file is supplied.
    :param automatic_file: The name (with path if necessary) of the file with the automatically generated sentiment
        for each instance.
    :param gold_standard_file: The name (with path if necessary) of the file with the actual sentiment of each instance.
    :param output_file: The name (with path if necessary) of the file to which the output should be written. If omitted,
        the output will be printed to the console.
    """
    automatic_data = ""
    try:
        with open(automatic_file, 'r', encoding='UTF8') as file:
            automatic_data += file.read()  # Add the whole file's text to a string
    except UnicodeDecodeError:
        with open(automatic_file, 'r', encoding='UTF16') as file:  # Use a different unicode scheme in case that works
            automatic_data += file.read()  # Add the whole file's text to a string

    gold_standard = ""
    try:
        with open(gold_standard_file, 'r', encoding='UTF8') as file:
            gold_standard += file.read()
    except UnicodeDecodeError:
        with open(gold_standard_file, 'r', encoding='UTF16') as file:  # Use a different unicode scheme in case that works
            automatic_data += file.read()  # Add the whole file's text to a string

    # Count all of the tokens and tags
    auto_answers = parse_answers(automatic_data)
    gold_answers = parse_answers(gold_standard)
    auto_gold_tuples = zip(auto_answers, gold_answers)
    predicted_vs_actuals = Counter()
    for auto_sense, gold_sense in auto_gold_tuples:  # Iterate through the token/tag pairs to count and compare results.
        predicted_vs_actuals[auto_sense, gold_sense] += 1  # auto_sense is predicted, gold_sense is actual


    sentiment_order = list(set(auto_answers + gold_answers))  # Get the list of possible answers
    sentiment_order.sort()
    running_counts = Counter()
    output = "Predicted: "
    for sense in sentiment_order:
        output += "\t" + sense
    output += "\n"

    # Find the ratio of (TP + TN) / (TP + TN + FP + FN) to calculate the accuracy
    for actual in sentiment_order:
        output += "Actual " + actual
        for predicted in sentiment_order:
            count = predicted_vs_actuals[tuple((predicted, actual))]
            if predicted == actual:
                running_counts["correct"] += count
            running_counts["total"] += count
            output += "\t" + str(count)
        output += "\n"

    assert len(running_counts) != 0
    accuracy = running_counts["correct"] / running_counts["total"]
    output += "\nAccuracy = " + str(running_counts["correct"]) + " / " + str(running_counts["total"]) + " = "\
              + str(accuracy * 100) + "%"

    if output_file and output_file != ">":  # If the output file was included in the arguments, write the output there
        with open(output_file, 'w+', encoding="UTF8") as file:
            file.write(output)  # Write the entire output to the file
    else:
        print(output)


if __name__ == "__main__":
    command_line_args = sys.argv[:]
    if len(command_line_args) > 2:  # The program should be run with arguments for the training and testing files
        main_args = command_line_args
    else:  # Prompt for arguments if not enough were found
        main_args = input("Arguments: ").split(" ")

    main(*main_args)  # Run the main function with the (unpacked) list of arguments
