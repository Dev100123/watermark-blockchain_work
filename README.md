# 🧱  Watermark+Blockchain

This Project is designed to showcase the integration of blockchain technology with the watermark video. It uses a Solidity smart contract (`ProductTracker.sol`) to track the video information on a blockchain network. The project includes scripts for compiling, deploying, and interacting with the smart contract, as well as a tool to log data from an Excel sheet onto the blockchain.


## 🧱 Directory Layout
<code>
📁 BLOCKCHAIN_PROJECT/
├─ 📄 blockchain/
│   └─ 🔗 blockchain.py (Blockchain Interaction)
│   └─ 📥 log_excel_to_blockchain.py
├─ 📄 contract/
│   └─ 🛠️ compile_contract.py
│   └─ 🚀 deploy_contract.py
│   └─ 💻 ProductTracker.sol (Smart Contract)
├─ 📄 data/
│   └─ 📊 datasheet.xlsx (Input Data)
├─ 📄 web/
│   └─ 🤖 model.py (classify video using model)  
│   └─ 🤖 product_search.py (Search video information on blockchain)
│   └─ 🤖 hash_search.py (Search product using hash)
│   └─ 🤖 utils.py (Streamlit Interface)
│   └─ 🤖 video_hash.py (Generate unique hash)
├─ 🎯 main.py (Entry Point)
└─ 📦 requirements.txt (Dependencies)
</code> 


## 📦 Installation

```python
https://github.com/Dev100123/watermark-blockchain_work.git
cd watermark-blockchain_work
pip install -r requirements.txt
```

## ⚙️ Usage

### 1. 📦 Install Ganache
First, download and install Ganache (a personal Ethereum blockchain for local development):

[🔗 Download Ganache](https://archive.trufflesuite.com/ganache/)

Once installed:
- Open ***Ganache***
- Click on the ***Quickstart*** button to launch a local blockchain

### 2. 🖥️ Run the Streamlit App
Finally, launch the web interface using Streamlit:
```python
streamlit run main.py
```

Open the provided link in your browser to interact with your watermark+blockchain application!

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

### What does the MIT License allow?

The MIT License is a permissive open-source license that allows:
- Free use, copy, modify, and distribute the software
- Commercial use
- No warranty provided ("as is")

🔗 [More about the MIT License](https://opensource.org/licenses/MIT) 
