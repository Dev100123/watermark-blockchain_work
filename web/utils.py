import streamlit as st

def display_product(match, container=st):
    container.markdown("---")
    container.markdown(
        f"""
        <style>   
            .certificate-container {{
                background-color: #1a1a1a;
                color: #ffffff;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.3);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: auto;
                border: 2px solid #4CAF50;
            }}
            .cert-title {{
                color: #4CAF50;
                font-size: 24px;
                text-align: center;
                margin-bottom: 20px;
            }}
            .cert-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 12px;
            }}
            .cert-label {{
                font-weight: bold;
                color: #ccc;
                min-width: 140px;
            }}
            .cert-value {{
                color: #fff;
                word-break: break-all;
            }}
            .footer-note {{
                margin-top: 25px;
                font-size: 0.9em;
                color: #aaa;
                text-align: center;
                border-top: 1px dashed #444;
                padding-top: 15px;
            }}
        </style>

        <div class="certificate-container">
            <div class="cert-title">🔐 Smart Contract Certificate</div>
            <div class="cert-row"><span class="cert-label">🆔 Hash ID:</span><span class="cert-value">{match[0]}</span></div>
            <div class="cert-row"><span class="cert-label">🏷️ Name Registration:</span><span class="cert-value">{match[1]}</span></div>
            <div class="footer-note">
                This certificate is permanently recorded on the blockchain and cannot be altered.
                <br/>
                ⚙️ Verified via decentralized smart contract.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
