__author__ = 'Pedro Sernadela sernadela@ua.pt'

'''
    Convert abstracts into annotations from the XML articles
'''

from os.path import isdir
from os import listdir
import xml.etree.ElementTree as ET
import requests
from os.path import exists
from os import makedirs
import re
from multiprocessing import Pool


INPUT_DIR = 'publications/'
OUTPUT_DIR = 'annotations/'
SERVICE = 'http://biodatacenter.ieeta.pt:7180/ctakes'


# return files from dir
def get_files_from_dir(args_input):
    input_files = []
    if isdir(args_input):
        for f in listdir(args_input):
            input_files.append(args_input + f)
    return input_files


def write_file(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()


def do_request(service, abstract_text, pub_id):

    try:
        headers = {'content-type': 'text/plain'}
        r = requests.post(service, data=abstract_text, headers=headers)
        pub_id_int = re.findall(r'\d+', pub_id)
        output_name = OUTPUT_DIR + pub_id_int[0] + '.ann'
        write_file(output_name, r.text)

    except requests.exceptions.RequestException:
        print 'FAIL: ' + output_name


def process(pub_file):
    # print "processing %d of %d" % (i, len(input_pubs))
    tree = ET.parse(pub_file)
    root = tree.getroot()
    # join abstracts of the same pub
    text = ''
    for abstract in root.findall('.//AbstractText'):
        if abstract.text is not None:
            text += abstract.text
    do_request(SERVICE, text.encode('utf-8'), pub_file)

if __name__ == '__main__':

    if not exists(OUTPUT_DIR):
        makedirs(OUTPUT_DIR)

    input_pubs = get_files_from_dir(INPUT_DIR)

    p = Pool(8)
    p.map(process, input_pubs)

