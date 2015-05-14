__author__ = 'Pedro Sernadela sernadela@ua.pt'

'''
    Convert radiology text reports into annotations from MIMIC2 DB
'''

import requests
from os.path import exists
from os import makedirs
from multiprocessing import Pool
import psycopg2
import psycopg2.extras
import uuid


DB = "host='biodatacenter.ieeta.pt' dbname='MIMIC2' user='' password='' port='7132'"
OUTPUT_DIR = 'mimic2ann/'
SERVICE = 'http://biodatacenter.ieeta.pt:7180/ctakes'


def write_file(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()


def do_request(service, abstract_text, pub_id):

    try:
        headers = {'content-type': 'text/plain'}
        r = requests.post(service, data=abstract_text, headers=headers)
        output_name = OUTPUT_DIR + pub_id + '.ann'
        write_file(output_name, r.text)

    except requests.exceptions.RequestException:
        print 'FAIL: ' + output_name


def process(text):
    do_request(SERVICE, text[0].encode('utf-8'), str(uuid.uuid4()))

if __name__ == '__main__':

    if not exists(OUTPUT_DIR):
        makedirs(OUTPUT_DIR)
    try:
        print "Connecting to database\n	->%s" % (DB)
        conn = psycopg2.connect(DB)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select text from mimic2v26.noteevents where category='RADIOLOGY_REPORT' AND charttime >= '3560-02-27 00:00:00.0'")
        records = cursor.fetchall()

        print "Getting annotations.."
        p = Pool(8)
        p.map(process, records)
        print "Done."
    except:
        print "unable to connect to the database"




