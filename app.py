import fitz
import time
from io import BytesIO

def compare_pages_with_annotations(file1, file2):
    doc1 = fitz.open(stream=file1.read(), filetype="pdf")
    doc2 = fitz.open(stream=file2.read(), filetype="pdf")

    for k in range(len(doc1)):
        page1=doc1[k]
        page2=doc2[k]
        
        pix1=page1.get_pixmap(dpi=150,alpha=False)
        pix2=page2.get_pixmap(dpi=150,alpha=False)
        
        t0 = time.perf_counter()
        pix_count = 0
        for i in range(pix1.width):
            for j in range(pix1.height):
                if pix1.pixel(i, j) != pix2.pixel(i, j):
                    pix2.set_pixel(i, j, (255, 0, 0)) # red)
                    pix_count += 1
        t1 = time.perf_counter()
        
        img_data = pix2.tobytes("png")
        img_stream = BytesIO(img_data)
 
        print("Modified %i pixels" % pix_count)
        print("Duration %g seconds" % round(t1 - t0, 2))
        # Display the image
        img_stream.seek(0)
        # st.write(f"Differences on Page {k + 1}")
        st.markdown(f"<center>Differences on Page {k + 1}</center>", unsafe_allow_html=True)
        st.image(img_stream, 
                #  caption=f"Differences on Page {k + 1}", 
                 use_column_width=True )

        # Print the number of modified pixels and the duration
        # st.write(f"Modified {pix_count} pixels")
        # st.write(f"Duration {round(t1 - t0, 2)} seconds")
        
    doc1.close()
    doc2.close()
    

import streamlit as st
# Create the Streamlit app
st.set_page_config(page_title="PDF Page Comparison Tool", page_icon=":page_facing_up:")
# st.title("PDF Page Comparison Tool")
st.sidebar.title("PDF Page Comparison Tool")
with st.sidebar.form("TextSelectForm",clear_on_submit=True):
    # Upload two PDF files
    uploaded_pdf1 = st.file_uploader("Upload the older PDF file", type=["pdf"],accept_multiple_files=False)
    uploaded_pdf2 = st.file_uploader("Upload the newest PDF file", type=["pdf"],accept_multiple_files=False)
    submit_button = st.form_submit_button("Start to compare PDF Pages")

if uploaded_pdf1 is not None and uploaded_pdf2 is not None:
    st.subheader("Comparing PDFs...")
    compare_pages_with_annotations(uploaded_pdf1, uploaded_pdf2)
    st.balloons()