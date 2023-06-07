import streamlit as st

def add_logo():
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] + div {{
                background-image: url(http://placekitten.com/200/200);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }}
            [data-testid="stSidebarNav"]::before {{
                content: "My Company Name";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main() :
    #Create a side bar and format it
    with st.sidebar:
        st.title("Policy at a Glance")
    add_logo()    
    #File upload function    
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)
      
if __name__ == "__main__":
    st.set_page_config(page_title="Testing Policy Tool", layout="wide")
    main()
