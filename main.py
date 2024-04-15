import streamlit as st
from msal import PublicClientApplication
import webbrowser

# Configure your MSAL client
CLIENT_ID = '8395b6fb-53d2-4a1f-b582-828323691482'
TENENT_ID = 'common'
AUTHORITY_URL = f'https://login.microsoftonline.com/{TENENT_ID}'
SCOPES = []  # This scope allows reading user profile data
REDIRECT_URI = 'https://pricing-analyst.streamlit.app'  # Make sure this is added in Azure

# MSAL app instance
app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY_URL)
st.write("Hello")

def authenticate():
    flow = app.initiate_auth_code_flow(SCOPES, redirect_uri=REDIRECT_URI)
    st.session_state['auth_flow'] = flow
    login_url = flow['auth_uri']
    st.markdown(f'Please log in [here]({login_url}).')

if 'auth_flow' not in st.session_state:
    st.button("Login with Microsoft", on_click=authenticate)

def handle_redirect():
    if 'auth_flow' in st.session_state and st.query_params:
        code = st.query_params.get('code', None)
        if code:
            flow = st.session_state['auth_flow']
            result = app.acquire_token_by_auth_code_flow(flow, st.query_params)
            if 'id_token_claims' in result:
                st.session_state['user'] = result['id_token_claims']
                user_email = st.session_state['user'].get('email', 'No email found')
                st.write(f"Logged in as: {user_email}")

if 'user' in st.session_state:
    st.write(f"Welcome {st.session_state['user'].get('email', 'Unknown User')}!")
else:
    handle_redirect()
