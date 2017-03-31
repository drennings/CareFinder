import pickle 
import pandas as pd
import wikipedia
import re
import nltk
from nltk.tokenize import word_tokenize

terms=" "
with open ("terms.txt", "r") as myfile:
    terms = ' '.join([line.replace('\n', '') for line in myfile.readlines()])
    
letters_only = re.sub('[^a-zA-Z]+', ' ', terms)
words = letters_only.split()
words_no_rep =" ".join(sorted(set(words), key=words.index))

tokens = word_tokenize(words_no_rep.lower())

#%% Remove stopwords and lemmatize
from nltk.corpus import stopwords
stopwords_english = set(stopwords.words("english"))
tokens_no_stopwords = [w for w in tokens if not w in stopwords_english]
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
tokens_lemmatzed = [wordnet_lemmatizer.lemmatize(w) for w in tokens_no_stopwords]
#%% clean first layer
print("FIRST LAYER")
meta = pd.read_excel("meta.xlsx")
for spec in meta.Specialization[1:2]:
    print(spec)
    terms=" "
    with open (spec+".txt", "r") as myfile:
        termsFromFile = ' '.join([line.replace('\n', '') for line in myfile.readlines()])
    letters_only = re.sub('[^a-zA-Z]+', ' ', termsFromFile)
    tokens = word_tokenize(letters_only.lower())
    tokens_no_stopwords = [w for w in tokens if not w in stopwords_english]
    tokens_lemmatzed_file = [wordnet_lemmatizer.lemmatize(w) for w in tokens_no_stopwords]
    finalWords=[w for w in tokens_lemmatzed_file if w in tokens_lemmatzed]
    file = open(spec+".txt",'w') 
    file.write(re.sub("[^a-zA-Z]", " ", spec)) 
    file.write(" ") 
    file.write(re.sub("[^a-zA-Z]", " ", str(finalWords)))
print("SECOND LAYER")

#% clearn second layer
for spec in meta.Specialization[1:2]:
    print(spec)
    terms=" "
    with open (spec+"_links.txt", "r") as myfile:
        termsFromFile = ' '.join([line.replace('\n', '') for line in myfile.readlines()])
    letters_only = re.sub('[^a-zA-Z]+', ' ', termsFromFile)
    tokens = word_tokenize(letters_only.lower())
    tokens_no_stopwords = [w for w in tokens if not w in stopwords_english]
    tokens_lemmatzed_file = [wordnet_lemmatizer.lemmatize(w) for w in tokens_no_stopwords]
    finalWords=[w for w in tokens_lemmatzed_file if w in tokens_lemmatzed]
    #file = open("test.txt",'w') 
    
    file = open(spec+"_links.txt",'w') 
    file.write(" ") 
    file.write(re.sub("[^a-zA-Z]", " ", str(finalWords)))
#%
print("THIRD LAYER")

#% clearn third layer
for spec in meta.Specialization[:]:
    print(spec)
    terms=" "
    with open (spec+"_furtherLinks.txt", "r") as myfile:
        termsFromFile = ' '.join([line.replace('\n', '') for line in myfile.readlines()])
    letters_only = re.sub('[^a-zA-Z]+', ' ', termsFromFile)
    tokens = word_tokenize(letters_only.lower())
    tokens_no_stopwords = [w for w in tokens if not w in stopwords_english]
    tokens_lemmatzed_file = [wordnet_lemmatizer.lemmatize(w) for w in tokens_no_stopwords]
    finalWords=[w for w in tokens_lemmatzed_file if w in tokens_lemmatzed]
    #file = open("test.txt",'w') 
    file = open(spec+"_furtherLinks.txt",'w') 
    file.write(" ") 
    file.write(re.sub("[^a-zA-Z]", " ", str(finalWords)))
