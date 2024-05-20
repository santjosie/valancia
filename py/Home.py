import streamlit as st

def main():
    st.set_page_config(
        page_title='Valancia',
        page_icon=':material/home:',
        menu_items={
            'Get help': 'https://www.google.com',
            'About': '# Version: 2.2 #'
        })
    st.header("Welcome to Valancia!")
    st.caption("A suite of open-source tools to transform pdf documents. For free!")
    st.subheader("List of tools")
    functions = [
        {"Name": "Merger","Description":"Combines multiple pages of a pdf into a single page."},
                 {"Name": "Splitter","Description":"Split a pdf into separate files. Like chapters of a book"}
                 ]

    st.dataframe(data=functions)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()