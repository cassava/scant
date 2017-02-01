#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Morgan <neembi@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import argparse
import subprocess
import pathlib
import os.path

class Geometry:
    def __init__(self, w, h, x=0, y=0):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def __print__(self):
        return "{}x{}+{}+{}".format(self.w, self.h, self.x, self.y)

def std_geometry(s):
    return {
        'a4': Geometry(210, 297),
        'a5': Geometry(148, 210),
        'letter': Geometry(215.9, 279.4)
    }[s]

class Scanner:
    def __init__(self, device, resolution=300, size=None):
        self.device = device
        self.resolution = resolution
        self.size = size

        # TODO: Should I initialize these in __init__ or in
        # the class itself?
        self.path = 'scanimage'
        self.format = 'png'
        self.mode = 'Color'

    def scan(self, filename, size=None, resolution=None, mode=None):
        # Catch default values
        if size is None:
            size = self.size
        if resolution is None:
            resolution = self.resolution
        if mode is None:
            mode = self.mode

        # Add the extension if the filename does not already have it.
        base, ext = os.path.splitext(filename)
        if ext != (".%s" % self.format):
            filename += (".%s" % self.format)

        # Build the command
        cmd = [self.path,
            '--device-name', self.device,
            '--format', self.format,
            '--resolution', str(resolution),
            '--mode', mode]
        if size is not None:
            cmd.extend(['-x', str(size.w), '-y', str(size.h)])

        # Open output file and run the command.
        if os.path.exists(filename):
            raise Exception("output file %s already exists" % filename)
        with open(filename, "w") as outfile:
            subprocess.run(cmd, stdout=outfile, check=True)

def flatten(l):
    return [item for sublist in l for item in sublist]

parser = argparse.ArgumentParser(description='Scan documents from scanner')
parser.add_argument('-d', '--device', dest='device', type=str, default='epson2:net:192.168.178.2', help='scanner device string')
parser.add_argument('-r', '--resolution', dest='dpi', type=int, default=300, help='scan resolution in DPI (available: 75, 150, 300, 600, 1200, 2400)')
parser.add_argument('-s', '--paper-size', dest='size', type=str, default='a4', help='paper size (available: a4, a5, letter)')
parser.add_argument('--format', dest='format', type=str, default='png', help='output file format (available: png, tiff, pnm)')

if __name__ == "__main__":
    args = parser.parse_args()
    scanner = Scanner(args.device, args.dpi, std_geometry(args.size))
    scanner.format = args.format

    print("scant usage: [option,...>]filename[.format]")
    while True:
        size = None
        dpi = None
        filename = input("> ")
        # See if extra options are specified
        idx = filename.find(">")
        if idx != -1:
            optstr, filename = filename.split(">", 1)
            options = optstr.split(",")
            for o in options:
                if o.isdigit():
                    dpi = int(o)
                elif std_geometry(o) is not None:
                    size = std_geometry(o)
                else:
                    raise Exception("unknown option")
        scanner.scan(filename, size, dpi)

