#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib as urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    def after_dash(x):
        result = re.findall('(?<=-)\w+', x)[-1]
        return result
        
    with open(filename, 'r') as f:
        file_str = f.read()
        puzzle_url = re.findall(r'GET (.*?) HTTP', file_str)
        full_urls = ['http://code.google.com' + url for url in puzzle_url]
        del_dupl = list(set(full_urls))
        puzzle_urls = filter(lambda k: 'puzzle' in k, del_dupl)
        sorted_urls = sorted(list(set(puzzle_urls)), key=after_dash)
    return sorted_urls


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    if not os.path.exists(str(dest_dir)):
        os.mkdir(dest_dir)
    print('Retreiving...')
    with open(str(dest_dir) + "/index.html", 'w') as file:
        file.write("<html><body>")
        for index, url in enumerate(img_urls):
            urllib.urlretrieve(url, filename = dest_dir + '/img' + str(index) + ".jpg")
            file.write("<img src='img" + str(index) + ".jpg' >")
        file.write("</body></html>")
    return


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
