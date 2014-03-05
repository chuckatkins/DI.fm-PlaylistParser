#DI.fm-PlaylistParser
```
usage: DI-PlaylistParser.py [-h] [-s {di,sky}] [-c {mp3,aac}]
                            [-q {40,64,128,96,256}] [-k KEY] [-f {pls,exaile}]
                            [-l]

Extract DI.fm or SKY.fm playlists into different formats

optional arguments:
  -h, --help            show this help message and exit
  -s {di,sky}, --source {di,sky}
                        Playlist source, DI.fm or SKY.fm. Default: "di"
  -c {mp3,aac}, --codec {mp3,aac}
                        Audio codec. Default: "aac"
  -q {40,64,128,96,256}, --quality {40,64,128,96,256}
                        Bitrate in kbps. Default: highest possible given codec
                        and free / premium constraints.
  -k KEY, --key KEY     Your premium Listen Key.
  -f {pls,exaile}, --format {pls,exaile}
                        Playlist file format. Default: "pls"
  -l, --long            Use the full channel title for the filename instead of
                        the short name, e.g. "Digitally Imported - Drum 'n
                        Bass.pls" instad of "drumandbass.pls". Only valid for
                        "pls" format since "exaile" format always uses the
                        long name.
```

#Usage Examples

## Downloading premium Digitally Imported playlists
```
[chuck@euclid tmp]$ python DI-PlaylistParser.py -k abc123def456abc123def456
Source  : DI.fm
Codec   : AAC
Bitrate : 128kbps
Key     : abc123def456abc123def456
URL     : http://listen.di.fm/premium

Retrieving JSON playlist info...
Psybient
Electropop
Underground Techno
Trance
Vocal Trance
...
Future Synthpop
Latin House
Oldschool Acid
Chiptunes
Sankeys Radio
[chuck@euclid tmp]$ ls
ambient.pls             drumandbass.pls         minimal.pls
bigroomhouse.pls        dubstep.pls             moombahton.pls
breaks.pls              eclectronica.pls        oldschoolacid.pls
chillhop.pls            electronicpioneers.pls  progressive.pls
chilloutdreams.pls      electro.pls             progressivepsy.pls
...
deeptech.pls            latinhouse.pls          undergroundtechno.pls
DI-PlaylistParser.py    liquiddnb.pls           vocalchillout.pls
discohouse.pls          liquiddubstep.pls       vocallounge.pls
djmixes.pls             lounge.pls              vocaltrance.pls
downtempolounge.pls     mainstage.pls
[chuck@euclid tmp]$ 
```

## Downloading premium SKY.fm MP3 playlists
```
[chuck@euclid tmp]$ python DI-PlaylistParser.py -k abc123def456abc123def456 -s sky -c mp3
Source  : SKY.fm
Codec   : MP3
Bitrate : 256kbps
Key     : abc123def456abc123def456
URL     : http://listen.sky.fm/premium_high

Retrieving JSON playlist info...
Smooth Jazz
Love Music
Top Hits
Relaxation
Solo Piano
...
Pop Punk
Ska
Jpop
Israeli Hits
Compact Discoveries
[chuck@euclid tmp]$ ls
60srock.pls              dreamscapes.pls         relaxation.pls
80sdance.pls             guitar.pls              relaxingexcursions.pls
80srock.pls              hardrock.pls            romantica.pls
90srnb.pls               hit60s.pls              rootsreggae.pls
altrock.pls              hit70s.pls              russiandance.pls
...
compactdiscoveries.pls   oldies.pls              urbanjamz.pls
country.pls              oldschoolfunknsoul.pls  vocalnewage.pls
dancehits.pls            pianojazz.pls           vocalsmoothjazz.pls
datempolounge.pls        poppunk.pls             world.pls
DI-PlaylistParser.py     poprock.pls
[chuck@euclid tmp]$
```

## Downloading free SKY.fm MP3 playlists
```
[chuck@euclid tmp]$ python DI-PlaylistParser.py -s sky -c mp3
Source  : SKY.fm
Codec   : MP3
Bitrate : 96kbps
Key     : None
URL     : http://listen.sky.fm/public3

Retrieving JSON playlist info...
...
```

## Downloading free low quality DI.fm MP3 playlists
```
[chuck@euclid tmp]$ python DI-PlaylistParser.py -s di -q 40
Source  : DI.fm
Codec   : AAC
Bitrate : 40kbps
Key     : None
URL     : http://listen.di.fm/public2

Retrieving JSON playlist info...
...
```

