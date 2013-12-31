#!/usr/bin/env python

import json
import hashlib
import logging
from datetime import datetime
import grequests
from redis import StrictRedis
from pythropod import pythropod


def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.CRITICAL)

    pool = grequests.Pool(20)
    # t = {'id':666, 'type':'text', 'text':'Portland','url':'http://fourletterlife.com'}
    # p = pythropod.Pythropod(t, test_finished, pool)
    # p.run()

    r = StrictRedis()
    while True:
        logging.info("Waiting for a test...")
        test = r.brpop('test_queue')[1]
        t = json.loads(test)

        if 'scheduled' in t and t['scheduled']:
            r.srem('scheduled_tests', t['id'])

        logging.info("Running test {}".format(t['id']))
        p = pythropod.Pythropod(t, test_finished, pool)
        p.run()
        r.srem('tests_in_queue', t['id'])


def test_finished(results):
    r = StrictRedis()
    # only take one screenshot of a url at a time
    if r.sismember('pending_screenshots', results['url']):
        filename = r.get('pending_screenshot_{}'.format(results['url']))
    else:
        hash = hashlib.sha1(str(results['id']) + str(datetime.now())).hexdigest()
        filename = hash + '.jpg'
        screenshot_info = {'url': results['url'], 'filename': filename}
        r.sadd('pending_screenshots', results['url'])
        r.set('pending_screenshot_{}'.format(results['url']), filename)
        r.lpush('pending_screenshot_blocked_list', 'x')
    
    results['screenshot'] = filename

    r.lpush('test_results', json.dumps(results))
    logging.info("Test {} complete".format(results['id']))

    

if __name__ == "__main__":
    main()