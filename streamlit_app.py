import streamlit as st

from streamlit_gallery import apps, components
from streamlit_gallery.utils.page import page_group 

def main() :
    page = page_group("p")
    
    with st.sidebar:
        st.title("Policy at a Glance")
        
    with st.expander("COMPONENTS", True):
        page.item("Item 1 Testing")
        page.item("Item 2 Testing")
        page.item("Item 3 Testing")
        page.item("Item 4 Testing")
    
    page.show()
    
if __name__ == "__main__":
    st.set_page_config(page_title="Testing Policy Tool", layout="wide")
    main()
