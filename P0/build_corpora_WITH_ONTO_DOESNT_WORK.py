#%% Building corpus
import pandas as pd
import wikipedia
import re
import pymedtermino
pymedtermino.LANGUAGE = "en"
pymedtermino.REMOVE_SUPPRESSED_CONCEPTS = True
from pymedtermino.all import *
import nltk
from nltk.tokenize import word_tokenize
import sqlite3
from sqlite3 import OperationalError

meta = pd.read_excel("meta.xlsx")
for spec in meta.Specialization:
    page = wikipedia.page(spec)
#    file = open(spec+'.txt','w') 
#    file.write(re.sub("[^a-zA-Z]", " ", page.title)) 
#    file.write(re.sub("[^a-zA-Z]", " ", page.content)) 
#   file = open(spec+'_links.txt','w')
#    for link in page.links:
#        linkPage=wikipedia.page(link)
#        file.write(re.sub("[^a-zA-Z]", " ", linkPage.title))
#        file.write(re.sub("[^a-zA-Z]", " ", linkPage.summary)) 
    page_tokenized = []
    letters_only = re.sub('[^a-zA-Z]+', ' ', page.title+" "+page.content)
    tokens = word_tokenize(letters_only.lower())
    page_tokenized.append(tokens) 
    file = open(spec+'_Ontology.txt','w') 
    for token in tokens: 
        concept=-1
        word=token.lower()+"*"
#        try:
        concept=SNOMEDCT.search(word)
#        except OperationalError:
#            continue
        if concept!=-1:
            file.write(re.sub("[^a-zA-Z]", " ", concept))


    
    #print concept    
    #file = open(spec+'_SNOMEDCT.txt','w')
    #file.write(re.sub("[^a-zA-Z]", " ", concept)) 
#for ancestor in concept.ancestors(): print ancestor:
    #print from 6th letter
#SNOMEDCT[80891009].associated_clinical_findings()
#SNOMEDCT[3424008].ancestors_no_double()
#SNOMEDCT[3424008].children
#SNOMEDCT[3424008].parents
#concept.INVERSE_has_definitional_manifestation
#concept.interprets