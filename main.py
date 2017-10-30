from scrapy import cmdline


# Added this main.py to debug the spider. Can be run from here instead of the command line if preferred.
# Output can be written to 'jsonlines', 'marshal', 'pickle', 'xml', 'json', 'csv', 'jl'

cmdline.execute("scrapy crawl rarbg -o torrentz.xml".split())
