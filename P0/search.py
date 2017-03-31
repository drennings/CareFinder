#def spec_search(query):
    #% Initializing, getting index
import pickle 
[meta1,vectorizer1,corpus_indexed1,feature_names1] = pickle.load(open('index_Layer1.p','rb'))
[meta2,vectorizer2,corpus_indexed2,feature_names2] = pickle.load(open('index_Layer2.p','rb'))
[meta3,vectorizer3,corpus_indexed3,feature_names3] = pickle.load(open('index_Layer3.p','rb'))
#%% Query processing
query="arm surgery"
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
stopwords_english = set(stopwords.words("english"))
wordnet_lemmatizer = WordNetLemmatizer()
letters_only = re.sub("[^a-zA-Z]", " ", query)     
query_tokened = word_tokenize(letters_only.lower())
query_stopwords_removed = [w for w in query_tokened if not w in stopwords_english]
query_lemmatized = [wordnet_lemmatizer.lemmatize(w) for w in query_stopwords_removed]

# Transform the query using TFIDF vectorizer
query_indexed1 = vectorizer1.transform([' '.join(query_lemmatized)])
query_indexed2 = vectorizer2.transform([' '.join(query_lemmatized)])
query_indexed3 = vectorizer3.transform([' '.join(query_lemmatized)])

#% Indexing
from sklearn.metrics.pairwise import cosine_similarity

cosMat1 = cosine_similarity(query_indexed1,corpus_indexed1)
cosMat2 = cosine_similarity(query_indexed2,corpus_indexed2)
cosMat3 = cosine_similarity(query_indexed3,corpus_indexed3)

weight1=1.0
weight2=0.3
weight3=0.3
   
related_docs_indices = cosMat1[0][:]


cosMat1[0][:]=(weight1*cosMat1[0][:]+weight2*cosMat2[0][:]+weight3*cosMat3[0][:])/(weight1+weight2+weight3)
 # Find the top-5 most relevant specializations
 
related_docs_indices = cosMat1[0].argsort()[:-6:-1]
print ('\n\nThe index numbers for top-5 results are:')
print ('(Episode Number | Cosine Similarity)\n')
spec = []
prob = []
for item in related_docs_indices:
    print( 'Speciality:', meta1.Specialization[item], '|', cosMat1[0][item])
    spec.append(meta1.Specialization[item])
    prob.append(cosMat1[0][item])
#return spec, prob
