import fitz
import streamlit as st
from datetime import datetime

def sidebar():
    with st.sidebar:
        st.subheader("Configure PDF")
        page_height = st.number_input(label="Page height (cms)", min_value=4.0, value=29.7, help="Enter the height of each page in the transformed pdf in cms")
        page_width = st.number_input(label="Page width (cms)", min_value=4.0, value=21.0, help="Enter the width of each page in the transformed pdf in cms")
        margin = st.number_input(label="Margin (cms)", min_value=0.0, max_value=min(page_height, page_width)/2, value=1.27)
        landscape_mode = st.checkbox(label="Landscape mode?", value=False, help="If you want the slides to be placed one next to each other, then enable this. If you want the slides to be placed one above the other, then leave this unchecked")
        dpi = st.number_input(label="Image DPI", min_value=72, max_value=600, value=150)
        convert_cms_to_points = 28.3465
        st.session_state['page_height'] = page_height * convert_cms_to_points
        st.session_state['page_width'] = page_width * convert_cms_to_points
        st.session_state['margin'] = margin * convert_cms_to_points
        st.session_state['landscape'] = landscape_mode
        st.session_state['dpi'] = dpi

def header():
    st.header("Welcome to Valancia")
    st.caption("If you have a pdf that was created from a powerpoint and you want to convert it into a pdf file that can be printed with two slides on a single page, Valancia can do that for you")


def file_uploader():
    uploaded_file = st.file_uploader(label="Upload the pdf you want to transform", type=["pdf"])
    if uploaded_file:
        download_file = splitter(uploaded_file)
        st.success("Your file is ready for download!")
        st.download_button(label="Download", data=download_file, file_name='v' + str(datetime.now()) + uploaded_file.name)

def splitter(pdf_stream):
    existing_doc = fitz.open(filetype="pdf", stream=pdf_stream.getvalue())
    effective_width = st.session_state['page_width'] - (2 * st.session_state['margin'])
    effective_height = st.session_state['page_height'] - (2 * st.session_state['margin'])
    margin = st.session_state['margin']
    if st.session_state['landscape']:
        panel_height = effective_height
        panel_width = (effective_width / 2) - (margin / 2)
    else:
        panel_height = (effective_height / 2) - (margin / 2)
        panel_width = effective_width

    panel_aspect = panel_height / panel_width

    new_doc = fitz.open()

    for i in range (0, existing_doc.page_count, 2):
        new_page = new_doc.new_page(width=st.session_state['page_width'], height=st.session_state['page_height'])

        first_page = existing_doc.load_page(i)
        first_image = first_page.get_pixmap(dpi=st.session_state['dpi'])

        first_image_height = first_image.height
        first_image_width = first_image.width
        first_image_aspect = first_image_height / first_image_width

        if first_image_aspect > panel_aspect:
            first_image_scale_x = (panel_height / first_image_aspect) / first_image_width
            first_image_scale_y = panel_height / first_image_height
        else:
            first_image_scale_x = panel_width / first_image_width
            first_image_scale_y = (panel_width * first_image_aspect)/ first_image_height

        first_image_height = first_image.height * first_image_scale_y
        first_image_width = first_image.width * first_image_scale_x

        first_image_start_x = margin + ((panel_width - first_image_width) / 2)
        first_image_start_y = margin + ((panel_height - first_image_height)/2)
        first_image_rect = fitz.Rect(first_image_start_x, first_image_start_y, first_image_start_x + first_image_width , first_image_start_y + first_image_height)
        new_page.insert_image(first_image_rect, pixmap=first_image)

        if (i+1 < existing_doc.page_count) :
            second_page = existing_doc.load_page(i+1)
            second_image = second_page.get_pixmap(dpi=st.session_state['dpi'])

            second_image_height = second_image.height
            second_image_width = second_image.width
            second_image_aspect = second_image_height / second_image_width

            if second_image_aspect > panel_aspect:
                second_image_scale_x = (panel_height / second_image_aspect) / second_image_width
                second_image_scale_y = panel_height / second_image_height
            else:
                second_image_scale_x = panel_width / second_image_width
                second_image_scale_y = (panel_width * second_image_aspect) / second_image_height

            second_image_height = first_image.height * second_image_scale_y
            second_image_width = first_image.width * second_image_scale_x

            if st.session_state['landscape']:
                second_image_start_x = margin + panel_width + margin / 2 + ((panel_width - second_image_width) / 2)
                second_image_start_y = margin + ((panel_height - second_image_height)/2)
            else:
                second_image_start_x = margin + ((panel_width - second_image_width) / 2)
                second_image_start_y = margin + panel_height + (margin / 2) + ((panel_height - second_image_height)/2)

            second_image_rect = fitz.Rect(second_image_start_x, second_image_start_y, second_image_start_x + second_image_width , second_image_start_y + second_image_height)
            new_page.insert_image(second_image_rect, pixmap=second_image)

    file_name = 'v' +  str(datetime.now()) + pdf_stream.name
    #new_doc.save(file_name, garbage=4, deflate=True, deflate_images=True, clean=True, deflate_fonts=True)
    pdf_bytes = new_doc.tobytes(garbage=4, deflate=True, use_objstms=True, deflate_images=True)
    return pdf_bytes


def main():
    st.set_page_config(
        page_title='Valancia',
        page_icon=':material/home:',
        menu_items={
            'Get help': 'https://www.google.com',
            'About': '# Version: 2.2 #'
        })

    sidebar()
    header()
    file_uploader()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()