#%% Load text
import pandas as pd
meta = pd.read_excel("meta.xlsx")
corpus = []
for spec in meta.Specialization:    
    with open(spec+'.txt', 'r') as myfile:
        corpus.append(myfile.read().replace('\n', ''))  

#%% Tokenize
from nltk.tokenize import word_tokenize
import re
corpus_tokenized = []
for spec in corpus:
    letters_only = re.sub('[^a-zA-Z]+', ' ', spec)
    tokens = word_tokenize(letters_only.lower().decode('utf-8'))
    corpus_tokenized.append(tokens)
    
#%% Remove stopwords
from nltk.corpus import stopwords
stopwords_english = set(stopwords.words("english"))
corpus_stopwords_removed = []
for spec_tokenized in corpus_tokenized:
    words = [w for w in spec_tokenized if not w in stopwords_english]
    corpus_stopwords_removed.append(words)
    
#%% Stemming
from nltk.stem import PorterStemmer
porter_stemmer = PorterStemmer()    
corpus_stemmed = []
for spec_stopwords_removed in corpus_stopwords_removed:
    words = [porter_stemmer.stem(w) for w in spec_stopwords_removed]
    corpus_stemmed.append(words)

#%% Lemmatizing
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
corpus_lemmatized = []
for spec_stemmed in corpus_stemmed:
    words = [wordnet_lemmatizer.lemmatize(w) for w in spec_stemmed]
    corpus_lemmatized.append(words)

#%% Join words in the same episode as a long string
corpus_result = []
for spec_lemmatized in corpus_lemmatized:
    corpus_result.append(' '.join(spec_lemmatized))
    
#%% Build term-document matrix
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
corpus_indexed = vectorizer.fit_transform(corpus_result)
feature_names = vectorizer.get_feature_names()

#%% store data
import pickle
pickle.dump([meta,vectorizer,corpus_indexed,feature_names], open('index.p','wb'))
