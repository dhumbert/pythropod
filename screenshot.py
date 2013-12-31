#!/usr/bin/env python
import subprocess
import os
import logging
from redis import StrictRedis


def main():
    logging.basicConfig(level=logging.INFO)
    r = StrictRedis()
    while True:
        logging.info("Waiting for a screenshot...")
        # block if no screenshots
        r.brpop('pending_screenshot_blocked_list')[1]
        # get a pending screenshot
        url = r.spop('pending_screenshots')

        if url:
            pipeline = r.pipeline()
            pipeline.get('pending_screenshot_{}'.format(url))
            pipeline.delete('pending_screenshot_{}'.format(url))
            filename, _ = pipeline.execute()

            logging.info("Taking screenshot of {} to {}".format(url, filename))

            screenshot_path = os.path.join('/Users/dhumbert/Code/Projects/Misc/clementia/public/user/screenshots', filename)
            subprocess.Popen(['/usr/local/bin/phantomjs', 'screenshot.js', url, screenshot_path], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()


if __name__ == '__main__':
    main()