# Given a name how can we rate that person?

The general approach should be to retrieve as much information on the doctor's specialization as possible.
With this information we could be able to give an overview about the expertise a doctor has in a given field.

## Available information / interfaces

### NCBI database
The search function on this site allows to search for authors and returns publications.
There is also an API available:
https://www.ncbi.nlm.nih.gov/books/NBK25497/

### clinicaltrials.gov/
This site is a DB for clinical trials.
Information that might be relevant for us, are the names of the doctors leading a trial and related publications.

Supported Interfaces are:
- direct access to the DB 
https://aact-prod.herokuapp.com/
- use url request to return records in XML 
https://clinicaltrials.gov/ct2/resources/download#UseURL

### Google Scholar
scholar.google.com has actually many publications in the field of medicine,
but it seems more difficult to identify relevant information.

### private hospitals
http://www.hopkinsmedicine.org/
shows research from their own hospitals, it only includes 4 and is available through their web search interface - no API

### List of databases

https://en.wikipedia.org/wiki/List_of_academic_databases_and_search_engines
shows a list of academic DBs, including medicine. 
There are a number of journals that require a subscription, but I haven't checked them all out yet.

## Important questions

Does more publications in a field mean a doctor is a better practitioner in that field? Maybe he is only good at theory.

Also, is a doctor without any scientific publications a 'less good' practitioner?

If we answer the above questions with no, can we still rate doctors that way?
