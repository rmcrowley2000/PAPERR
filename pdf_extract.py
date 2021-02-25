import sys
import argparse
import platform

parser = argparse.ArgumentParser(description='Reads a (set of) pdf files and extracts raw text')
parser.add_argument('path', nargs='+', help='Path of a file or a folder of files.')
parser.add_argument('-n', '--removenumeric', dest="removenum", default=False, action='store_true', help='Flag to remove numerics.')
args = parser.parse_args()


if sys.platform.startswith('linux'):
    if platform.machine().endswith('64'):
        OS = "lin"
        BITS = 64
    else:
        OS = "lin"
        BITS = 32
elif sys.platform == "darwin":
    OS = "mac"
elif sys.platform == "win32":
    OS = "win"

if OS == "lin":
    import textract
elif OS == "win":
    if sys.version_info[0] < 3:
        from cStringIO import StringIO
    else:
        from io import StringIO
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    #import getopt
else:
    print("Unsupported OS")
    sys.exit()

import re
import os

# Settings
files = args.path
remove_numeric = args.removenum

def main_lin():
    if not os.path.exists('Data/'):
        os.mkdir('Data')

    text = ''
    for f in files:
        newtext = textract.process(f)
        if len(newtext) < 10000:
             newtext = textract.process(f,method='tesseract', language='eng')
        print(f + '\n' + str(len(newtext)))
        text = text + ' ' + newtext 

    print('Stripping out other characters')
    text = re.sub(r'([^\s\w]|_)+', '', text)
    if remove_numeric:
        text = re.sub(r'\w*\d\w*', '', text).strip()
    text = ' '.join(text.split()) + '\n'

    text = 'text\n' + text

    if sys.version_info[0] < 3:
        with open('Data/text.txt', 'w') as f:
            f.write(text)
    else:
        with open('Data/text.txt', 'w', encoding='utf-8') as f:
            f.write(text)
    return

#converts pdf, returns its text content as a string
#from https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text 
   
#converts all pdfs in directory pdfDir, saves all resulting txt files to txtdir
def convertMultiple(pdfDir, files, txtDir):
    text = ""
    if pdfDir == "": pdfDir = os.getcwd() + "\\" #if no pdfDir passed in 
    for pdf in files: #iterate through pdfs in pdf directory
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            pdfFilename = pdfDir + pdf 
            newtext = convert(pdfFilename) #get string of text content of pdf
            #textFilename = txtDir + pdf + ".txt"
            text = text + ' ' + newtext
    
    print('Stripping out other characters')
    text = re.sub(r'([^\s\w]|_)+', '', text)
    if remove_numeric:
        text = re.sub(r'\w*\d\w*', '', text).strip()
    
    text = ' '.join(text.split()) + '\n'

    text = 'text\n' + text

    if sys.version_info[0] < 3:
        with open('Data/text.txt', 'w') as f:
            f.write(text)
    else:
        with open('Data/text.txt', 'w', encoding='utf-8') as f:
            f.write(text)
    
def main_win():
    """
    pdfDir = ""
    txtDir = ""
    try:
        opts, args = getopt.getopt(argv,"ip:t:")
    except getopt.GetoptError:
        print("pdfToT.py -p <pdfdirectory> -t <textdirectory>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            print("pdfToT.py -p <pdfdirectory> -t <textdirectory>")
            sys.exit()
        elif opt == "-p":
            pdfDir = arg
        elif opt == "-t":
            txtDir = arg
    convertMultiple(pdfDir, txtDir)
    """
    convertMultiple("", files, "Data/text.txt")
    
    
    return

if __name__ == "__main__":
    if OS == "lin":
        main_lin()
    elif OS == "win":
        main_win()
    else:
        sys.exit()
