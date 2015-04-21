__author__ = 'Pedro Sernadela sernadela@ua.pt'

'''
    Download xml articles from pubmed given an CSV PMID list
'''

import csv
import requests
from os.path import exists
from os import makedirs
from xml.sax.saxutils import unescape


INPUT_FILE = 'cardiology.csv'
OUTPUT_DIR = 'publications/'


def get_pub(pub_id):

    try:
        headers = {'Accept': 'application/xml', 'Accept-Charset': 'UTF-8'}
        query = 'https://www.ncbi.nlm.nih.gov/pubmed/'+pub_id+'?report=xml&format=text'
        r = requests.get(query, headers=headers)

        write_file(OUTPUT_DIR + pub_id+'.xml', unescape(r.text.encode('utf-8', 'ignore')))

    except requests.exceptions.RequestException:
        print 'FAIL:' + pub_id


def write_file(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()

if not exists(OUTPUT_DIR):
    makedirs(OUTPUT_DIR)

with open(INPUT_FILE, 'rb') as f_ids:
    reader = csv.reader(f_ids, delimiter='\t', quoting=csv.QUOTE_NONE)
    row_number = 0
    for row in reader:
        row_number += 1
        get_pub(row[0])
    print 'Total publications: ' + str(row_number)