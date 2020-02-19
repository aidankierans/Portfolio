"""
Aidan Kierans
2/1/2020
CMSC 416: Intro to NLP
Prof. Bridget Thomas-McInnes

The goal is to simulate a teletype-based conversation with a Rogerian-style psychotherapist named Eliza, based on the
1966 program written by Joseph Weizenbaum towards the same end. The Rogerian style of psychotherapy mostly involves
turning the client's statements into probing questions, so they can talk themselves to a solution. This can be
accomplished by a computer program that simply modifies sentences according to predefined patterns, without any idea
of meaning attached to the words by the program.

To use the program, execute it from the command line with no arguments. Eliza is most able to understand grammatically
correct sentences written in simple English. When you're done talking, say goodbye to exit.

Example input and output:
  OUTPUT: Hello, my name is Eliza. What's your name?
INPUT: My name is Sam.
  OUTPUT: Nice to meet you, Sam. You can let me know you're ready to leave any time by saying "goodbye".
  Is there anything in particular you want to talk about today?
INPUT: I feel tired
  OUTPUT: Tell me more about how you feel tired.
INPUT: I keep having to stay up late
  OUTPUT: Is there a reason that you keep having to stay up late?
INPUT: I need to finish my work
  OUTPUT: What would it mean to you if you got to finish your work?
INPUT: I could go to sleep
  OUTPUT: Is there a reason that you could go to sleep?
INPUT: I'd have nothing else left to do
  OUTPUT: Could you elaborate?
INPUT: No thank you, goodbye.
  OUTPUT: Have a nice day, Sam.


The algorithm for the main part of the program has two parts: first, it replaces words in the first person with words in
the second person, and vice versa. Second, it uses a variety of different patterns to compare the sentence to, and
changes the sentence further depending on which pattern it matched. The patterns are listed in descending order of
(approximate) specificity and importance, so the first pattern a sentence matches with determines how it will be
changed. All pattern matching is done using RegEx, besides some comparisons of one full string to another full string.
To increase verisimilitude, some data from the introduction phase (specifically the user's name and the main
topic of the session) are remembered throughout the session, and there are also a couple of points where the pattern to
use is randomly chosen from a short list of matching candidates.

"""
import re
import random


def change_person(token):
    """Changes tokens from first person to second person, or from second person to first person."""
    unchanged = token
    unchanged = unchanged.lower()  # Change the text to lower case for ease of comparison
    changing = unchanged
    # try to change from first person to second person
    changing = re.sub(r'\Ai\Z', "you", changing)  # Change "i" to "you"
    changing = re.sub(r'\Ame\Z', "you", changing)  # Change "me" to "you"
    changing = re.sub(r'\Amy\Z', "your", changing)  # Change "my" to "your"
    changing = re.sub(r'\Amine\Z', "yours", changing)  # Change "mine" to "yours"
    changing = re.sub(r"\Ai'm\Z", "you're", changing)  # Change "i'm" to "you're"
    changing = re.sub(r'\Aam\Z', "are", changing)  # Change "am" to "are", so that "I am" becomes "you are"
    changing = re.sub(r'\Ai\'ve\Z', "you've", changing)  # Change "i've" to "you've"
    if changing != unchanged:
        return changing  # It's important to return early here so that second person doesn't get changed back to first
    # try to change from second person to first person
    changing = re.sub(r'\Ayou\Z', "I", changing)  # Change "you" to I
    changing = re.sub(r'\Ayour\Z', "my", changing)  # Change "your" to "my"
    changing = re.sub(r'\Ayours\Z', "mine", changing)  # Change "yours" to "mine"
    changing = re.sub(r"\Ayou're\Z", "I'm", changing)  # Change "you're" to "I'm"
    changing = re.sub(r'\Aare\Z', "am", changing)  # Change "are" to "am", so that "you are" becomes "I am"
    changing = re.sub(r"\Aaren't\Z", "am not", changing)  # Change "aren't" to "am not"
    changing = re.sub(r'\Ayou\'ve\Z', "I've", changing)  # Change "you've" to "I've"
    if changing != unchanged:
        return changing
    else:
        return token  # The word didn't need to be changed after all; keep its case how it was.


name = input("Hello, my name is Eliza. What's your name?\n")
temp = re.search(r'\A(.+)\s(\w+)(\W*)\Z', name)  # Catches multi-word inputs, like "My name is Aidan" or "I'm Aidan."
if temp:
    name = temp.group(2)  # Only keep the last word, which is hopefully the actual name
subject = input("Nice to meet you, " + name + ". You can let me know you're ready to leave any time by saying "
                                              "\"goodbye\".\nIs there anything in particular you want to talk about"
                                              " today?\n")
