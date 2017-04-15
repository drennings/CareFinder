#%% find specialism from query
def spec_search(query):
    #input:  string, query
    #output: specialization
    
    #% Initializing, getting index
    import pickle 
    [meta1,vectorizer1,corpus_indexed1,feature_names1] = pickle.load(open('index_Layer1p2.p','rb'))
    [meta2,vectorizer2,corpus_indexed2,feature_names2] = pickle.load(open('index_Layer2p2.p','rb'))
    [meta3,vectorizer3,corpus_indexed3,feature_names3] = pickle.load(open('index_Layer3p2.p','rb'))
    
    # Query processing
    
    from nltk.tokenize import word_tokenize
    import re
    from nltk.corpus import stopwords
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
    weight2=0
    weight3=1.0
       
    related_docs_indices = cosMat1[0][:]
    
    
    cosMat1[0][:]=(weight1*cosMat1[0][:]+weight2*cosMat2[0][:]+weight3*cosMat3[0][:])/(weight1+weight2+weight3)
     # Find the top-5 most relevant specializations
     
    related_docs_indices = cosMat1[0].argsort()[:-2:-1]
    #print ('\n\nThe index numbers for top-5 results are:')
    #print ('(Episode Number | Cosine Similarity)\n')
    spec = []
    prob = []
    for item in related_docs_indices:
        #print( 'Speciality:', meta1.Specialization[item], '|', cosMat1[0][item])
        spec.append(meta1.Specialization[item])
        prob.append(cosMat1[0][item])
        #print('You seek for care in the specialization: '+str(spec)[3:len(str(spec))-2])
    return spec

#%% define search function
def search(query):
    from Bio import Entrez
    Entrez.email = 'team17TUDELFT@hotmail.com'
    results = Entrez.read(Entrez.esearch(db='pubmed',sort='pub+date',retmax='31',retmode='xml',term=query))
    return results

#%% find specialization of a doctor
def specialization(author,affiliation):
    # import libraries
    import wikipedia
    import re
    from Bio.Entrez import efetch, read
    author = '"'+author+'"'
    
    # Find ID's for doctor + affiliation
    ids = []
    results = search('%s[AUTH] AND %s[AFFL]' % (author,affiliation))['IdList']
    for i in results:
        ids.append(i)    
    num_paper = len(ids)
    
    # get abstracts from list of ID's
    query_abstracts = ''
    keywords = []
    query_keywords = ''
    query_title = '' 
    for i in ids:
        xml_data = read(efetch(db='pubmed', id=i, retmode='xml'))
        try:
            abstract = xml_data['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']['AbstractText']
            query_abstracts = query_abstracts + str(abstract) + ' '
        except:
            print('Paper with ID: ' + i + ' has no abstract')
            
    #get keuywords from ID's     
        if xml_data['PubmedArticle'][0]['MedlineCitation']['KeywordList'] != []:
            for x in xml_data['PubmedArticle'][0]['MedlineCitation']['KeywordList'][0] :
                keywords.append(str(re.sub("[^a-zA-Z]", " ", x)))
                query_keywords = query_keywords + x + ' '   
                
    #get paper titel from ID's
        try:
            query_title = query_title + ' ' + xml_data['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle']
        except:
            print('Paper with ID: ' + i + ' has no title')
     
    # get wiki pages first sentence of keywords
    query_wiki = ''
    for keyword in keywords:
        try:
            page = wikipedia.summary(keyword,sentences = 1)
            query_wiki = query_wiki + ' ' + str(re.sub("[^a-zA-Z]", " ", page))
        except:
            print('Disambiguation error for keyword: '+keyword+', action: keyword excluded')
        
    
    # find specialism
    corpus = query_abstracts + ' ' + query_keywords + ' ' + query_wiki + ' ' + query_title 
    specialization = str(spec_search(corpus))
    
    if num_paper == 0:
        print('no papers found')
        specialization = []
    else:
        print('this doctor is specialized in: '+specialization)
    return specialization

#%% count number of papers for a doctor
def papers(author,affiliation):
    author = '"'+author+'"'
    num_paper = len(search('%s[AUTH] AND %s[AFFL]' % (author,affiliation))['IdList'])
    return num_paper

