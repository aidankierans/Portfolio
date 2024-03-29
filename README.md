# Portfolio
A selection of my undergraduate classwork and extracurricular projects.

## Project Descriptions
### Sentiment Analysis
Written in Python in March, 2020 for my Intro to Natural Language Processing course at Virginia Commonwealth University. This program automatically analyzes the sentiment of tweets, e.g. to classify them as either "positive" or "negative" in tone. Using a Naive Bayes model trained on a set of tagged tweets, this program determines which sentiment is the most probable given the relative frequency of each sentiment in general, and the tokens (i.e. words and some punctuation) that appear in the tweet.

Detailed documentation regarding the Naive Bayes model and the implimentation can be found in sentiment.py. The other files in the folder are training and testing data for use with sentiment.py, a module for scoring the output, and example output files of the program.

### Word Sense Disambiguation
Written in Python in March, 2020, for my Intro to Natural Language Processing course at Virginia Commonwealth University. This program automatically performs word sense disambiguation (WSD) on instances of a word with only the context of a few sentences for each one, using a Naive Bayes model trained on a set of tagged sentences. WSD is necessary because of homonyms and homographs; two words can have the same spelling, but different meanings, and only context can distinguish them. In this case, the context for each instance of a word is used to compute which meaning/sense is the most probable given the relative frequency of each sense in general, and the important parts of the context.

Detailed documentation regarding the Naive Bayes model and the implimentation can be found in wsd.py. The other files in the folder are training and testing data for use with wsd.py, a module for scoring the output, and example output files of the program.

### Sentence Generation Using N-grams 
Written in Python in February, 2020, for my Intro to Natural Language Processing course at Virginia Commonwealth University. This program generates sentences using statistical data about the orders in which words are used, without any understanding of the words' meaning. Language is complicated and always evolving, so it's easier to generate somewhat plausible sounding text by looking at which words follow which other words than it is to construct a complete logical representation of how we communicate. This program uses the n-gram model to collect these statistics.

Detailed documentation regarding the n-gram model, usage instructions, etc. are in ngram.py. The other files in the folder are the data that were used to train the ngram model; they are Anna Karenina by Leo Tolstoy (1399-0.txt), Crime and Punishment by Fyodor Dostoevsky (2554-0.txt), and War and Peace by Leo Tolstoy (2600-0.txt). Some information, such as each text's table of contents, has been removed to reduce noise.

### eliza.py
Written in Python in February, 2020, for my Intro to Natural Language Processing course at Virginia Commonwealth University. This program simulates a teletype-based conversation with a Rogerian-style psychotherapist named Eliza, based on the 1966 program written by Joseph Weizenbaum towards the same end. The Rogerian style of psychotherapy mostly involves turning the client's statements into probing questions, so they can talk themselves to a solution. This can be accomplished by a computer program that simply modifies sentences according to predefined patterns, without any idea of meaning attached to the words by the program. Detailed documentation on how the program works can be found in the file itself.

### Animal Shelter Database
This was a group project for my Database Theory class in the fall semester of 2019. The project report is something we worked on together, which I've included because it goes into detail about the purpose and design of the database, but the ER Diagram and the .sql files are my own work (not including the population of the tables with data). For the sake of full disclosure, my team members also helped define the requirements and built a front-end application I did not include here. 

The project required us to upload the database to Google Cloud Platform so that we could attach it to a web application, so to make that possible, the dump file contains only the definition and population of the schemas and their constraints, and can be loaded using MySQL's import tool. After importing the dump file, to see/add the remaining components, including the users, privileges, triggers, and procedures, set "shelter" (without quotes) for use as the default database, then copy the contents of \_Run_after_import_of_dump.sql and paste them into the GCP console. 
 
### Forming Clusters As Needed 
Written in Java in November, 2019. A detailed project report and requirements document can be found in the project folder, but the general purpose of the project is to sort sentences/"documents" according to their similarity, using the Forming Clusters As Needed unsupervised learning algorithm. This kind of task could be applied to an Information Retrieval setting, like organizing a document or website database to make it searchable, without too much difficulty. The output of my code as it's currently written is optimized for precision more than for recall, so the few clusters that were chosen were groups of sentences that met a high threshold for similarity.

### Efficient_Critical_Definitions.sage
I wrote this code in Sage in May of 2019, and optimized it over the course of the graph theory research project so that we could efficiently iterate through large sets of graphs and find the ones we cared about. 

Post Mortem: It was my first time using Python and Sage, as well as gt.sage (a library of graph theory objects and functions that my program assumes is already loaded). If I were to write it again today, I'd look into Cythonizing it to speed it up further, although it served its purpose as-is well enough at the time.  

### CSV Data Imputation
I wrote this code in Python in September of 2019 for CMSC 435: Intro to Data Science. The purpose of the program is to take three csv files—one missing 5% of the values, one missing 20% of the values, and one that isn't missing values for comparison—and impute (fill in) the missing values using various methods.

Post Mortem: This was the second program I wrote in Python, and the first time I used pandas, so I'm proud of what I was able to accomplish despite the optimizations to the program that I'm sure could be made. To start, I believe hot_deck() would benefit from being Cythonized, as well as distance(); the program reaches a CPU bottleneck in that area that contributes to the vast majority of the processing time. For the same reason I would also implement distance() using Python or Numpy arrays rather than pandas Series objects, and avoid most of the nesting for loops in favor of an operation applied to the whole Data Frame at once if possible. By the time I learned about these possible optimizations, the program was in the testing phase and I didn't have time to start over and learn how to do things differently, but I at least know now where to start when implementing a computationally intense algorithm like this in the future.
