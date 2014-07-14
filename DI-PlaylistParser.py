#!/usr/bin/env python

import urllib2
import json
import sys
import argparse
import ConfigParser
import io

# Mapping of premium URLs
urls_prem = {'di': {'aac': {}, 'mp3': {}}, 'sky': {'aac': {}, 'mp3': {}}}
urls_prem['di']['aac'][40] = 'http://listen.di.fm/premium_low'
urls_prem['di']['aac'][64] = 'http://listen.di.fm/premium_medium'
urls_prem['di']['aac'][128] = 'http://listen.di.fm/premium'
urls_prem['di']['mp3'][256] = 'http://listen.di.fm/premium_high'
urls_prem['sky']['aac'][40] = 'http://listen.sky.fm/premium_low'
urls_prem['sky']['aac'][64] = 'http://listen.sky.fm/premium_medium'
urls_prem['sky']['aac'][128] = 'http://listen.sky.fm/premium'
urls_prem['sky']['mp3'][256] = 'http://listen.sky.fm/premium_high'

# Mapping of free URLs
urls_free = {'di': {'aac': {}, 'mp3': {}}, 'sky': {'aac': {}, 'mp3': {}}}
urls_free['di']['aac'][40] = 'http://listen.di.fm/public2'
urls_free['di']['aac'][64] = 'http://listen.di.fm/public1'
urls_free['di']['mp3'][96] = 'http://listen.di.fm/public3'
urls_free['sky']['aac'][40] = 'http://listen.sky.fm/public1'
urls_free['sky']['mp3'][96] = 'http://listen.sky.fm/public3'

itunes_header_strings = [
    "Name", "Artist", "Composer", "Album", "Grouping", "Genre", "Size", "Time",
    "Disc Number", "Disc Count", "Track Number", "Track Count", "Year",
    "Date Modified", "Date Added", "Bit Rate", "Sample Rate",
    "Volume Adjustment", "Kind", "Equalizer", "Comments", "Plays",
    "Last Played", "Skips", "Last Skipped", "My Rating", "Location"]


def get_url(args):
    '''Determine the appropriate URL pull playlists from'''
    if args.key:
        url_map = urls_prem[args.source][args.codec]
        if not args.quality:
            args.quality = 128 if args.codec == 'aac' else 256
    else:
        if args.quality is None:
            args.quality = {('di', 'aac'): 64,
                            ('di', 'mp3'): 96,
                            ('sky', 'aac'): 40,
                            ('sky', 'mp3'): 96}[(args.source, args.codec)]
        url_map = urls_free[args.source][args.codec]
    return url_map[args.quality] if args.quality in url_map else None


def process_pls(channel, key):
    '''Parse the PLs playlist from a JSON channel object'''
    url = channel['playlist']
    if key:
        url += '?%s' % key
    pls_raw = urllib2.urlopen(url).read()
    pls_config = ConfigParser.SafeConfigParser()
    pls_config.optionxform = str
    pls_config.readfp(io.BytesIO(pls_raw))
    return pls_config


def main():
    parser = argparse.ArgumentParser(
        description='Extract DI.fm or SKY.fm playlists into different formats')
    parser.add_argument('-s', '--source', default='di', choices=['di', 'sky'],
                        help='Playlist source, DI.fm or SKY.fm.  "\
                        "Default: "di"')
    parser.add_argument('-c', '--codec', default='aac', choices=['mp3', 'aac'],
                        help='Audio codec.  Default: "aac"')
    parser.add_argument('-q', '--quality', choices=[40, 64, 128, 96, 256],
                        type=int, help='Bitrate in kbps.  Default: highest "\
                        "possible given codec and free / premium constraints.')
    parser.add_argument('-k', '--key', help='Your premium Listen Key.')
    parser.add_argument('-f', '--format', choices=['pls', 'exaile', 'itunes'],
                        default='pls',
                        help='Playlist file format.  Default: "pls"')
    parser.add_argument('-l', '--long', action='store_true',
                        default=False, help='Use the full channel title for "\
                        "the filename instead of the short name, e.g. "\
                        ""Digitally Imported - Drum \'n Bass.pls" instad of "\
                        ""drumandbass.pls".  Only valid for "pls" format "\
                        "since exaile" format always uses the long name.')
    args = parser.parse_args()

    url = get_url(args)
    print('Source  : %s.fm' % args.source.swapcase())
    print('Codec   : %s' % args.codec.swapcase())
    print('Bitrate : %dkbps' % args.quality)
    print('Key     : %s' % args.key)
    print('URL     : %s' % url)
    print('')

    if not url:
        print('Playlists not available for the specified source, codec, and '
              'quality.')
        return 1

    print('Retrieving JSON playlist info...')
    channels = json.load(urllib2.urlopen(url))

    # Default PLS Format
    if args.format == 'pls':
        get_title = lambda pls: pls.get('playlist', 'Title1')
        for c in channels:
            print('%s' % c['name'])
            pls = process_pls(c, args.key)
            filename = '%s.pls' % (get_title(pls) if args.long else c['key'])
            with open(filename, 'wb') as f:
                pls.write(f)

    # Format for the exaile media player
    elif args.format == 'exaile':
        all_stations = []
        for c in channels:
            print('%s' % c['name'])
            pls = process_pls(c, args.key)
            title = pls.get('playlist', 'Title1')
            filename = '%s.playlist' % title
            all_stations.append(title)
            n = int(pls.get('playlist', 'NumberOfEntries'))
            with open(filename, 'w') as f:
                for i in range(1, n + 1):
                    f.write('%s\n' % pls.get('playlist', 'File%d' % i))
                f.write('EOF\n')
                f.write('shuffle_mode=S: disabled\n')
                f.write('repeat_mode=S: disabled\n')
                f.write('dynamic_mode=S: disabled\n')
                f.write('current_position=I: -1\n')
                f.write('name=U: %s\n' % title)
        print('Building order_file')
        with open('order_file', 'a') as fo:
            for name in all_stations:
                fo.write('%s\n' % name)
            fo.write('EOF')

    elif args.format == 'itunes':
        # The playlist file *must* have these columns tab-delimited in the
        # correct order
        output = "%s\n" % "\t".join(itunes_header_strings)

        # Add each channel to the output with 26 tabs between the name and
        # location URL
        for c in sorted(channels, key=lambda x: x['name']):
            pls = process_pls(c, args.key)
            title = pls.get('playlist', 'Title1')
            url = pls.get('playlist', 'File1')
            output += "%s%s%s\n" % (c['name'], "\t"*26, url)

        # Write the filename depending on the source
        if args.source == "di":
            filename = "Digitally Imported.txt"
        elif args.source == "sky":
            filename = "SKY.FM.txt"
        else:
            filename = "Radio Playlist.txt"

        # Write the iTunes playlist text file
        # NOTE: SKY.FM has some peculiar unicode characters in some of their
        # stream titles.
        with open(filename, 'wb') as f:
            f.write(output.encode('utf-8'))

        print("In iTunes, go to File > Library > Import Playlist and choose "
              "%s from this directory." % filename)

    return 0

if __name__ == '__main__':
    sys.exit(main())
