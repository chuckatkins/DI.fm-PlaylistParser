#!/usr/bin/env python

import urllib2
import json
import sys
import argparse
import ConfigParser
import io


def main():
    parser = argparse.ArgumentParser(
        description='Extract DI.fm or SKY.fm playlists into different formats',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--url', default='http://listen.di.fm/premium',
                        help='URL containing all playlists')
    parser.add_argument('-k', '--key', required=True, help='Your premium Listen Key.  It can be found in "Player Settings"')
    parser.add_argument('-f', '--format', choices=['pls', 'exaile'],
                        default='pls', help='Output format')
    args = parser.parse_args()

    print('Retrieving JSON playlist info...')
    result = json.load(urllib2.urlopen(args.url))

    for p in result:
        print('%s' % p['name'])
        pls_data = urllib2.urlopen('%s?%s' % (p['playlist'], args.key)).read()

        if args.format == 'pls':
            with open('%s.pls' % p['key'], 'w') as f:
                f.write(pls_data)

        elif args.format == 'exaile':
            parser = ConfigParser.SafeConfigParser()
            parser.readfp(io.BytesIO(pls_data))
            name = parser.get('playlist', 'Title1')
            n = int(parser.get('playlist', 'NumberOfEntries'))
            with open('%s.playlist' % name, 'w') as f:
                for i in range(1, n + 1):
                    f.write('%s\n' % parser.get('playlist', 'File%d' % i))
                f.write('EOF\n')
                f.write('shuffle_mode=S: disabled\n')
                f.write('repeat_mode=S: disabled\n')
                f.write('dynamic_mode=S: disabled\n')
                f.write('current_position=I: -1\n')
                f.write('name=U: %s\n' % name)
    return 0

if __name__ == '__main__':
    sys.exit(main())
