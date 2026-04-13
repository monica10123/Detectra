# =========================================================
# 🛡 DETECTRA - AI Scam Detection System (FINAL UI VERSION)
# =========================================================

# ---------------- IMPORT LIBRARIES ----------------
import streamlit as st
import torch
import speech_recognition as sr
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from deep_translator import GoogleTranslator
from collections import Counter
from lime.lime_text import LimeTextExplainer

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="DETECTRA", page_icon="🛡", layout="wide")

# ---------------- CUSTOM UI STYLING ----------------
st.markdown("""
<style>

/* -------- BACKGROUND -------- */
body {
    background: linear-gradient(to right, #f0f9ff, #fef9ff);
    font-family: 'Times New Roman', serif;
}

/* -------- TITLE -------- */
h1 {
    color: #1e293b;
}
p {
    color: #64748b;
}

/* -------- RADIO BUTTON -------- */
.stRadio > div {
    background-color: #f1f5f9;
    padding: 10px;
    border-radius: 10px;
}

/* -------- SELECTBOX -------- */
.stSelectbox > div > div {
    border-radius: 10px;
    background-color: #f1f5f9;
}

/* -------- TEXT INPUT -------- */
.stTextInput > div > div > input {
    border-radius: 10px;
    background-color: #f8fafc;
    padding: 8px;
}

/* -------- BUTTON -------- */
.stButton > button {
    background: #151B54;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 600;
    border: none;
}


/* -------- RESULT COLORS -------- */
.scam {
    background: #fee2e2;
    color: #b91c1c;
    padding: 12px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: bold;
}

.genuine {
    background: #dcfce7;
    color: #15803d;
    padding: 12px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: bold;
}

/* -------- LIME TAGS -------- */
.tag {
    display: inline-block;
    padding: 5px 10px;
    margin: 4px;
    border-radius: 20px;
    background: #e0f2fe;
    color: #0369a1;
    font-size: 13px;
}

.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
}

/* -------- HEADINGS -------- */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #151B54;
    margin-top: 15px;
}
            
/* -------- DOWNLOAD BUTTON -------- */
div.stDownloadButton > button {
    background: #151B54;
    color: white;
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 600;
}

div.stDownloadButton > button:hover {
    background: #059669;
}

/* -------- HORIZONTAL LINE -------- */
hr {
    border: none;
    height: 1px;
    background: #e5e7eb;
}

</style>
""", unsafe_allow_html=True)
# ---------------- TITLE ----------------
st.markdown("""
<div style='
    background: #151B54;
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 20px;
'>
    <h1 style='color: white; font-size: 55px; margin-bottom: 5px;'>🛡 DETECTRA</h1>
    <p style='color: #e0f2fe; font-size:16px;'>XAI Powered Multilingual Scam Detector</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 🤖 MODEL LOADING
# =========================================================
@st.cache_resource
def load_model():
    tokenizer = DistilBertTokenizerFast.from_pretrained("./distilbert_model")
    model = DistilBertForSequenceClassification.from_pretrained("./distilbert_model")
    model.eval()
    model.to("cpu")
    return model, tokenizer

model, tokenizer = load_model()

# =========================================================
# 🌍 TRANSLATION
# =========================================================
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

# =========================================================
# 🎤 VOICE INPUT
# =========================================================
def get_voice_input(lang):
    r = sr.Recognizer()
    r.pause_threshold = 2.5
    with sr.Microphone() as source:
        st.write("🎤 Speak now...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio, language=lang)
    except:
        return ""
# =========================================================
# 🧠 SCAM CATEGORY DETECTOR
# =========================================================
def get_scam_type(text):
    t = text.lower()

    if "otp" in t:
        return "OTP Fraud"
    elif "kyc" in t:
        return "KYC Scam"
    elif "lottery" in t or "reward" in t:
        return "Lottery Scam"
    elif "link" in t or "click" in t:
        return "Phishing Scam"
    elif "bank" in t or "account" in t:
        return "Banking Scam"
    else:
        return "General Scam"

# =========================================================
# 📊 PATTERN DETECTION
# =========================================================
def detect_patterns(text):
    t = text.lower()
    patterns = []
    if "otp" in t: patterns.append("OTP Request")
    if "urgent" in t: patterns.append("Urgency")
    if "click" in t or "link" in t: patterns.append("Suspicious Link")
    if "bank" in t: patterns.append("Financial Target")
    return patterns

# =========================================================
# 🧠 LIME EXPLAINER (REAL XAI)
# =========================================================
explainer = LimeTextExplainer(class_names=["GENUINE", "SCAM"])

def lime_explain(text):
    def predict_proba(texts):
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1).numpy()
        return probs

    exp = explainer.explain_instance(text, predict_proba, num_features=6)
    return exp.as_list()

# =========================================================
# 📄 REPORT GENERATION
# =========================================================
def generate_report(df):

    file_path = "detectra_report.txt"

    total = len(df)
    scam_count = len(df[df["Result"] == "SCAM"])
    genuine_count = len(df[df["Result"] == "GENUINE"])

    with open(file_path, "w", encoding="utf-8") as f:

        # ================= HEADER =================
        f.write("🛡 DETECTRA Scam Detection Report\n")
        f.write("============================================\n\n")

        # ================= SUMMARY =================
        f.write("📊 SUMMARY\n")
        f.write("--------------------------------------------\n")
        f.write(f"Total Messages: {total}\n")
        f.write(f"Scam Detected: {scam_count}\n")
        f.write(f"Genuine Messages: {genuine_count}\n\n")

        # ================= DETAILED LOG =================
        f.write("📜 DETAILED ANALYSIS\n")
        f.write("============================================\n\n")

        for i, row in df.iterrows():

            message = str(row["Message"]) if str(row["Message"]).strip() else "[Empty]"

            # 🔥 LIME EXPLANATION FOR REPORT
            translated_text = translate_to_english(message)
            lime_results = lime_explain(translated_text)

            f.write(f"[Message {i+1}]\n")
            f.write(f"Time: {row['Time']}\n")
            f.write(f"Message: {message}\n")
            f.write(f"Result: {row['Result']}\n")

            # 🔥 ADD LIME OUTPUT
            f.write("LIME Explanation:\n")
            for word, weight in lime_results:
                f.write(f"  {word} → {round(weight,3)}\n")

            f.write("\n--------------------------------------------\n\n")

    return file_path

# =========================================================
# 💾 SESSION STATE
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = []
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

# =========================================================
# 📥 INPUT SECTION
# =========================================================

st.markdown("<div class='section-title'>📥 INPT SECTION</div>", unsafe_allow_html=True)

input_type = st.radio("Select Input Type", ["SMS Message","Call (Voice Input)"])
lang = st.selectbox("🌍 Language", ["Select Language", "English", "Hindi", "Hinglish", "Kannada", "Tamil"])
lang_map = {"English":"en-IN","Hindi":"hi-IN","Kannada":"kn-IN","Tamil":"ta-IN"}



if input_type == "SMS Message":
    st.session_state.voice_text = ""
    message = st.text_input("Enter message...")
else:
    if st.button("🎤 Record Voice"):
        st.session_state.voice_text = get_voice_input(lang_map[lang])
    if st.session_state.voice_text:
        st.write("📝", st.session_state.voice_text)
    message = st.session_state.voice_text

analyze = st.button("🚀 Detect Scam")
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# 🔍 OUTPUT SECTION
# =========================================================
if analyze and message.strip():

    translated = translate_to_english(message)

    inputs = tokenizer(translated, return_tensors="pt", truncation=True, padding=True, max_length=128)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        prob = probabilities[0][1].item()

    verdict = "SCAM" if prob > 0.5 else "GENUINE"

    st.session_state.history.append({
        "Time": datetime.now().strftime("%H:%M"),
        "Message": message,
        "Result": verdict
    })

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔍 DETECTION RESULT</div>", unsafe_allow_html=True)

    
    # ================= SCAM CATEGORY (ADD THIS) =================
    if verdict == "SCAM":
        st.markdown(f"<div class='scam'>🚨 SCAM ({prob*100:.2f}%)</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='genuine'>✅ GENUINE ({(1-prob)*100:.2f}%)</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)

    # =====================================================
    # 🧠 LIME EXPLANATION (ONLY XAI)
    # =====================================================
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🧠 LIME (XAI)</div>", unsafe_allow_html=True)
    lime_results = lime_explain(translated)

    lime_data = lime_explain(translated)
    lime_data = lime_explain(translated)
    lime_df = pd.DataFrame(lime_data, columns=["Word", "Impact"])

    # index from 1
    lime_df.index += 1
    
    # round values
    lime_df["Impact"] = lime_df["Impact"].round(3)

    # convert to string to avoid right align
    lime_df["Impact"] = lime_df["Impact"].astype(str)

    # styling
    styled_df = lime_df.style \
        .set_properties(subset=["Impact"], **{'text-align': 'left'}) \
        .set_table_styles([
            {
                'selector': 'th.col_heading',
                'props': [
                    ('text-align', 'center'),
                    ('font-weight', 'bold')
                ]
            }
        ])

    # center layout
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h4 style='text-align:center; font-weight:bold;'>Important Words (LIME)</h4>", unsafe_allow_html=True)
        st.write(styled_df)
    # =====================================================
    # 🔐 CYBERSECURITY ADVICE (ADDED)
    # =====================================================
    if verdict == "SCAM":
        st.markdown("<h4 style='font-weight:bold;'>🛡 Cyber Security Measures</h4>", unsafe_allow_html=True)
    
        st.warning("⚠️ Do NOT share OTP or personal details.")
        st.warning("⚠️ Avoid clicking unknown links.")
        st.warning("⚠️ Verify messages through official sources.")
    else:
        st.success("✅ Message appears safe.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# 🌐 MESSAGE UNDERSTANDING (RESTORED)
# =========================================================

if analyze and message.strip():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🌐 MESSAGE </div>", unsafe_allow_html=True)

    st.write("📝 Original Text:", message)
    st.write("🌍 Translated Text:", translated)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# 📊 ANALYTICS + HISTORY
# =========================================================
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 ANALYTICS</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='line-height:2'>
    📨<b>Total:</b> {len(df)}<br>
    🚨 <b>Scam:</b> {len(df[df['Result']=='SCAM'])}<br>
    ✅ <b>Genuine:</b> {len(df[df['Result']=='GENUINE'])}
    </div>
    """, unsafe_allow_html=True)

    scam_count = len(df[df["Result"]=="SCAM"])
    genuine_count = len(df[df["Result"]=="GENUINE"])

    if scam_count == 0:
        labels = ['GENUINE']
        sizes = [genuine_count]
    elif genuine_count == 0:
        labels = ['SCAM']
        sizes = [scam_count]
    else:
        labels = ['SCAM','GENUINE']
        sizes = [scam_count,genuine_count]

    # ---------------- FINAL PIE CHART ----------------
    col1, col2 = st.columns([1,3])

    with col1:
        fig, ax = plt.subplots(figsize=(3,3))

        counts = df["Result"].value_counts()

        labels = counts.index.tolist()
        sizes = counts.values

        colors = ['#151B54', "#6495ED"]  # dark blue, light blue

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,              # label inside
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={'edgecolor': 'white'}
        )

        # make text white for better visibility
        for text in texts:
            text.set_color('white')
            text.set_fontsize(9)

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)

        # legend on side
        ax.legend(wedges, labels, title="Type", loc="center left", bbox_to_anchor=(1, 0.5))

        ax.set_title("Distribution", fontsize=10)

        st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

    file = generate_report(df)
    with open(file, "rb") as f:
        st.download_button("📄 Download Report", f, file_name="detectra_report.txt", mime="text/plain")

    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📜 HISTORY</div>", unsafe_allow_html=True)
    df_display = df.copy()
    df_display.index = df_display.index + 1
    st.dataframe(
        df_display.style.set_table_styles([
            {'selector': 'th', 'props': [
                ('text-align', 'center'),
                ('font-weight', 'bold')
            ]},
            {'selector': 'td', 'props': [
                ('background-color', '#eef2ff'),
                ('color', 'black')
            ]}
        ]),
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)