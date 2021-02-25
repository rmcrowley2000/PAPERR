#!/usr/bin/env python

import settings

# Imports for file access and system detection
import os # interact with file system
import sys # Needed to load settings file
import shutil
#import platform # identify OS type

# Standard Libraries
import argparse
#from collections import Counter # use a Counter object
import csv # read and write csv files
#import datetime # deal with datetime objects
#from functools import partial
import io
#import math # basic math functions
#import operator
#import random # randomization
import re # regular expression support
import shutil
import subprocess

# Tools for multiprocessing
#import multiprocessing
#import signal # smooth SIGINT handling (i.e., gracefully shut down on ^C)
#import time # timing
#import traceback # Error handling

# Store and load abstract python objects
#try:
#    import cPickle as pickle
#except:
#    import pickle

#import numpy as np # Advanced C compiled math routines
#import scikitlearn as sk # algorithms and statistics
#import pandas as pd # statistics
#import statsmodels # regressions for pandas

# Handle unicode text when writing to text files
#from kitchen.text.converters import to_bytes

# Web downloads
#import urllib2 # download files directly
#from selenium import webdriver # interact with webpages
#import tweepy # download from and interact with Twitter

# Terminal wizardry
#from subprocess import Popen, PIPE
#import curses

# Interface support
#import Tkinter as tk

def strip_chalkboard(html):
    html_out = []
    writing = True
    for line in html:
        if "chalkboard: {" in line:
            writing = False
        if writing and 'plugin/chalkboard/chalkboard.js' not in line and 'RevealChalkboard.' not in line:
            html_out.append(line)
        if not writing and '},' in line:
            writing = True
    return html_out


def strip_search(html):
    html_out = []
    writing = True
    for line in html:
        if 'plugin/search/search.js' not in line:
            html_out.append(line)
    return html_out


def strip_mathjax(html):
    html_out = []
    writing = True
    for line in html:
        if 'dynamically load mathjax for compatibility with self-contained' in line:
            writing = False
        if writing:
            html_out.append(line)
        if not writing and '</script>' in line:
            writing = True
    return html_out


def ref_r_functions(html):
    html_out = []
    funcs = {}
    with open("function_list.txt", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row):
                funcs[row[0]] = row[1]
    for line in html:
        matches = re.findall('\<code\>[a-zA-Z0-9_\.]+\(\)\\<\/code\>',line)
        if len(matches):
            for match in matches:
                f = match[6:-9]
                if f in funcs:
                    line = line.replace(match, '<a href="'+funcs[f]+'" class="ref">'+f+'()</a>')
        html_out.append(line)
    return html_out

def ref_r_packages(html):
    html_out = []
    funcs = {}
    with open("package_list.txt", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row):
                funcs[row[0]] = row[1]
    for line in html:
        matches = re.findall('\<code\>package\:[a-zA-Z0-9_\.]+\\<\/code\>',line)
        if len(matches):
            for match in matches:
                f = match[14:-7]
                if f in funcs:
                    line = line.replace(match, '<a href="'+funcs[f]+'" class="ref">'+f+'</a>')
        html_out.append(line)
    return html_out


def strip_exclude(html):
    html_out = []
    waitfor = ''
    writing = True
    for line in html:
        if writing == False and '</section>' in line:
            writing = True
        # allow this to overwrite above, since revealjs puts them on the same line
        if '<section' in line and 'id="' in line and 'class="' in line and 'exclude' in line:
            writing = False
            if '<section>' in line:
                html_out.append(line.split('</section>')[0])
        if writing:
            if "<img " in line and 'class="' in line and 'exclude"' in line:
                pass  # no need to wait for an ending tag, but don't print
            elif "<div " in line and 'class="' in line and 'exclude"' in line:
                waitfor = "</div>"
            elif "<span " in line and 'class="' in line and 'exclude"' in line:
                waitfor = "</span>"
            elif waitfor != '':
                if waitfor in line:
                    waitfor = ''
            else:
                html_out.append(line)
    return html_out
        
