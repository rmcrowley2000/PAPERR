#!/usr/bin/env python

# NOTE: This script requires a copy of decktape.js properly set up in the decktape-2.9.3 folder, along with ghostscript AND node.js WITH chalk installed
# It uses puppet, based on chrome, to print.  It prints at a higher resolution than printreveal.py.

import sys
#if sys.version_info[0] < 3:
#    import SimpleHTTPServer
#else:
#    import http.server

#import SocketServer
#from threading import Thread
#import time
import subprocess
import argparse
import os

import posixpath
if sys.version_info[0] < 3:
    import urllib
else:
    import urllib.parse as urllib

#if sys.version_info[0] < 3:
#    from SimpleHTTPServer import SimpleHTTPRequestHandler
#    from BaseHTTPServer import HTTPServer
#else:
#    from http.server import SimpleHTTPRequestHandler
#    from http.server import HTTPServer


#class RootedHTTPServer(HTTPServer):
#    def __init__(self, base_path, *args, **kwargs):
#        HTTPServer.__init__(self, *args, **kwargs)
#        self.RequestHandlerClass.base_path = base_path


#class RootedHTTPRequestHandler(SimpleHTTPRequestHandler):
#    def translate_path(self, path):
#        path = posixpath.normpath(urllib.unquote(path))
#        words = path.split('/')
#        words = filter(None, words)
#        path = self.base_path
#        for word in words:
#            drive, word = os.path.splitdrive(word)
#            head, word = os.path.split(word)
#            if word in (os.curdir, os.pardir):
#                continue
#            path = os.path.join(path, word)
#        return path

# Variables
#URL = 'localhost'
#PORT = 8000
cwd = os.path.dirname(os.path.abspath(__file__))
print(cwd)

# interpret input
args = argparse.ArgumentParser(description="Reveal.js parser")
args.add_argument('-f', '--file', dest='slidehtml', default='NA',
                      help='Location of html file to print')
args.add_argument('-c', '--compress', dest='compress', default=False, action='store_true')
args.add_argument('-n', '--number', dest='number', default='NA',
                      help='Number of slides to print')
args = args.parse_args()
slidehtml = os.path.abspath(args.slidehtml)
if '.html' not in slidehtml:
    print('Please pass a valid reveal.js html file')
    exit()

#if sys.platform == "win32":
#    http_directory = '\\'.join(slidehtml.split('\\')[:-3])
#else:
#    http_directory = '/'.join(slidehtml.split('/')[:-3])
http_directory = 'file://' + '/'.join(slidehtml.split('/')[:-3])

#server_address = ('', PORT)

#httpd = RootedHTTPServer(http_directory, server_address, RootedHTTPRequestHandler)
#sa = httpd.socket.getsockname()
print(slidehtml)
print(http_directory)
#print("Serving HTTP on", http_directory, "port", sa[1], "...")

#def simple_sever():
#    httpd.serve_forever()

#simple_sever_T = Thread(target=simple_sever, name='simple_sever')
#simple_sever_T.daemon = True
#simple_sever_T.start()

# wait for server to be running
#while not simple_sever_T.is_alive():
#    time.sleep(1)

# run print command and wait for finish
if sys.platform == "win32":
    relativehtml = http_directory + '/' + '/'.join(slidehtml.split('\\')[-3:])
    os.chdir(cwd + '/decktape-2.9.3-windows/')  # sets the directory for print libraries
else:
    relativehtml = http_directory + '/' + '/'.join(slidehtml.split('/')[-3:])
    os.chdir(cwd + '/decktape-2.9.3-linux/')  # sets the directory for print libraries
slidepdf = slidehtml[:-4] + 'pdf'
compressedpdf = slidepdf[:-4]+'-compress.pdf'

print('Printing from: ' + relativehtml)
print('Printing to: ' + slidepdf)

if args.number != 'NA':
    try:
        number = int(args.number)
        number = ' --slides 1-' + str(number)+' '
    except:
        number = ''
else:
    number = ''

# Print slides in full resolution
return_code = subprocess.call("node decktape.js "+ number +"-s 1536x1152 reveal " + relativehtml + ' \"' + slidepdf+"\"", shell=True)

if args.compress:
    print('Compressing pdf')
    if sys.platform == "win32":    
        return_code = subprocess.call("gswin64c -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -dPrinted=false -sOutputFile=\""+compressedpdf+"\" \""+slidepdf+"\"", shell=True)
    else:
        return_code = subprocess.call("ghostscript -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -dPrinted=false -sOutputFile=\""+compressedpdf+"\" \""+slidepdf+"\"", shell=True)

#httpd.shutdown()
#httpd.server_close()





