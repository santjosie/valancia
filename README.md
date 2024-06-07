# valancia

## table of contents
-[introduction](#introduction)
-[what can valancia do?](#what-can-it-do)
-[how do I run this?](#how-do-i-run-this)
-[origin story](#origin-story)
-[contributing](#contributing)
-[thanks](#thanks)

## introduction
valancia is a free pdf transformer that can be used to programmatically manipulate pdf files. if there is a specific pdf transformation that you want and is currently not supported, please log an issue and we'll try to get it added.

## what can it do?
valancia currently supports three functions.
1. merger - when you have multiple pdfs that you want to combine into a single file. maybe you scanned pages of a document as separate pdfs and you want to combine them into one. 
2. mixer - the og transformation. can mix multiple pdf pages into a single page. perfect when you have pdfs made from powerpoints and you want to merge two slides into a single page to save on paper when printing.
3. splitter - when you have a single pdf that you want to split into multiple pdfs - one for each chapter, or maybe one for each page.

## how do i run this?
1. option 1 - you can access the hosted version of the app at [valancia](https://valancia.streamlit.app)
2. option 2 - you can clone this repo and run it locally on your machine. if you're doing that ensure that all the python libraries in the requirements.txt file are installed in your machine. once installed, navigate to the project folder and run the following command to start valancia in your browser `streamlit run py/Home.py`

## origin story
valancia was originally built for a very specific request that came from a stranger on the internet. the original request for valancia came up on [reddit](https://www.reddit.com/r/learnprogramming/comments/1cqafk8/seeking_help_resizing_powerpoint_slides_for/). it stated:
> Hello, I'm a university student, and usually, our teachers, after the lectures, send us the lessons that were PowerPoint presentations as PDFs. You know the form of the slides that looks like [img 1]. When I want to print them, they look huge on the pages. Even if I print two on one page, it still doesn't look good for me. I want to make it look like [img 2]. I heard that there's an option in printers to do that, but unfortunately, it's not available on the printer that I have access to. So, I thought using Python to do that would be great. However, I've been struggling all week with the results that I'm not good with. So, please, if someone can help me with this or provide me with the code, I'd be so grateful because I need it as fast as possible. Also, I want to print the files in duplex printing (printing on both sides of the page). Thank you very much.

after building the mixer transformation, other transformations were added as and when other needs arose.

## contributing
if you would like to contribute to this project and add in more transformations, or enhance one of the existing ones, please go ahead and log an issue.

## thanks
this project is standing on the shoulders of giants. the open-source libraries that made this project feasible are:
1. streamlit
2. pymupdf
3. pypdf

## how does the mixer work?
#### user journey
- specify the page height, width, margin, dpi of the final pdf that you want
- upload the pdf that you want to convert
- download the transformed pdf

#### what happens behind the scenes?
- the file is loaded into memory
- the pages of the file are opened, two at a time
- a pixmap of each page is generated
- calculations are done to determine where to place the pixmap in a new page
- the pixmaps are placed, two in a page
- the final document is created in memory and bound to a download button

## so, how to centre a div?
i don't know. but i can tell you how i centre slides.
the app tries to centre the two slides as much as possible.

to do this, first the area of the page is generated based on the height and the width that the user inputs.
then the margins are subtracted to find the total available area for placing content.
an additional margin is added in the middle to provide some space between the slides.
whether this is a vertical margin or a horizontal margin depends on whether the user has chosen landscape mode or portrait mode for the transformed pdf.
what is left over are the panel areas where slides need to be centred.
the slides are resized while maintaining the aspect ratio and then placed into the center of the panels.

all quick maths.
