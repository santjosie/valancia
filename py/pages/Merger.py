import streamlit as st
from datetime import datetime
from pypdf import PdfReader, PdfWriter
import io

def header():
    st.header("Welcome to Valancia Merger")
    st.caption("If you lots of pdf files that you want to merge into a single file, this is the tool for you.")


def merger():
    writer = PdfWriter()
    pdf_buffer = io.BytesIO()
    for uploaded_file in st.session_state['uploaded_files']:
        current_file = PdfReader(uploaded_file)
        for page in current_file.pages:
            writer.add_page(page)

    writer.write(pdf_buffer)
    writer.close()
    return pdf_buffer


def file_uploader():
    uploaded_files = st.file_uploader(label="Upload the pdf you want to split into chapters", type=["pdf"], accept_multiple_files=True)

    if len(uploaded_files) > 1:
        merge_files = st.button(label="Merge!", type='primary')
        if merge_files:
            with st.spinner("Working magic...."):
                st.session_state['uploaded_files'] = uploaded_files
                st.download_button(label="Download", data=merger(), file_name='v_merged_' + str(datetime.now()) + '.pdf')
                st.toast(body="Your file is ready for download", icon=":material/thumb_up:")

def main():
    st.set_page_config(
        page_title='Valancia | Merger',
        page_icon=':material/home:',
        menu_items={
            'Get help': 'https://www.google.com',
            'About': '# Version: 2.2 #'
        })

    header()
    file_uploader()

if __name__=="__main__":
    main()