"""
    Spotify Now Playing Script
    Requires Python, Xchat, Spotify and DBus

    Dorian Harmans
    
    original by Erik Nosar - see https://github.com/enosar/xchat-spotify-np
    Script released under Public Domain
"""

__module_name__         = "xchat-spotify-np"
__module_version__      = "1.0"
__module_description__  = "Now playing script for Spotify for XChat on Linux"

import xchat
import dbus

bus = dbus.SessionBus()
def get_spoti():
    try:
        return bus.get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
    except DBusException:
        print "\x02Either Spotify is not running or you have something wrong with your D-Bus setup."
        return None

"""
Sample data contained from within the following dbus call:
    trackinfo = spotify.Get("org.mpris.MediaPlayer2.Player","Metadata")

dbus.Dictionary(
    {dbus.String(u'xesam:album'): dbus.String(u'A State Of Trance Episode 631', variant_level=1),
    dbus.String(u'xesam:title'): dbus.String(u'Daylight [ASOT 631] - Philippe El Sisi Remix', variant_level=1),
    dbus.String(u'xesam:trackNumber'): dbus.Int32(27, variant_level=1),
    dbus.String(u'xesam:artist'): dbus.Array([dbus.String(u'Jumpy Jumps')], signature=dbus.Signature('s'), variant_level=1),
    dbus.String(u'xesam:discNumber'): dbus.Int32(0, variant_level=1),
    dbus.String(u'mpris:trackid'): dbus.String(u'spotify:track:59PulgxMdbrXRA4ScxuHaJ', variant_level=1),
    dbus.String(u'mpris:length'): dbus.UInt64(251000000L, variant_level=1),
    dbus.String(u'mpris:artUrl'): dbus.String(u'http://open.spotify.com/thumb/98ce7987aa9944788ffdc50b8605a38f1e66de16', variant_level=1),
    dbus.String(u'xesam:autoRating'): dbus.Double(0.45, variant_level=1),
    dbus.String(u'xesam:contentCreated'): dbus.String(u'2013-01-01T00:00:00', variant_level=1),
    dbus.String(u'xesam:url'): dbus.String(u'spotify:track:59PulgxMdbrXRA4ScxuHaJ', variant_level=1)},
    signature=dbus.Signature('sv'), variant_level=1)

"""

def on_nowplaying(word, word_eol, userdata):

    # Get current channel and get latest track from Spotify
    spotify = get_spoti()
    context = xchat.get_context()
    trackinfo = spotify.Get("org.mpris.MediaPlayer2.Player","Metadata")

    # Get track information from DBus dictionary
    album       = trackinfo.get("xesam:album")
    title       = trackinfo.get("xesam:title")
    trackNumber = str(trackinfo.get("xesam:trackNumber"))
    discNumber  = str(trackinfo.get("xesam:discNumber"))
    trackid     = str(trackinfo.get("xesam:trackid"))
    length      = trackinfo.get("xesam:length")
    artUrl      = trackinfo.get("xesam:artUrl")
    url         = trackinfo.get("xesam:url")

    # The artist list is provided as an array. Combine all artists to a single string.
    artist = str(", ".join(trackinfo.get("xesam:artist"))).strip()

    npmsg = "is now playing: %s - %s [%s] (%s)" % (artist, title, album, url)
    xchat.command("me %s" % (npmsg))
    return xchat.EAT_ALL
xchat.hook_command("now", on_nowplaying, help="/now - Announce currently playing track in Spotify")
print "xchat-spotify-np plugin loaded"
