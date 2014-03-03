#!/usr/bin/env python

import urllib2
import json
import sys
import argparse
import ConfigParser
import io

def process_pls(channel, key=''):
    url = '%s?%s'%(channel['playlist'], key)
    print(url)
    pls_raw = urllib2.urlopen(url).read()
    pls_config = ConfigParser.SafeConfigParser()
    pls_config.optionxform = str
    pls_config.readfp(io.BytesIO(pls_raw))
    return pls_config
    

def main():
    parser = argparse.ArgumentParser(
        description='Extract DI.fm or SKY.fm playlists into different formats',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--url', default='http://listen.di.fm/premium',
                        help='URL containing all playlists')
    parser.add_argument('-k', '--key', default='', help='Your premium Listen Key.  It can be found in "Player Settings"')
    parser.add_argument('-f', '--format', choices=['pls', 'exaile'],
                        default='pls', help='Output format')
    parser.add_argument('-l', '--long', action='store_true',
                        default=False, help='Use the full channel title for the filename instead of the short name, e.g. "Digitally Imported - Drum \'n Bass.pls" instad of "drumandbass.pls".  Only valid for "pls" format since "exaile" format always uses the long name.')
    args = parser.parse_args()

    print('Retrieving JSON playlist info...')
    channels = json.load(urllib2.urlopen(args.url))

    # Shotcut to retrieve channel title

    # Default PLS Format
    if args.format == 'pls':
        get_title = lambda pls: pls.get('playlist', 'Title1')
        for c in channels:
            print('%s' % c['name'])
            pls = process_pls(c, args.key)
            filename = '%s.pls'%(get_title(pls) if args.long else c['key'])
            with open(filename, 'wb') as f:
                pls.write(f)

    # Format for the exaile media player
    elif args.format == 'exaile':
        all_stations = []
        for c in channels:
            print('%s' % c['name'])
            pls = process_pls(c, args.key)
            title = pls.get('playlist', 'Title1')
            filename = '%s.playlist'%title
            all_stations.append(title)
            n = int(pls.get('playlist', 'NumberOfEntries'))
            with open(filename, 'w') as f:
                for i in range(1, n + 1):
                    f.write('%s\n'%pls.get('playlist', 'File%d' % i))
                f.write('EOF\n')
                f.write('shuffle_mode=S: disabled\n')
                f.write('repeat_mode=S: disabled\n')
                f.write('dynamic_mode=S: disabled\n')
                f.write('current_position=I: -1\n')
                f.write('name=U: %s\n'%title)
        print('Building order_file')
        with open('order_file', 'a') as fo:
            for name in all_stations:
                fo.write('%s\n'%name)
            fo.write('EOF')
    return 0

if __name__ == '__main__':
    sys.exit(main())
