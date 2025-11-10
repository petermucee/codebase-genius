import streamlit as st
import subprocess
import sys
import os

st.set_page_config(page_title='Backend Test', page_icon='📚')

st.title('Backend Connection Test')
st.write('Click the button to test backend connection')

if st.button('Test Backend'):
    with st.spinner('Running backend analysis'):
        result = subprocess.run([
            sys.executable, 'BE/integrated_supervisor.py'
        ], capture_output=True, text=True, cwd='..')
        
        if result.returncode == 0:
            st.success('Backend working')
            st.text_area('Output', result.stdout, height=400)
        else:
            st.error('Backend failed')
            st.text_area('Error', result.stderr, height=400)
