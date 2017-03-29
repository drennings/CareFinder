_________________________________________________________
Steps to perform search:
	
	1.	from search import spec_search
	2.	[spec,prob] = spec_search(query)

	output: top 5 most relevant specialization
_________________________________________________________
Example:
	1.	from search import spec_search
	2.	[spec,prob] = spec_search('mental disease')

	output:	
		Speciality: Psychiatry | 0.432053427632
		Speciality: Cardiology | 0.0

	in[1]:  spec
	Out[1]: [u'Psychiatry', u'Cardiology']

	in[2]:  prob
	Out[2]: [0.36418937590972561, 0.11353391535740698]
_________________________________________________________
Files:

meta.xlsx:	Names of specializations (each entry is same as a .txt file containing info on the specialization
.txt:		The titles of all .txt files containing info on the specialization must be present in the meta.xlsx file.

build_index.py:	Python code that builds an index with output stored as Pickle 'index.p'
index.p:	Doc-term index saved as Pickle
search.py:	Python code containing the search function which search the doc-term index for a given query.

 


		