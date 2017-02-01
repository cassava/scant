#!/usr/bin/env python3

import argparse
import subprocess
import pathlib
import os.path

parser = argparse.ArgumentParser(description='Convert high quality scans to lower quality PDFs.')
parser.add_argument('filenames', metavar='FILE', type=str, nargs='+',
                    help='input files to be converted')
parser.add_argument('-o', '--output', dest='output', type=str, default='output.pdf',
                    help='output PDF')
parser.add_argument('-p', '--profile', dest='profile', type=str, default='scan',
                    help='conversion profile [original, scan, high-contrast]')
parser.add_argument('-q', '--quality', dest='quality', type=str, default='l',
                    help='quality profile [original, xxs, xs, s, m, l, xl, xxl]')
parser.add_argument('--test-all', dest='testall', action='store_true',
                    help='try all the different settings, barring original')

def flatten(l):
    return [item for sublist in l for item in sublist]

def looks_like_pdf(filename):
    p = pathlib.PurePath(filename)
    return p.suffix == ".pdf"

def _convert(in_files, out_file, profile, quality):
    cmd = "convert"
    profiles = {
        'original': [],
        'scan':     ["-normalize", "-level", "10%,90%", "-sharpen", "0x1"],
        'highlight':["-normalize", "-selective-blur", "0x4+10%", "-level", "10%,90%", "-sharpen", "0x1", "-brightness-contrast", "0x25"],
    }
    qualities = {
        'original': [],
        'xl':       ["-depth", "8", "-quality", "50%", "-density", "300x300"],
        'l':        ["-resample", "50%", "-depth", "8", "-quality", "50%", "-density", "150x150"],
        'm':        ["-resample", "37%", "-depth", "8", "-quality", "50%", "-density", "111x111"],
        's':        ["-resample", "25%", "-depth", "8", "-quality", "50%", "-density", "75x75"],
        'xs':       ["-resample", "20%", "-depth", "8", "-quality", "50%", "-density", "60x60"],
        'xxs':      ["-resample", "15%", "-depth", "8", "-quality", "50%", "-density", "45x45"],
        'xxxs':     ["-resample", "10%", "-depth", "8", "-quality", "50%", "-density", "30x30"],
    }
    subprocess.run(flatten([[cmd], in_files, profiles[profile], qualities[quality], [out_file]]))

def convert(in_files, out_file, profile='scan', quality='high'):
    # Make sure all our input is okay
    if not looks_like_pdf(out_file):
        raise Exception("output file %s is not a PDF" % out_file)
    if os.path.exists(out_file):
        raise Exception("output file %s already exists" % out_file)
    for f in in_files:
        if not os.path.exists(f):
            raise Exception("input file %s does not exist" % f)

    print("Converting following files to ", out_file, ":", sep="")
    for f in in_files:
        print("\t", f)
    print("This may take a while...")
    _convert(in_files, out_file, profile, quality)
    print("Done.")

def compare(in_files, out_file, profiles=['scan', 'highlight'], qualities=['extreme', 'high', 'medium', 'low']):
    # Make sure all our input is okay
    if not looks_like_pdf(out_file):
        raise Exception("output file %s is not a PDF" % out_file)
    for f in in_files:
        if not os.path.exists(f):
            raise Exception("input file %s does not exist" % f)

    # Generate the different formats.
    for p in profiles:
        for q in qualities:
            # Change output filename
            out = "{} ({},{}).pdf".format(out_file[:-4], p, q)
            if os.path.exists(out):
                raise Exception("output file %s already exists" % out)
            print("Writing ", out, sep="", end="... ", flush=True)
            _convert(in_files, out, profile=p, quality=q)
            print("done.")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.testall:
        compare(args.filenames, args.output)
    else:
        convert(args.filenames, args.output, args.profile, args.quality)



