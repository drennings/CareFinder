#%% Building corpus
import pandas as pd
import wikipedia
import re
import nltk
from nltk.tokenize import word_tokenize

        


meta = pd.read_excel("meta.xlsx")
for spec in meta.Specialization[:]:
    print(spec)
    terms=" "
    with open (spec+"_links.txt", "r") as myfile:
        termsFromFile = ' '.join([line.replace('\n', '') for line in myfile.readlines()])
    newTerms=[]
    i = 0
    while i < len(termsFromFile):
        letter=termsFromFile[i]
        if(letter.isupper() ):
            if(termsFromFile[i+1].islower()):
                newTerms.append(" ")
            newTerms.append(letter)
        else:
            newTerms.append(letter)
        i+=1
    newTerms = ''.join(newTerms)
    file = open(spec+'_links.txt','w')
    file.write(newTerms)
    
        
        
        

        
        
