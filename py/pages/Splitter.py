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


def validate():
    st.session_state['chapters'].sort(key=lambda x: x['start_page'])
    for i, chapter in enumerate(st.session_state['chapters']):
        if 'chapter_title' not in chapter or chapter['chapter_title'] is None:
            chapter['chapter_title'] = f'chapter{i+1}'

        if 'end_page' not in chapter or chapter['end_page'] is None:
            next_start_page = None
            for next_chapter in st.session_state['chapters']:
                if next_chapter['start_page'] > chapter['start_page']:
                    if next_start_page is None or next_chapter['start_page'] < next_start_page:
                        next_start_page = next_chapter['start_page']

            if next_start_page is not None:
                chapter['end_page'] = next_start_page - 1
            else:
                chapter['end_page'] = len(st.session_state['existing_doc'].pages)

def page_wise_chapters():
    list_of_pages = [
        {"start_page": i + 1,
         "end_page": i + 1,
         "chapter_title": f'chapter{i+1}'
         }
        for i in range(len(st.session_state['existing_doc'].pages))
    ]

    return list_of_pages


def file_uploader():
    uploaded_file = st.file_uploader(label="Upload the pdf you want to split into chapters", type=["pdf"])
    if uploaded_file:
        st.session_state['existing_doc'] = PdfReader(uploaded_file)
        total_pages = len(st.session_state['existing_doc'].pages)
        st.info("Total number of pages in the document is " + str(total_pages))
        st.subheader("How do you want to split?")
        st.caption("By default, the splitter will split each page into a separate file. If you want to split by chapters "
                   "enable the below option")
        chapter_split = st.toggle(label="Split by chapters that I specify", value=False)

        if chapter_split:
            chapters = [{"start_page": None, "end_page": None, "chapter_title": None}]

            column_config = {
                "start_page": st.column_config.NumberColumn(label="Start page", required=True, min_value=0,
                                                            max_value=total_pages, step=1),
                "end_page": st.column_config.NumberColumn(label="End page", min_value=0, max_value=total_pages, step=1),
                "chapter_title": "Chapter title"
            }
            st.session_state['chapters'] = st.data_editor(data=chapters, column_config=column_config, num_rows='dynamic')
        else:
            st.session_state['chapters'] = page_wise_chapters()

        split_files = st.button(label="Split into chapters!", type='primary')
        if split_files:
            with st.spinner("Working magic...."):
                validate()
                st.download_button(label="Download", data=splitter(), file_name='v' + str(datetime.now()) + uploaded_file.name + '.zip')
                st.toast(body="Your file is ready for download", icon=":material/thumb_up:")

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