import json

from pythropod import pythropod

def main():
    # todo get queued tests out of redis
    tests = [
        '{"url":"http://dhwebco.com", "type":"text"}'
    ]

    for test in tests:
        t = json.loads(test)
        p = pythropod.Pythropod(t)
        p.run()

if __name__ == "__main__":
    main()