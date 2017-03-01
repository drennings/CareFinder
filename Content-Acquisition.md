# Content Acquisition

## Content collection

## Important questions

- Does more publications in a field mean a doctor is a better practitioner in that field? Maybe he is only good at theory.

- Also, is a doctor without any scientific publications a 'less good' practitioner?

- If we answer the above questions with no, can we still rate doctors that way?


### Top-down vs Bottom-up approach

In general, there are two approaches to tackle the extraction of the information we need:

**Top-down:**
Look for people on websites —> extract field —> evaluate their experience in this field by e.g. papers.

**Bottom-up:**
Scan papers to extract people —> cluster papers to extract fields —> classify their experience in this field

We believe that the top-down approach is more suitable for our particular case and circumstances.
First of all, it will help us to separate concerns while building the system.
The group members can work much more independent as the process of finding people is not dependent on analyzing papers in the first place.
Therefore, we can split the task of 1. finding relevant people and 2. determining their experience, given a handful of examples.
Second of all, we believe that this approach will guide us more productively to satisfying results.

## Sources

### NCBI database
The search function on this site allows to search for authors and returns publications.
There is also an API available:
https://www.ncbi.nlm.nih.gov/books/NBK25497/

### clinicaltrials.gov
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

### Private hospitals
http://www.hopkinsmedicine.org/
shows research from their own hospitals, it only includes 4 and is available through their web search interface - no API

### List of databases

https://en.wikipedia.org/wiki/List_of_academic_databases_and_search_engines
shows a list of academic DBs, including medicine.
There are a number of journals that require a subscription, but I haven't checked them all out yet.
