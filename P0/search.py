def spec_search(query):
    #% Initializing, getting index
    import pickle 
    [meta,vectorizer,corpus_indexed,feature_names] = pickle.load(open('index.p','rb'))
    
    #% Query processing
    from nltk.tokenize import word_tokenize
    import re
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    from nltk.stem import WordNetLemmatizer
    stopwords_english = set(stopwords.words("english"))
    porter_stemmer = PorterStemmer() 
    wordnet_lemmatizer = WordNetLemmatizer()
    
    letters_only = re.sub("[^a-zA-Z]", " ", query)     
    query_tokened = word_tokenize(letters_only.lower().decode('utf-8'))
    query_stopwords_removed = [w for w in query_tokened if not w in stopwords_english]
    query_stemmed = [porter_stemmer.stem(w) for w in query_stopwords_removed]
    query_lemmatized = [wordnet_lemmatizer.lemmatize(w) for w in query_stemmed]
    # Transform the query using TFIDF vectorizer
    query_indexed = vectorizer.transform([' '.join(query_lemmatized)])
    
    #% Indexing
    from sklearn.metrics.pairwise import cosine_similarity
    
    cosMat = cosine_similarity(query_indexed,corpus_indexed)
    
    
    # Find the top-5 most relevant specializations
    related_docs_indices = cosMat[0].argsort()[:-6:-1]
    print '\n\nThe index numbers for top-5 results are:'
    print '(Episode Number | Cosine Similarity)\n'
    spec = []
    prob = []
    for item in related_docs_indices:
        print 'Speciality:', meta.Specialization[item], '|', cosMat[0][item]
        spec.append(meta.Specialization[item])
        prob.append(cosMat[0][item])
    return spec, prob
