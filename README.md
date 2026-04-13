# 🛡 Detectra  
## Multilingual Scam Detection using Explainable AI (XAI)

AI-powered platform for detecting scam SMS messages and call transcripts with explainable insights using modern NLP and deep learning techniques.

---

## 📌 Problem Statement

With the rapid growth of digital communication, scam messages and fraudulent calls have increased significantly. These scams often attempt to steal sensitive information such as OTPs, bank details, or personal data.

Existing systems only classify messages as spam without providing any explanation, leading to low user trust and lack of awareness.

---

## 💡 Solution

Detectra is an AI-powered system that:

- Detects scam messages using deep learning  
- Supports multilingual inputs  
- Provides explainable predictions using XAI (LIME)  
- Improves user awareness and trust  

---

## 🚀 Features

### 📩 Input Handling
- SMS message input  
- Voice-based input (call simulation)  

### 🌐 Multilingual Support
- English  
- Hindi  
- Kannada  
- Tamil  
- Hinglish  

### 🤖 Scam Detection
- DistilBERT-based classification  
- Scam / Genuine prediction  
- Confidence score  

### 🧠 Explainable AI (XAI)
- LIME-based explanation  
- Highlights important words influencing prediction  

### ⚠️ Scam Categorization
- OTP Fraud  
- Phishing  
- KYC Scam  
- Banking Scam  
- Lottery Scam  

### 📊 Analytics Dashboard
- Total messages processed  
- Scam vs Genuine distribution  
- Pie chart visualization  

### 📄 Report Generation
- Downloadable report  
- Includes predictions and logs  

### 🔐 Cybersecurity Measures
- Alerts for risky messages  
- Safe usage suggestions  

---

## 🧠 Tech Stack

- DistilBERT (Transformer Model)  
- LIME (Explainable AI)  
- Streamlit (Frontend)  
- Python (Backend)  

---

## 🏗 Architecture
User Input (Text / Voice)
↓
Translation (Multilingual → English)
↓
Tokenizer (DistilBERT)
↓
Classification Model
↓
Prediction (Scam / Genuine)
↓
LIME Explanation
↓
UI Output + Analytics + Report

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py

⚠️ Note on Large Files
Some project files (such as trained model files and datasets) exceed GitHub's file size limit (25MB), so they are not included in this repository.

You can access them here:
👉 https://drive.google.com/drive/folders/1BTA7i-Cg366HWbk2lI1SwudTW7jOLcpH?usp=sharing

---

📌 Overview

Detectra is an AI-based system that detects scam messages using DistilBERT and explains predictions using LIME.

---

👨‍💻 Contributors
Monica D
Akshatha G Dhongadi
Naolin Gregory Vaz
Manasavi

---

🎯 Conclusion

Detectra combines Artificial Intelligence, cybersecurity, and explainability to create a reliable and transparent scam detection system. It enhances digital safety, builds user trust, and promotes awareness in modern communication systems.
