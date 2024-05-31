import fitz
import streamlit as st
from datetime import datetime

def sidebar():
    with st.sidebar:
        st.subheader("Configure PDF")
        convert_cms_to_points = 28.3465
        st.session_state['page_height'] = convert_cms_to_points * st.number_input(label="Page height (cms)", min_value=4.0, value=29.7, help="Enter the height of each page in the transformed pdf in cms")
        st.session_state['page_width'] = convert_cms_to_points * st.number_input(label="Page width (cms)", min_value=4.0, value=21.0, help="Enter the width of each page in the transformed pdf in cms")
        st.session_state['margin'] = convert_cms_to_points * st.number_input(label="Margin (cms)", min_value=0.0, max_value=min(st.session_state['page_height'], st.session_state['page_width'])/2, value=1.27)
        st.session_state['landscape'] = st.checkbox(label="Stack side by side?", value=False, help="If you want the slides to be placed one next to each other, then enable this. If you want the slides to be placed one above the other, then leave this unchecked")
        st.session_state['dpi'] = st.number_input(label="Image DPI", min_value=72, max_value=600, value=150)
        st.session_state['pages'] = st.number_input(label="Pages to be merged into a single page", min_value=2, max_value=6, value=2)

def header():
    st.header("Welcome to Valancia Mixer")
    st.caption("If you have a pdf that was created from a powerpoint and you want to convert it into a pdf file that can be printed with two slides"
               "on a single page, Valancia Merger can do that for you")


def file_uploader():
    uploaded_file = st.file_uploader(label="Upload the pdf you want to transform", type=["pdf"])
    if uploaded_file:
        download_file = splitter(uploaded_file)
        st.success("Your file is ready for download!")
        st.download_button(label="Download", data=download_file, file_name='v_mixed_' + str(datetime.now()) + uploaded_file.name)

def splitter(pdf_stream):
    existing_doc = fitz.open(filetype="pdf", stream=pdf_stream.getvalue())
    effective_width = st.session_state['page_width'] - (2 * st.session_state['margin'])
    effective_height = st.session_state['page_height'] - (2 * st.session_state['margin'])
    margin = st.session_state['margin']
    if st.session_state['landscape']:
        panel_height = effective_height
        panel_width = (effective_width / st.session_state['pages']) - (margin / 2)
    else:
        panel_height = (effective_height / st.session_state['pages']) - (margin / 2)
        panel_width = effective_width

    panel_aspect = panel_height / panel_width

    new_doc = fitz.open()

    for i in range (0, existing_doc.page_count, st.session_state['pages']):
        new_page = new_doc.new_page(width=st.session_state['page_width'], height=st.session_state['page_height'])

        for j in range(0, st.session_state['pages']):
            if i + j < existing_doc.page_count:
                page = existing_doc.load_page(i+j)
                image = page.get_pixmap(dpi=st.session_state['dpi'])

                image_height = image.height
                image_width = image.width
                image_aspect = image_height / image_width

                if image_aspect > panel_aspect:
                    image_scale_x = (panel_height / image_aspect) / image_width
                    image_scale_y = panel_height / image_height
                else:
                    image_scale_x = panel_width / image_width
                    image_scale_y = (panel_width * image_aspect)/ image_height

                image_height = image.height * image_scale_y
                image_width = image.width * image_scale_x

                if st.session_state['landscape']:
                    image_start_x = margin + ((panel_width - image_width) / 2) + ((panel_width + margin) * j )
                    image_start_y = margin + ((panel_height - image_height)/2)
                else:
                    image_start_x = margin + ((panel_width - image_width) / 2)
                    image_start_y = margin + ((panel_height - image_height) / 2) + ((panel_height + margin) * j)

                image_rect = fitz.Rect(image_start_x, image_start_y, image_start_x + image_width , image_start_y + image_height)
                new_page.insert_image(image_rect, pixmap=image)

    pdf_bytes = new_doc.tobytes(garbage=4, deflate=True, use_objstms=True, deflate_images=True)
    return pdf_bytes


def main():
    st.set_page_config(
        page_title='Valancia | Mixer',
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