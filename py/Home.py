import streamlit as st

def main():
    st.set_page_config(
        page_title='Valancia | Home',
        page_icon=':material/home:',
        menu_items={
            'Get help': 'https://www.google.com',
            'About': '# Version: 2.2 #'
        })
    st.header("Welcome to Valancia!")
    st.caption("A suite of open-source tools to transform pdf documents. For free!")
    st.subheader("List of tools")
    functions = [
        {"Name": "Merger",
         "Description": "Combines multiple pdf files into a single pdf file."},
        {"Name": "Mixer","Description":"Combines multiple pages of a pdf into a single page. Useful for printing pdfs made from powerpoint slides."},
        {"Name": "Splitter","Description":"Split a pdf into separate files. Like chapters of a book. You could also split the entire pdf into single page pdfs."}
        ]

    st.dataframe(data=functions)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()