temp = re.search(r'\A(\W*)([^.]*)(\W*)', subject)
response = subject
subject = temp.group(2)  # Remove any leading or trailing whitespace and punctuation
tokens = re.split(r'\s+', subject)
tokens = (change_person(token) for token in tokens)
subject = ' '.join(tokens)
while not re.search(r'.*[g|G]ood[b|B]ye.*', response):
    if re.search(r'.*\?.*', response):  # Check if the user entered a question mark
        response = input("That's not for me to say. What do you think?\n")
        continue
    temp = re.search(r'\A(\W*)([^.]*)(\W*)', response)
    response = temp.group(2)  # Remove all leading/trailing whitespace and/or special characters

    tokens = re.split(r'\s+', response)
    tokens = (change_person(token) for token in tokens)
    changed = ' '.join(tokens)
#    response = changed
    if response != changed:  # The user said something personal
        think = re.search(r'(.*)\b(think)\b(.+)', changed)  # Check for statements like "I think..."
        negative = re.search(r'.*((do\snot)|(don\'t)).*((think)|(feel)).*', changed)  # Check for statements like "I don't think..." or "I don't feel like..."
        if think:
            rand = random.randint(1, 5)  # Randomly choose which follow-up question to use.
            if rand != 4 and not negative:
                response = input("What gives you the impression that" + think.group(3) + "?\n")
                continue
            if rand != 4 and negative:
                response = input("Why don't you think that" + think.group(3) + "?\n")
                continue
            if rand == 4:  # This response is only chosen an average of 25% of the time.
                response = input(name + ", are you sure about that? ")
                continue
        feel = re.search(r'(.*)\b(feel)\s(.*)', changed)  # Check for statements like "I feel..."
        feels = re.search(r'(.*)\b(feels)\s(.*)', changed)  # Check for statements like "It feels like..."
        if feel:
            if not negative:
                response = input("Tell me more about how you feel " + feel.group(3) + ".\n")
                continue
            if negative:
                response = input("Why don't you feel " + feel.group(3) + "?\n")
                continue
        if feels:
            if not negative:
                response = input("Why does it feel" + feels.group(3) + "?\n")
                continue
            if negative:
                response = input("Why doesn't it feel" + feels.group(3) + "?\n")
                continue
        want = re.search(r'(.*)\b(want)\s(.*)', changed)  # Check for statements like "I want..."
        if want:
            response = input("Do you think that's what most people want?\n")
            continue
        need = re.search(r'(.*)\b(need)\s(.*)', changed)  # Check for statements like "I need..."
        if need:
            response = input("What would it mean to you if you got " + need.group(3) + "?\n")
            continue
            
        # Note: the following few statements have first and second person flipped to account for the earlier flip
        general_reflection = re.search(r'(\Ayou\'re)(.*)', changed)  # Check if the user typed something like "I'm ..."
        if general_reflection:
            response = input("Why are you" + general_reflection.group(2) + "?\n")
            continue
        general_statement = re.search(r'(\Ayou)(.*)', changed)  # Check if the user typed something else like "I ..."
        if general_statement:
            response = input("Is there a reason that you" + general_statement.group(2) + "?\n")
            continue
        general_judgement = re.search(r'(\AI)(.*)', changed)  # Check if the user typed something else like "You ..."
        if general_judgement:
            response = input("What makes you think " + general_judgement.group(0) + "?\n")
            continue

    if response == changed:  # The user didn't say anything personal
        lower = changed.lower()
        if re.search(r'((.*\s)|(\A))(yes)|(yeah)|(no)|(nope)|((dis)?agree)((.*\s)|(\Z))', lower):  # Check for (dis)agreement
            response = input("Could you elaborate?\n")
            continue
        if re.search(r'((.*\s)|(\A))(maybe)|(perhaps)|(kinda)|(kind of)|(doubt)|(probably)((.*\s)|(\A))', lower):  # Check for hesitance
            response = input("Is there a reason you're not sure?\n")
            continue
        # Not sure what they said otherwise, so revert to default

    # For all other inputs:
    rand = random.randint(1, 5)  # Randomly choose which follow-up question to use, with a 25% chance each.
    if rand == 1:
        response = input("Do you think about that often?\n")
        continue
    if rand == 2:
        response = input(name + ", are you sure that's realistic?\n")
        continue
    if rand == 3:
        response = input("Do you think that's related to why " + subject + "?\n")
        continue
    if rand == 4:
        response = input("How does that make you feel?\n")

print("Have a nice day, " + name + ".")