def strip_presentonly(html):
    html_out = []
    waitfor = ''
    writing = True
    for line in html:
        if writing == False and '</section>' in line:
            writing = True
        # allow this to overwrite above, since revealjs puts them on the same line
        if '<section' in line and 'id="' in line and 'class="' in line and 'present-only' in line:
            writing = False
            if '<section>' in line:
                html_out.append(line.split('</section>')[0])
        if writing:
            if "<img " in line and 'class="' in line and 'present-only"' in line:
                pass  # no need to wait for an ending tag, but don't print
            elif "<div " in line and 'class="' in line and 'present-only"' in line:
                waitfor = "</div>"
                waititer = 1
                waitincrease = '<div'
            elif "<span " in line and 'class="' in line and 'present-only"' in line:
                waitfor = "</span>"
                waititer = 1
                waitincrease = '<span'
            elif waitfor != '':
                if waitincrease in line:
                    waititer += 1
                if waitfor in line:
                    waititer -= 1
                    if waititer == 0:
                        waitfor = ''
            else:
                html_out.append(line)
    return html_out

def strip_never(html):
    html_out = []
    waitfor = ''
    writing = True
    for line in html:
        if writing == False and '</section>' in line:
            writing = True
        # allow this to overwrite above, since revealjs puts them on the same line
        if '<section' in line and 'id="' in line and 'class="' in line and 'never' in line:
            writing = False
            if '<section>' in line:
                html_out.append(line.split('</section>')[0])
        if writing:
            if "<img " in line and 'class="' in line and 'never"' in line:
                pass  # no need to wait for an ending tag, but don't print
            elif "<div " in line and 'class="' in line and 'never"' in line:
                waitfor = "</div>"
            elif "<span " in line and 'class="' in line and 'never"' in line:
                waitfor = "</span>"
            elif waitfor != '':
                if waitfor in line:
                    waitfor = ''
            else:
                html_out.append(line)
    return html_out

def strip_iframe(html):
    html_out = []
    writing = True
    for line in html:
        if writing == False and '</section>' in line:
            writing = True
        # allow this to overwrite above, since revealjs puts them on the same line
        if '<section' in line and 'data-background-iframe=' in line:
            writing = False
            if '<section>' in line:
                html_out.append(line.split('</section>')[0])
        if writing:
            html_out.append(line)
    return html_out


def strip_survey(html):
    html_out = []
    writing = True
    used = False
    for line in html:
        if not len(re.findall('rmc.link/[a-zA-Z0-9\-\_\.]*survey',line)):
            html_out.append(line)
    return html_out


def add_katex(html, dir, filedir):
    html_out = []
    replacing = False
    for line in html:
        # switch on
        if 'class=\"math display\"' in line:
            replacing = True
        # replacements
        if replacing:
            line = line.replace('\[','')
            line = line.replace('\]','')
            line = line.replace('{align*}','{aligned}')
            line = line.replace('{align}','{aligned}')
            if '{equation' in line:
                line = ''
        if 'class=\"math inline\"' in line:
            line = line.replace('\(','')
            line = line.replace('\)','')
        # main output
        html_out.append(line)
        
        # additions
        if 'maxScale: 1,\n' in line:
            html_out.append('        math: {\n')
            html_out.append('          enableGlobally: false,\n')
            html_out.append('          katexScript: \'plugin/math-katex/lib/katex-0.7.1/katex.min.js\',\n')
            html_out.append('          katexStylesheet: \'plugin/math-katex/lib/katex-0.7.1/katex.min.css\'\n')
            html_out.append('        },')
        if 'dependencies: [' in line:
            html_out.append('          { src: \'plugin/math-katex/math-katex.js\', async: true },\n')
        if replacing and '</span>' in line:
            replacing = False
    if not os.path.exists(dir+'/plugin/math-katex'):
        shutil.copytree('Templates/plugins/math-katex/plugin/math-katex',dir+'/plugin/math-katex')
    if not os.path.exists(dir + '/' + filedir+'/reveal.js-3.8.0/plugin/math-katex'):
        shutil.copy('Templates/plugins/math-katex/math-katex.js', dir+'/plugin/math-katex/math-katex.js')
    return html_out


