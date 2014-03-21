
# gutenberg.py
#
# Reformats and renames the downloaded etexts.
#
# Software by Michiel Overtoom, motoom@xs4all.nl, july 2009.
#

# <papna> Luyt: You could have title_prefix = "Title: " and do if line.startswith(title_prefix): line = line[len(title_prefix):]
# <Luyt> papna: Indeed, that'd get rid of that horrible 7.  It has happened to me before that I changed the prefix, and forgot to adjust the length too

import os
import re
import sys

# Repetive stuff I don't want to read a 1000 times on my eBook reader.
remove = ["Produced by","End of the Project Gutenberg","End of Project Gutenberg"]

def beautify(fn, ofn=None):
    ''' Reads a raw Project Gutenberg etext, reformat paragraphs,
    and removes fluff.  Determines the title of the book and uses it
    as a filename to write the resulting output text. '''
    lines = [line.strip() for line in open(fn)]
    collect = False
    lookforsubtitle = False
    outlines = []
    startseen = endseen = False
    title=""
    author=""
    release_date=""
    language=""
    character_set_encoding=""
    for line in lines:
        if line.startswith("Title: "):
            title = line[7:]
            lookforsubtitle = True
            continue
        if lookforsubtitle:
            if not line.strip():
                lookforsubtitle = False
            else:
                subtitle = line.strip()
                subtitle = subtitle.strip(".")
                title += ", " + subtitle
            print "Title:", title
            continue
        if line.startswith("Author: "):
            author = line[8:]
            print "Author:", author
            continue
        if line.startswith("Language: "):
            language = line[10:]
            print "Language:", language
            continue
        if line.startswith("Character set encoding: "):
            character_set_encoding = line[24:]
            print "Character set:", character_set_encoding
            continue

        if ("*** START" in line) or ("***START" in line):
            collect = startseen = True
            paragraph = ""
            continue
        if ("*** END" in line) or ("***END" in line):
            endseen = True
            break
        if not collect:
            continue
        if not line:
            paragraph = paragraph.strip()
            for term in remove:
                if paragraph.startswith(term):
                    paragraph = ""
            if paragraph:
                outlines.append(paragraph)
                outlines.append("")
            paragraph = ""
        else:
            paragraph += " " + line

    # Compose a filename.  Replace some illegal file name characters with alternatives.
    if ofn is None:
        ofn = title[:150] + ", " + fn
        ofn = ofn.replace("&", "en")
        ofn = ofn.replace("/", "-")
        ofn = ofn.replace("\"", "'")
        ofn = ofn.replace(":", ";")
        ofn = ofn.replace(",,", ",")

    # Report on anomalous situations, but don't make it a showstopper.
    if not title:
        print ofn
        print "    Problem: No title found\n"
    if not startseen:
        print ofn
        print "    Problem: No '*** START' seen\n"
    if not endseen:
        print ofn
        print "    Problem: No '*** END' seen\n"

    f = open(ofn, "wt")
    f.write("\n".join(outlines))
    f.close()

sourcepattern = re.compile("^[0-9]{4,5}\-[0-9]\.txt$")
#for fn in os.listdir("."):
#    if sourcepattern.match(fn):
#        beautify(fn)

rootdir = sys.argv[1]
max_count = int(sys.argv[2])
cur_count = 0
for root, subfolders, files in os.walk(rootdir):
    for filename in files:
        if filename.endswith(".txt") and not filename.startswith("out-"):
            file_path = os.path.join(root, filename)
            out_file_path = os.path.join(root, "out-"+filename)
            print file_path, "--->", out_file_path
            beautify(file_path, out_file_path)
            cur_count += 1
            if cur_count == max_count:
                exit()

