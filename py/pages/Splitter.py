import streamlit as st
from pypdf import PdfReader, PdfWriter
from datetime import datetime
import re
import io
import zipfile

def header():
    st.header("Welcome to Valancia Splitter")
    st.caption("If you have a pdf that contains multiple chapters and you want to split the single pdf into individual chapters,"
               "Valancia Splitter can do that for you")


def zipper(pdfs_buffer):
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as z:
        for pdf_buffer in pdfs_buffer:
            z.writestr(pdf_buffer['file_name'], pdf_buffer['pdf_object'].getvalue())

    return zip_buffer

def splitter():
    disallowed_special_chars = r'[^a-zA-Z0-9\s_]'
    pdfs_buffer = []
    for chapter in st.session_state['chapters']:
        writer = PdfWriter()
        pdf_buffer = io.BytesIO()
        for page in st.session_state['existing_doc'].pages[chapter['start_page'] - 1 :chapter['end_page']]:
            writer.add_page(page)

        writer.add_metadata(
            {
                "/Author": "Valancia Splitter",
                "/Title": chapter['chapter_title'],
                "/CreationDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "/ModDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

        file_name = re.sub(disallowed_special_chars, '', chapter['chapter_title']) + '.pdf'

        writer.write(pdf_buffer)
        pdfs_buffer.append({"file_name":file_name, "pdf_object":pdf_buffer})
        writer.close()

    return zipper(pdfs_buffer)


def file_uploader():
    uploaded_file = st.file_uploader(label="Upload the pdf you want to split into chapters", type=["pdf"])
    if uploaded_file:
        st.session_state['existing_doc'] = PdfReader(uploaded_file)
        total_pages = len(st.session_state['existing_doc'].pages)
        st.info("Total number of pages in the document is " + str(total_pages))

        st.subheader("Specify the pages of each chapter")
        chapters = [{"start_page":None, "end_page":None, "chapter_title":None}]

        column_config = {
            "start_page" : st.column_config.NumberColumn(label="Start page", required=True, min_value=0, max_value=total_pages, step=1),
            "end_page" : st.column_config.NumberColumn(label="End page", min_value=0, max_value=total_pages, step=1),
            "chapter_title" : "Chapter title"
        }
        st.session_state['chapters'] = st.data_editor(data=chapters, column_config=column_config, num_rows='dynamic')

        split_files = st.button(label="Split into chapters!", type='primary')
        if split_files:
            #STEP1 - validate chapter list
            st.success("Your file is ready for download!")
            st.download_button(label="Download", data=splitter(), file_name='v' + str(datetime.now()) + uploaded_file.name + '.zip')

def main():
    st.set_page_config(
        page_title='Valancia',
        page_icon=':material/home:',
        menu_items={
            'Get help': 'https://www.google.com',
            'About': '# Version: 2.2 #'
        })

    header()
    file_uploader()


if __name__ == '__main__':
    main()