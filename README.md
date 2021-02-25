# PAPERR
**P**ython script to **A**ssemble **P**resentations for **E**ducation using **R**markdown and **R**eveal.js.  This script and template takes Rmarkdown files knitted using the revealjs R library and converts them to presentation slides (html), handout slides (html & pdf, with options for pre- & post-presentation copies), and code extraction output (html).  Contains many compatibility fixes and convenience additions.

Requirements:
1. [R](https://www.r-project.org/) (tested on 3.4.0 and up)
2. [Rmarkdown](https://github.com/rstudio/rmarkdown)
3. The [revealjs](https://github.com/rstudio/revealjs) R library
4. [Python 3](https://www.python.org/)
5. [decktape-2.9.3](https://github.com/astefanutti/decktape/tree/v2.9.3)
    - OPTIONAL: needed for printing out PDF files
    - INSTALLATION NOTES: If on Linux, store decktape-2.9.3 either:
        1. In the base folder and rename it to decktape-2.9.3-linux or decktape-2.9.3-windows depending on your operating system
        2. Put the folder somewhere that is directly on PATH, e.g. in ~/bin/ on Linux or add it to the PATH environmental variable in windows.
6. [Ghostscript](https://www.ghostscript.com/)
    - OPTIONAL: needed for compressing PDF output
    - INSTALLATION NOTES: Make sure ghostscript can be called from the terminal or is on PATH


Directory Structure:

- Backgrounds
    - Stores all slide backgrounds.  Includes Title, Section, and default slides
- Data
    - Stores data files for R and python.  Includes 2 example files used by template slides.
- Figures
    - Stores all other images.  Includes SMU logo for accenting by default.
- Slides
    - All Slide Rmd and html here
- Templates
    - Extra code referenced by `prep.py`.  Includes:
        - A copy of reveal.js-3.8.0 for patching knitted revealjs output
        - Updated chalkboard.js file to write in Chrome and Edge
        - A gallery plugin
        - A copy of katex for offline LaTeX rendering
        - Up-to-date css file (useful if making multiple Slide folders in 1 template)

Scripts:
- python pdf_extract.py
    - Takes one or my pdf files via command line (Windows or Linux only)
    - Converts files from pdf to 1 txt file, stored as "Data/text.txt"
    - Optionally take a '-n' flag, which instructs it to remove numbers
- python prep.py
    - Python 3 script handling all preparation of the html files
    - Passes off to printreveal_v2.py as needed for exporting PDF files
    - Requires ghostscript to be installed and on PATH
- RScript wordcloud.R
    - Takes the "Data/text.txt" file and generates "Backgrounds/wordcloud.png"
    - The latter file is suitable as a background

Tested on:
    - Windows 10 + Chrome
    - Debian Testing + Chrome
Troubleshooting:
    - Errors due to "The SUID sandbox helper binary is missing" or "No usable sandbox!" on Linux
        - Run in terminal: sudo sysctl -w kernel.unprivileged_userns_clone=1
    - Decktape not working
        - Are you using version 2.9.3?  The script cannot handle any other version, and PDF output is really finicky depending on the version.



Thanks to the following projects that make this possible:

1. [rstudio/Rmarkdown](https://github.com/rstudio/rmarkdown)
2. [hakimel/reveal.js](https://github.com/hakimel/reveal.js)
3. [rstudio/revealjs](https://github.com/rstudio/revealjs)
4. [astefanutti/decktape](https://github.com/astefanutti/decktape/)
5. [KaTeX/KaTeX](https://github.com/KaTeX/KaTeX)
6. [rajgoel/reveal.js-plugins/chalkboard](https://github.com/rajgoel/reveal.js-plugins/tree/master/chalkboard)
7. [marcins/revealjs-simple-gallery](https://github.com/marcins/revealjs-simple-gallery)
8. [Ghostscript](https://www.ghostscript.com/)
9. All the artists behind the included CC0 backgrounds

Copyright 2021 Richard M. Crowley (https://rmc.link/)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


