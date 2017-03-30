The names.jl contains the output of the NER tool
The text.jl contains the corresponding text surrounding each name

To use the scraper install scrapy and json_lines via pip
then type $ scrapy crawl doctors -o names.jl
then $ scrapy crawl doctext -o text.jl