def fix_edgebundleR(dir, filedir):
    shutil.copy("Templates/edgebundleR.js", dir + '/' + filedir + '/edgebundleR-binding-0.1.4/edgebundleR.js')
    return True


def fix_gallery(html, dir, filedir):
    fix = False
    insert1 = '  <link rel="stylesheet" href="'+filedir+'/reveal.js-3.8.0/plugin/gallery/gallery.css">\n'
    insert2 = "          { src: '"+filedir+"/reveal.js-3.8.0/plugin/gallery/gallery.plugin.js', async: true, condition: function() { return !!document.querySelector('.gallery'); } },\n"
    for line in html:
        if 'class="gallery' in line:
            fix = True
            break
    if fix:
        if not os.path.exists(dir + '/' + filedir + '/reveal.js-3.8.0/plugin/gallery'):
            shutil.copytree("Templates/plugins/gallery", dir + '/' + filedir + '/reveal.js-3.8.0/plugin/gallery')
        position1 = 0
        for i in range(0,len(html)):
            if "reveal.css" in html[i]:
                position1 = i+1
                break
        position2 = 0
        for i in range(0,len(html)):
            if "dependencies: [" in html[i]:
                position2 = i+1
                break
        
        if position1 and position2:
            html = html[0:position1] + [insert1] + html[position1:position2] + [insert2] + html[position2:]
    return html


def extract_run_code(dir):
    with open(dir + '/' + dir + '.Rmd', 'r') as f:
        rmd = f.readlines()
    first = True
    second = False
    writing = False
    header = ['---\n',
               'title: "Code for '+dir.replace('_',' ')+'"\n',
               'author: "Dr. Richard M. Crowley"\n',
               'date: ""\n',
               'output:\n',
               '  html_document:\n',
               '    highlight: default\n',
               '    self_contained: yes\n',
               '    theme: spacelab\n',
               '    toc: yes\n',
               '    toc_float:\n',
               '      collapsed: no\n',
               '  pdf_document:\n',
               '    toc: no\n',
               '---\n\n',
               'Note that the directories used to store data are likely different on your computer, and such references will need to be changed before using any such code.\n\n']
    header = ['---\n',
               'title: "Code for '+dir.replace('_',' ')+'"\n',
               'author: "Dr. Richard M. Crowley"\n',
               'date: ""\n',
               'output:\n',
               '  html_notebook\n',
               '---\n\n',
               'Note that the directories used to store data are likely different on your computer, and such references will need to be changed before using any such code.\n\n']
    rmd_out = []
    for line in rmd:
        if '---' in line and (first or second):
            if second:
                writing=False
                second=False
            elif first:
                second=True
                first=False
        if '```{r' in line[0:5] and not re.search('eval\s*=\s*F',line):
            writing = True
            newline = re.sub(',*\s*echo\s*=\s*F[ALSE]*', '', line)
            newline = re.sub(',*\s*include\s*=\s*F[ALSE]*', '', newline)
            newline = re.sub(',*\s*echo\s*=\s*F[ALSE]*', '', newline)
            rmd_out.append(newline)
        elif '```'  in line[0:3] and writing:
            writing = False
            rmd_out.append(line)
            rmd_out.append('\n')
        elif writing:
            rmd_out.append(line)
    
    with open(dir + '/' + dir + '_code.Rmd', 'w') as f:
        f.writelines(header + rmd_out)
    return True

def windows_unicode_patch(text):
    for i in range(0, len(text)):
        text[i] = text[i].replace('&lt;U+2191&gt;','&#x2191;')
        text[i] = text[i].replace('&lt;U+2193&gt;','&#x2193;')
        text[i] = text[i].replace('&lt;U+2714&gt;','&#x2714;')
    return text

def fix_iframe_background(html):
    for i in range(0,len(html)):
        if 'data-background-iframe' in html[i] and '<section' in html[i]:
            html = html[0:i] + [html[i].replace('data-background-iframe', 'data-background-interactive data-background-iframe')] + html[i+1:]
    return html


