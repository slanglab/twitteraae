# -*- encoding: utf-8 -*-
# actually that encoding line is NOT important codewise. only for doc purposes.
import re,sys

assert sys.maxunicode >= 0x10ffff, """This appears to be a UCS-2 build of python. We requires UCS-4 or a smarter newfangled one. (This code could be changed to support UCS-2 with some work.)
See:
http://stackoverflow.com/questions/26568722/remove-unicode-emoji-using-re-in-python
http://stackoverflow.com/questions/1446347/how-to-find-out-if-python-is-compiled-with-ucs-2-or-ucs-4
"""

# How unicode works
# There are 17 planes.  Each of which has 65536 codepoints.
# Within a plane, there are a number of blocks with variable sizes.  From size
# 16 to 65536.

# The three planes which I guess are most used today:
# 00000--0ffff : Basic Multilingual Plane
# 10000--1ffff : Supp. Multilingual Plane
# 20000--2ffff : Supp. Ideographic Plane. Includes part of CJK.
# there are also 14 other higher planes which are weird and not really used.

# Attempt 1: list out the interesting blocks.
# Turns out this is a bad approach since there are too many.
# https://en.wikipedia.org/wiki/Emoji#Unicode_blocks
# https://en.wikipedia.org/wiki/Miscellaneous_Symbols_and_Pictographs
# u'\U0001f300-\U0001F5FF' + # https://en.wikipedia.org/wiki/Miscellaneous_Symbols_and_Pictographs U+1F300..U+1F5FF
# u'\U0001f900-\U0001f9ff' + # https://en.wikipedia.org/wiki/Supplemental_Symbols_and_Pictographs U+1F900..U+1F9FF


# Attempt 2: just kill the entire Supplementary Multilingual Plane,
# some extra planes,
# and various blocks and special cases within the Basic Multilingual Plane.

# https://en.wikipedia.org/wiki/Plane_(Unicode)#Supplementary_Multilingual_Plane
# The SMP contains emoji and other symbols.  Besides that, it's mostly ancient
# languages like Egyptian hieroglyphics, or obscure modern things like the
# Mormon Church's attempt to reform English orthography.
# (The 93 blocks listed in the wikipedia page are fun to read through.)

JUNK_RE = (
u'[' +
    # Supplemental Multilingual Plane
    u'\U00010000-\U0001ffff' +

    # The weird extra planes
    u'\U00030000-\U0010ffff' +

    # E000–EFFF private use area,since I noticed \ue056 (doesnt display for me)
    u'\U0000e000-\U0000efff' +

    # There's a bunch of symbol blocks in the BMP here:
    # https://en.wikibooks.org/wiki/Unicode/Character_reference/2000-2FFF
    # Box Drawing
    # Box Elements
    # Miscellaneous Symbols
    # Dingbats
    # Miscellaneous Mathematical Symbols-A
    # Supplemental Arrows-A
    # Braille Patterns
    # Supplemental Arrows-B
    # Miscellaneous Mathematical Symbols-B
    # Supplemental Mathematical Operators
    # Miscellaneous Symbols and Arrows
    # e.g. \ue056  ✌

    u'\U00002500-\U00002bff' +

    # zero-width space, joiner, nonjoiner .. ZW Joiner is mentioned on Emoji wikipedia page
    # omg the ZWJ examples are downright non-heteronormative http://www.unicode.org/emoji/charts/emoji-zwj-sequences.html
    u'\U0000200B-\U0000200D' +

    # http://unicode.org/reports/tr51/
    # Certain emoji have defined variation sequences, where an emoji character can be followed by one of two invisible emoji variation selectors:
    # U+FE0E for a text presentation
    # U+FE0F for an emoji presentation
    u'\U0000fe0e-\U0000fe0f' +

u']+')

# Add optional whitespace. Because we want
# 1. A symbol surrounded by nonwhitespace => change to whitespace
# 2. A symbol surrounded by whitespace => no extra whitespace
# the current rule is too aggressive: also collapses pre-existing whitespace.
# this is ok for certain applications including ours.
SUB_RE = re.compile( r'\s*' + JUNK_RE + r'\s*', re.UNICODE)

def clean_emoji_and_symbols(text):
    assert isinstance(text, unicode), "Please pass in argument as unicode. This function will return unicode."
    ws_replace = SUB_RE.sub(u" ",text)
    # assert isinstance(ws_replace, unicode)
    return ws_replace

def test1():

    def run(s):
        print "INPUT REPR"
        print repr(s)
        print "INPUT RAW"
        print s.encode("utf8")

        out = clean_emoji_and_symbols(s)
        print "OUTPUT REPR"
        print repr(out)
        print "OUTPUT RAW"
        print out.encode("utf8")

    print "Assuming you have a good utf8-enabled terminal. tmux/screen might interfere."
    s = u'\U0001f60a ((: ^__^ (= ^-^ :)))) \U0001f601 \U0001f44d \ue056 :-)) \U0001f609 \u270c \n'
    run(s)

def test2():
    for line in sys.stdin:
        x = line.strip()
        x = x.decode("utf8")
        y = clean_emoji_and_symbols(x)
        if x==y:
            print "SAME\t" + x.encode("utf8")
        else:
            print "CHANGE\n\t%s\n\t%s" % (x.encode("utf8"), y.encode("utf8"))


if __name__=='__main__':
    # test1()
    test2()
