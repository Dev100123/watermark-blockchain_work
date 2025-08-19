import streamlit as st
import pyrebase
import requests 
from contract.compile_contract import compile_contract
from contract.deploy_contract import deploy_contract, is_contract_deployed
from blockchain.log_excel_to_blockchain import sync_excel_to_blockchain
from web.product_search import product_search
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv
import os

load_dotenv()  

# Initialize Firebase only once
cred = credentials.Certificate(r".\credential\blockchainauth-62dc6-619d33475cd0.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
}

firebase = pyrebase.initialize_app(firebase_config)
pb_auth = firebase.auth()


# Page config
st.set_page_config(page_title="📦 Blockchain Watermark", layout="centered", initial_sidebar_state="expanded")



st.markdown("""
    <style>

        [data-testid="stHeader"] {
            visibility: hidden;  /* Dark blue header */   
        }       

        [data-testid="stSidebar"] {
            background-color: #3E5F44;
        }
                
    </style>
""", unsafe_allow_html=True)



# Ensure smart contract is ready
@st.cache_resource
def ensure_contract_is_ready():
    if not is_contract_deployed():
        compile_contract()
        deploy_contract()
        sync_excel_to_blockchain()
        return "deployed"
    else:
        return "already_deployed"

ensure_contract_is_ready()
# sync_excel_to_blockchain()

# 🔐 LOGIN FLOW MANAGEMENT
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if st.session_state.is_logged_in:
    # ✅ Show hash_search page AFTER login
    # st.toast(f"Welcome, {st.session_state.username}!")
    
    # # Run sync logic once per session
    # if "has_synced" not in st.session_state:
    #     sync_excel_to_blockchain()
    #     st.session_state.has_synced = True

    sync_excel_to_blockchain()
    # Initialize product match state
    if "matched_product" not in st.session_state:
        st.session_state.matched_product = None

    # Show the search UI
    product_search()

else:
    st.title('Welcome to :violet[Media Integrity]')
    # st.markdown(
    #  '📦 Welcome to <span style="color: violet; font-size: 30px;">Blockchain Watermark Checking</span>',
    #  unsafe_allow_html=True
    # )

    with st.expander("🔑 Enter Credentials", expanded=True):
        choice = st.selectbox("Select an option", ["Login", "Sign Up"])

        # --- Login ---
        if choice == "Login":
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if email and password:
                    try:
                        user = pb_auth.sign_in_with_email_and_password(email, password)
                        account_info = pb_auth.get_account_info(user['idToken'])
                        display_name = account_info['users'][0].get('displayName', 'User')

                        st.session_state.username = display_name
                        st.session_state.useremail = email
                        st.session_state.is_logged_in = True
                        st.toast(f"Welcome, {display_name}!")
                        sync_excel_to_blockchain()
                        st.rerun()

                    except requests.exceptions.HTTPError as e:
                        st.error("Invalid email or password.")  
                else:
                    st.warning("Please enter both email and password.")

        # --- Sign Up ---
        else:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            username = st.text_input("Username")

            if st.button("Create My Account"):
                if email and password and username:
                    try:
                        # Check if user already exists
                        try:
                            auth.get_user_by_email(email)
                            st.error("This email is already registered. Please log in instead.")
                        except auth.UserNotFoundError:
                            # If not found, create new user
                            user = auth.create_user(
                                email=email,
                                password=password,
                                display_name=username
                            )
                            st.success(f"Account created for {user.display_name}!")
                            st.markdown("You can now log in with your credentials.")
                    except Exception as e:
                        st.error(f"Failed to create account: {str(e)}")
                else:
                    st.warning("Please fill out all fields.")  # Please thank us if you like this project work. Rock On!