#%% build the doctor DataFrame
def build_doctor_dataframe():
    import pandas as pd  
    doctors = pd.read_excel('main_data.xlsx')         
        # Set name to [SURNAME INITIALS] [Kennedy JF]
    for j in range(0,len(doctors.Name)):
        name = doctors.Name[j]
        if name.find(',') != -1:
            name = name[0:name.find(',')]
            name = name.split()
            initials = ''
            for i in range(0,len(name)-1):
                initials = initials + name[i][0]
            doctors.loc[j,'Name'] = name[len(name)-1]+ ' '+initials
                
        # Get number of papers if number_of_papers = -1
    for i in range(0,10611):
        print(i)
        if doctors.Number_of_papers[i] == -1:
            if i>0 and doctors.Name[i]==doctors.Name[i-1]:
                doctors.loc[i,'Number_of_papers'] = doctors.loc[i-1,'Number_of_papers']
            else:
                p = papers(doctors.Name[i],'New York')
                if p == 31:
                    doctors.loc[i,'Number_of_papers'] = '30+'
                else:
                    doctors.loc[i,'Number_of_papers'] = p
        
        # Get specialization if spec = []        
        if str(doctors.Spec[i]) == []:
            spec = specialization(doctors.Name[i],'New York')
            if len(spec)>0:
                doctors.loc[i,'Spec'] = spec[3:len(spec)-2]
                
    doctors = doctors.sort('Number_of_papers', ascending=False)
    doctors = doctors.reset_index()
    doctors = doctors.drop('level_0', 1)  
    writer = pd.ExcelWriter('main_data.xlsx', engine='xlsxwriter')
    doctors.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    return

#%% distance calculator
def calculateDistance(originLat, originLong, destinationLat, destinationLong):
    from math import sin, cos, sqrt, atan2, radians
    from decimal import Decimal
    
    originLat = Decimal(radians(originLat))
    originLong = Decimal(radians(originLong))
    destinationLat = Decimal(radians(destinationLat))
    destinationLong = Decimal(radians(destinationLong))
    
    # PLEASE NOTE: Code strongly based upon http://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    R = 6371.0 # #Radius of the Earth from Wikipedia
	
    dlon = Decimal(destinationLong - originLong)
    dlat = Decimal(destinationLat - originLat)

    a = sin(dlat / 2)**2 + cos(originLat) * cos(destinationLat) * sin(dlon / 2)**2		# apply the haversine formula
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

#%% find your doctor (end product)
def find_doctor():
    import numpy as np
    from termcolor import colored
    import pandas as pd
    from geopy.geocoders import Nominatim     
    print colored("What is your problem?", 'green')
    query = raw_input()
        
    verification = 'n'
    while verification == 'n':
        print(" ")
        print colored("What is your address? Example: 175 5th Avenue New York City", 'green')
        address =  raw_input()
        geolocator = Nominatim()
        location = geolocator.geocode(address)
        print(" ")
        print colored("Is the following address correct?", 'green')
        print(" ")
        print colored(location,'blue')
        print(" ")
        print colored("Please enter y/n:", 'green')
        verification = raw_input()
    print(" ")
    print colored("In what range are you looking for care? Please enter a distance [km]", 'green')
    Range = float(raw_input())

    originLat = location.latitude
    originLong = location.longitude
    
    spec = spec_search(query)
    
    k = 0
    i = 0
    doctors = pd.read_excel('main_data.xlsx')
    pd.set_option('display.width', 1000)
    doctor_for_you = pd.DataFrame()
    doctor_for_you.loc[0, 'Name'] ='' 
    
    while k < 5 and i < len(doctors)-1:
        if doctors.loc[i,'Spec'] == spec[0] and not(doctors.Name[i] in str(doctor_for_you.Name)) and calculateDistance(originLat, originLong, doctors.lat[i], doctors.lon[i])<=Range:
            doctor_for_you.loc[k,'Name'] = doctors.Name[i]
            doctor_for_you.loc[k,'Affiliation'] = doctors.Hosp[i]
            doctor_for_you.loc[k,'Specialization'] = doctors.Spec[i]
            doctor_for_you.loc[k,'Distance'] = str(int(calculateDistance(originLat, originLong, doctors.lat[i], doctors.lon[i])))+" km"
            doctor_for_you.loc[k,'Number of papers found'] = str(doctors.Number_of_papers[i])
            k = k + 1
        i = i + 1
    if k == 0:
        print("We're sorry, no doctors found.")
    else:
        doctor_for_you.index = np.arange(1, len(doctor_for_you) + 1)
        print(doctor_for_you)    
        
    return