# valancia

## introduction
valancia is a pdf transformer built for a very specific use case. if someone has handed you a pdf file made from a powerpoint presentation and you want to layout two slides on a single page, then valancia can help. the original request for valancia came up on [reddit](https://www.reddit.com/r/learnprogramming/comments/1cqafk8/seeking_help_resizing_powerpoint_slides_for/).

the original request stated:
> Hello, I'm a university student, and usually, our teachers, after the lectures, send us the lessons that were PowerPoint presentations as PDFs. You know the form of the slides that looks like [img 1]. When I want to print them, they look huge on the pages. Even if I print two on one page, it still doesn't look good for me. I want to make it look like [img 2]. I heard that there's an option in printers to do that, but unfortunately, it's not available on the printer that I have access to. So, I thought using Python to do that would be great. However, I've been struggling all week with the results that I'm not good with. So, please, if someone can help me with this or provide me with the code, I'd be so grateful because I need it as fast as possible. Also, I want to print the files in duplex printing (printing on both sides of the page). Thank you very much.

## how do i run this?
you can access the hosted version of the app at [valancia](https://valancia.streamlit.app)

## how does it work?
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
