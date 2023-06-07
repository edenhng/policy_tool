import streamlit as st
from streamlit_extras.app_logo import add_logo
    
def main() :
    #Create a side bar and format it
    with st.sidebar:
        st.title("Policy at a Glance")  
    add_logo("http://placekitten.com/120/120")
    
    #File upload function    
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)
      
if __name__ == "__main__":
    st.set_page_config(page_title="Testing Policy Tool", layout="wide")
    main()
