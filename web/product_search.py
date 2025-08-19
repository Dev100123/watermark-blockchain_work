import streamlit as st
from blockchain.blockchain import get_all_products
from web.utils import display_product
from web.video_hash import hash_video_file
from web.model import build_model, predict_video_class

# This module handles the product search functionality in the Streamlit app.
def product_search():
    # Inject CSS for sidebar layout
    st.markdown("""
        <style>
            [data-testid="stSidebar"] > div:first-child {
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .user-info-block {
                margin-top: auto;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown(
            f"""
            <style>
                .user-info-card {{
                    background: linear-gradient(135deg, #93DA97, #6BCF77);
                    padding: 1rem;
                    border-radius: 12px;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                    margin-top: 20px;
                    color: #222;
                    font-family: 'Segoe UI', sans-serif;
                }}
                .user-info-card h4 {{
                    margin: 0 0 0.5rem 0;
                    font-size: 20px;
                    display: flex;
                    align-items: center;
                    gap: 0.4rem;
                }}
                .user-info-card p {{
                    margin: 0;
                    font-size: 16px;
                    font-weight: 500;
                }}
                .username-badge {{
                    background-color: #262730;
                    color: #FAFAFA;
                    padding: 4px 8px;
                    border-radius: 6px;
                    font-family: monospace;
                    white-space: nowrap;
                }}
            </style>

            <div class="user-info-card">
                <h4>👤 Logged In</h4>
                <p><strong>User:</strong> <span class="username-badge">{st.session_state.username}</span></p>
            </div>
            """,
            unsafe_allow_html=True
        )


        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Main content
    st.title(':violet[Blockchain] Video Watermark Originality Check')

    # File uploader for video
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

    if uploaded_file:
        # Generate hash from uploaded video
        video_hash = hash_video_file(uploaded_file)

        # Search for matching product
        products = get_all_products()
        match = next((p for p in products if p[0] == video_hash), None)

        if match:
            st.success("✅ Video Found on Blockchain")
            st.session_state.matched_product = match
            display_product(match)
        else:
            st.error("❌ No Video Found on Blockchain.")
            
            # Ask user if they want to check the video
            st.write("Do you want to check by model if the video is Orginal or has a watermark?")
            
            if st.button("Check Video"):
                # Run watermark detection
                model = build_model()
                model.load_weights(r".\model\watermark_video_model_-6.h5")
                pred_class, pred_prob = predict_video_class(uploaded_file, model)
                if pred_prob >= 0.9:
                    st.success(f"✅ This video has a **{pred_class}**.")
                else:
                    st.success(f"ℹ️ This video is likely **{pred_class}**.")


