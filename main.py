import streamlit as st
from msal import PublicClientApplication

# Configure your MSAL client
CLIENT_ID = 'Your-Application-Client-ID'
AUTHORITY_URL = 'https://login.microsoftonline.com/Your-Tenant-ID'
SCOPES = ['User.Read']  # This scope allows reading user profile data

msal_app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY_URL)

# Authentication functions
def authenticate():
    session = st.session_state.get('auth_session', None)
    if not session:
        # Generate a login session
        flow = msal_app.initiate_auth_code_flow(SCOPES, redirect_uri="http://localhost:8501/login")
        st.session_state['auth_flow'] = flow
        st.write('Please log in:', flow['auth_uri'])
    elif 'user' in session:
        st.write(f'Welcome {session["user"].get("preferred_username")}')

# Redirect handling route (you would need to manage routing and states appropriately)
def login_callback():
    flow = st.session_state.get('auth_flow', None)
    if flow:
        result = msal_app.acquire_token_by_auth_code_flow(flow, st.experimental_get_query_params())
        if 'id_token_claims' in result:
            st.session_state['auth_session'] = {'user': result['id_token_claims']}
            st.experimental_rerun()

st.button("Login", on_click=authenticate)
if 'auth_session' in st.session_state:
    authenticate()