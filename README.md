#DI.fm-PlaylistParser
```
usage: DI-PlaylistParser.py [-h] [-u URL] -k KEY [-f {pls,exaile}]

Extract DI.fm or SKY.fm playlists into differnt formats

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL containing all playlists (default:
                        http://listen.di.fm/premium)
  -k KEY, --key KEY     Your premium Listen Key. It can be found in "Player
                        Settings" (default: None)
  -f {pls,exaile}, --format {pls,exaile}
                        Output format (default: pls)
```

#Usage Examples

## Downloading Digitally Imported playlists
```
[chuck@euclid tmp]$ python DI-PlaylistParser.py -k abc123def456abc123def456
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

## Downloading SKY.fm playlists
```
[chuck@euclid tmp]$ python DI-PlaylistParser.py -k abc123def456abc123def456 -u http://listen.sky.fm/premium
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
