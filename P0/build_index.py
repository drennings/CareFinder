#%% Load text
import pandas as pd
meta = pd.read_excel("meta.xlsx")
corpusLayer1 = []
corpusLayer2 = []
corpusLayer3 = []
print("File loading")

for spec in meta.Specialization:    
    with open(spec+'.txt', 'r') as myfile:
        corpusLayer1.append(myfile.read().replace('\n', ''))  
    with open(spec+'_links.txt', 'r') as myfile:
        corpusLayer2.append(myfile.read().replace('\n', ''))  
    with open(spec+'_furtherLinks.txt', 'r') as myfile:
        corpusLayer3.append(myfile.read().replace('\n', ''))  

#%% Tokenize
from nltk.tokenize import word_tokenize
import re
corpus_tokenized_Layer1 = []
corpus_tokenized_Layer2 = []
corpus_tokenized_Layer3 = []
print("Tokenizing")

for spec in corpusLayer1:
    letters_only = re.sub('[^a-zA-Z]+', ' ', spec)
    tokens = word_tokenize(letters_only.lower())
    corpus_tokenized_Layer1.append(tokens)
for spec in corpusLayer2:
    letters_only = re.sub('[^a-zA-Z]+', ' ', spec)
    tokens = word_tokenize(letters_only.lower())
    corpus_tokenized_Layer2.append(tokens)
for spec in corpusLayer3:
    letters_only = re.sub('[^a-zA-Z]+', ' ', spec)
    tokens = word_tokenize(letters_only.lower())
    corpus_tokenized_Layer3.append(tokens)
    
#%% Remove stopwords
from nltk.corpus import stopwords
stopwords_english = set(stopwords.words("english"))
corpus_stopwords_removed_Layer1 = []
corpus_stopwords_removed_Layer2 = []
corpus_stopwords_removed_Layer3 = []
print("Removing stopwords")

for spec_tokenized in corpus_tokenized_Layer1:
    words = [w for w in spec_tokenized if not w in stopwords_english]
    corpus_stopwords_removed_Layer1.append(words)
for spec_tokenized in corpus_tokenized_Layer2:
    words = [w for w in spec_tokenized if not w in stopwords_english]
    corpus_stopwords_removed_Layer2.append(words)
for spec_tokenized in corpus_tokenized_Layer3:
    words = [w for w in spec_tokenized if not w in stopwords_english]
    corpus_stopwords_removed_Layer3.append(words)    
#%% Stemming
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

corpus_stemmed_Layer1 = []
corpus_stemmed_Layer2 = []
corpus_stemmed_Layer3 = []
print("Stemming/Lemmatizing")

for spec_stopwords_removed in corpus_stopwords_removed_Layer1:
    words=[]
    words = [wordnet_lemmatizer.lemmatize(w) for w in spec_stopwords_removed]
    corpus_stemmed_Layer1.append(words)
for spec_stopwords_removed in corpus_stopwords_removed_Layer2:
    words=[]
    words = [wordnet_lemmatizer.lemmatize(w) for w in spec_stopwords_removed]
    corpus_stemmed_Layer2.append(words)
for spec_stopwords_removed in corpus_stopwords_removed_Layer3:
    words=[]
    words = [wordnet_lemmatizer.lemmatize(w) for w in spec_stopwords_removed]
    corpus_stemmed_Layer3.append(words)
#%% Join words in the same episode as a long string
corpus_result_Layer1 = []
corpus_result_Layer2 = []
corpus_result_Layer3 = []

print("Join words into single document")

for spec_lemmatized in corpus_stemmed_Layer1:
    corpus_result_Layer1.append(' '.join(spec_lemmatized))
for spec_lemmatized in corpus_stemmed_Layer2:
    corpus_result_Layer2.append(' '.join(spec_lemmatized))
for spec_lemmatized in corpus_stemmed_Layer3:
    corpus_result_Layer3.append(' '.join(spec_lemmatized))   
#% Build term-document matrix
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer1 = TfidfVectorizer()
vectorizer2 = TfidfVectorizer()
vectorizer3 = TfidfVectorizer()
print("Term-document matrix")

corpus_indexed_Layer1 = vectorizer1.fit_transform(corpus_result_Layer1)
corpus_indexed_Layer2 = vectorizer2.fit_transform(corpus_result_Layer2)
corpus_indexed_Layer3 = vectorizer3.fit_transform(corpus_result_Layer3)


feature_names_Layer1 = vectorizer1.get_feature_names()
feature_names_Layer2 = vectorizer2.get_feature_names()
feature_names_Layer3 = vectorizer3.get_feature_names()

#% store data
print("Data storage")
import pickle
pickle.dump([meta,vectorizer1,corpus_indexed_Layer1,feature_names_Layer1], open('index_Layer1.p','wb'))
pickle.dump([meta,vectorizer2,corpus_indexed_Layer2,feature_names_Layer2], open('index_Layer2.p','wb'))
pickle.dump([meta,vectorizer3,corpus_indexed_Layer3,feature_names_Layer3], open('index_Layer3.p','wb'))