def fix_mathjax(html):
    edit = 0
    fix = ['<script>\n', 'Reveal.addEventListener( \'slidechanged\', function(event) {\n', '  MathJax.Hub.Rerender(event.currentSlide);\n', '} );\n', '</script>\n']
    for i in range(0, len(html)):
        if '</script>' in html[i]:
            edit = i
    html = html[:i+1] + fix + html[i+1:]
    return html
        

def worker():
    parser = argparse.ArgumentParser(description='Clean and print Reveal.js presentations.', epilog='Outputs files based on specified directory, options, and settings.py')
    parser.add_argument('folder', default='ask',
                         help='The folder to process.  Can specify just a number "1", folder "Session_1", or "all".')
    parser.add_argument('-q', '--quick', default=False, action='store_true',
                         help='Only output *_base.html copy.')
    args = parser.parse_args()
    ask = False
    dirs = next(os.walk('.'))[1]
    slide_dirs = []
    for d in dirs:
        if 'Slide' in d or 'Session' in d:
            slide_dirs.append(d)
    
    if len(sys.argv) > 1:
        if len(slide_dirs) > 1:
            if args.folder != 'all':
                try:
                    int(sys.argv[1])
                    slide_dirs = ['Session_'+args.folder]
                except:
                    if args.folder in slide_dirs:
                        slide_dirs = [args.folder]
                    else:
                        ask = True
    elif len(slide_dirs) == 1:
        pass  # no need to ask, only 1 folder
    else:
        asking = True
        while asking:
            if sys.version_info[0] < 3:
                i = raw_input('Are you sure you want to process all slide folders? (y/n)\n')
            else:
                i = input('Are you sure you want to process all slide folders? (y/n)\n')
            if i == 'y':
                asking = False
            elif i == 'n':
                asking = False
                ask = True
    
    if ask:
        if sys.version_info[0] < 3:
            i = raw_input('What is the folder name to prepare?  e.g., Session_1\n')
        else:
            i = input('What is the folder name to prepare?  e.g., Session_1\n')
        slide_dirs = [i]
    
    # Versions:
    #     html
    #     html_print
    #     html_print_post
    #     html_post
    #     html_present
    
    
    for dir in slide_dirs:
        for filedir in next(os.walk(dir))[1]:
            if "_files" not in filedir or '_R_files' in filedir:
                continue
            fd = filedir
            # Copy updated reveal.js code to folder
            # Contains fixed version of chalkboard.js for proper writing (and thinner lines)
            if os.path.exists(dir + "/" + filedir + "/reveal.js-3.8.0"):
                shutil.rmtree(dir + "/" + filedir + "/reveal.js-3.8.0")
            shutil.copytree("Templates/reveal.js-3.8.0", dir + "/" + filedir + "/reveal.js-3.8.0")
            # Propogate newest css template
            shutil.copy("Templates/white-edits-3.8.0.css", dir + "/white-edits-3.8.0.css")
            # Drop the useless kePrint.js library
            if os.path.exists(dir + "/" + filedir + '/kePrint-0.0.1'):
                shutil.rmtree(dir + "/" + filedir + '/kePrint-0.0.1')
            # Within file commands
            
        # html file edits
        files = next(os.walk(dir))[2]
        # Find base file
        slide_base = ""
        for f in files:
            if ".html" in f and ('Session' in f or 'Slide' in f):
                if len(f) < len(slide_base) or slide_base == "":
                    slide_base = f
        
        with io.open(dir + '/' + slide_base, 'r', encoding='utf-8') as f:
            html = f.readlines()
        
        # Remove the useless kePrint.js and head.min.js calls
        for i in range(0, len(html)):
            if 'kePrint-0.0.1/kePrint.js"></script>' in html[i]:
                html[i] = ''
        for i in range(0, len(html)):
            if '/lib/js/head.min.js"></script>' in html[i]:
                html[i] = ''
        # Replace references to the old reveal.js with the 3.8.0 version
        for i in range(0, len(html)):
            if 'reveal.js-3.3.0.1' in html[i]:
                html[i] = html[i].replace('reveal.js-3.3.0.1', 'reveal.js-3.8.0')
        line_to_change = 0
        # Add in new controls layout
        for i in range(0, len(html)):
            if 'maxScale: 1,' in html[i]:
                line_to_change = i
                break
        html = html[0:i+1] + ['        controlsLayout: "edges",\n'] + html[i+1:-1]
        # Change css reference file
        for i in range(0, len(html)):
            if 'white-edits.css' in html[i]:
                html[i] = html[i].replace('white-edits.css', 'white-edits-3.8.0.css')
        # Global fixes
        if settings.katex:
            html = strip_mathjax(html)
            html = add_katex(html, dir, fd)  # Replaces mathjax with katex
        else:
            html = fix_mathjax(html)  # Forces local rerendering of Mathjax
        if settings.edgebundleR:
            fix_edgebundleR(dir, fd)  # Allows edgbundleR to work properly in the slides
        if settings.ref_r_functions:
            html = ref_r_functions(html)  # Adds references/formatting to R functions of the form `name()`
        if settings.ref_r_packages:
            html = ref_r_packages(html)  # Adds references/formatting to R packages of the form `package:name`
        html = fix_gallery(html, dir, fd)  # Makes gallery code functional
        html = fix_iframe_background(html)  # Makes iframe backgrounds scrollable
        # remove personal notes
        html = strip_never(html)
        # Fix some unicode characters that R on Windows chokes on
        html = windows_unicode_patch(html)
        if settings.output_code:
            extract_run_code(dir)
        
        for version in ["print","preprint","base","pre","post"]:
            # Individual version fixes
            if settings.versions[version] and (not args.quick or version == "base"):
                html_version = html[:]
                if settings.versions[version+'_search']:
                    html_version = strip_search(html_version)
                if settings.versions[version+'_chalkboard']:
                    html_version = strip_chalkboard(html_version)
                if settings.versions[version+'_exclude']:
                    html_version = strip_exclude(html_version)
                if settings.versions[version+'_presentonly']:
                    html_version = strip_presentonly(html_version)
                if settings.versions[version+'_survey']:
                    html_version = strip_survey(html_version)
                if not settings.versions[version+'_scaling']:
                    for i in range(0, len(html_version)):
                        if 'maxScale: 1,' in html_version[i]:
                            html_version[i] = html_version[i].replace('maxScale','//maxScale')
                        if 'minScale: 1,' in html_version[i]:
                            html_version[i] = html_version[i].replace('minScale','//minScale')
                if 'print' in version:
                    # special settings for printing compatibility
                    html_version = strip_iframe(html_version)
                with io.open(dir + '/' + slide_base[:-5]+'_'+version+'.html', 'w', encoding='utf-8') as f:
                    if sys.version_info[0] < 3:
                        f.writelines(map(unicode,html_version))
                    else:
                        f.writelines(html_version)
                if settings.printing and 'print' in version:
                    if settings.use_local_printreveal_instance:
                        printrevealcommand = 'python printreveal_v2.py'
                    else:
                        printrevealcommand = 'printreveal_v2.py'
                    if slide_base[:-5] in settings.overrides:
                        number = ' -n '+str('\n'.join(html_version).count('<section id='))
                    else:
                        number = ''
                    if settings.compress:
                        return_code = subprocess.call(printrevealcommand + ' -c' + number + ' -f \"' + os.path.abspath(dir + '/' + slide_base[:-5]+'_'+version+'.html\"'), shell=True)
                        if not settings.retain_full:
                            os.remove(dir + '/' + slide_base[:-5]+'_'+version+'.pdf')
                    else:
                        return_code = subprocess.call(printrevealcommand + number + ' -f \"' + os.path.abspath(dir + '/' + slide_base[:-5]+'_'+version+'.html\"'), shell=True)
    return True

if __name__ == '__main__':
    worker()

