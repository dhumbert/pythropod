#!/usr/bin/env python

import json
import hashlib
import subprocess
import os
import logging
from datetime import datetime
import grequests
from redis import StrictRedis
from pythropod import pythropod


def main():
    logging.basicConfig(level=logging.INFO)

    pool = grequests.Pool(20)
    # t = {'id':666, 'type':'text', 'text':'Portland','url':'http://fourletterlife.com'}
    # p = pythropod.Pythropod(t, test_finished, pool)
    # p.run()

    r = StrictRedis()
    while True:
        logging.info("Waiting for a test...")
        test = r.brpop('test_queue')[1]
        t = json.loads(test)
        logging.info("Running test {}".format(t['id']))
        p = pythropod.Pythropod(t, test_finished, pool)
        p.run()


def test_finished(results):
    hash = hashlib.sha1(str(results['id']) + str(datetime.now())).hexdigest()
    filename = hash + '.jpg'
    screenshot_path = os.path.join('/Users/dhumbert/Code/Projects/Misc/clementia/public/user/screenshots', filename)
    subprocess.Popen(['/usr/local/bin/phantomjs', 'screenshot.js', results['url'], screenshot_path], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    results['screenshot'] = filename
    r = StrictRedis()
    r.lpush('test_results', json.dumps(results))
    logging.info("Test {} complete".format(results['id']))


if __name__ == "__main__":
    main()