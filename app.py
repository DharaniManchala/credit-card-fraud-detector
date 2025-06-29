
# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import joblib
# import os
# import tempfile
# from datetime import datetime
# from fpdf import FPDF
# import numpy as np

# model = joblib.load("model/fraud_model.pkl")
# scaler = joblib.load("model/scaler.pkl")

# HISTORY_FOLDER = "history"
# os.makedirs(HISTORY_FOLDER, exist_ok=True)

# st.set_page_config(page_title="Smart Fraud Detection App", layout="wide")

# # --- Styling ---
# st.markdown("""
# <style>
# body {
#     background-color: #f7f9fa;
#     font-family: 'Segoe UI', sans-serif;
# }
# .stButton>button, .stDownloadButton>button {
#     background-color: #006400;
#     color: white;
#     font-size: 18px;
#     font-weight: bold;
#     border-radius: 12px;
#     padding: 14px 36px;
#     transition: all 0.3s ease;
#     width: 100%;
# }
# .stButton>button:hover, .stDownloadButton>button:hover {
#     background-color: #004d00;
#     transform: scale(1.05);
# }
# .header {
#     background-color: #006400;
#     color: white;
#     padding: 40px;
#     border-radius: 12px;
#     text-align: center;
#     margin-bottom: 30px;
#     font-size: 32px;
# }
# .main-cover {
#     background-color: #d9f2e3;
#     padding: 80px;
#     border-radius: 12px;
#     text-align: center;
#     font-size: 24px;
#     margin-bottom: 40px;
# }
# </style>
# """, unsafe_allow_html=True)

# # --- Session State ---
# if "auth" not in st.session_state:
#     st.session_state.auth = False
# if "users" not in st.session_state:
#     st.session_state.users = {}
# if "email" not in st.session_state:
#     st.session_state.email = ""
# if "page" not in st.session_state:
#     st.session_state.page = "main"

# # --- PDF Generation ---
# class PDF(FPDF):
#     def header(self):
#         self.set_font("Arial", "B", 14)
#         self.cell(0, 10, "Fraud Detection Report", ln=True, align="C")
#     def footer(self):
#         self.set_y(-15)
#         self.set_font("Arial", "I", 8)
#         self.cell(0, 10, f"Page {self.page_no()}", align="C")

# def generate_pdf(df, user_email, frauds):
#     pdf = PDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt=f"User: {user_email}", ln=True)
#     pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
#     pdf.cell(200, 10, txt=f"Total Rows: {len(df)}", ln=True)
#     pdf.cell(200, 10, txt=f"Frauds Detected: {frauds}", ln=True)
#     pdf.ln()
#     for i, row in df.head(10).iterrows():
#         pdf.cell(200, 10, txt=f"Amount: {row['Amount']}, Fraud_Prob: {row['Fraud_Prob']}, Prediction: {row['Prediction']}", ln=True)
#     temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
#     pdf.output(temp_pdf.name)
#     return temp_pdf.name

# # --- Pages ---
# def main_page():
#     st.markdown("""
#     <div class="main-cover">
#         <h1>Smart Fraud Detection App</h1>
#         <p>Detect fraudulent transactions using <span style='color: teal;'>advanced machine learning techniques</span>.</p>
#     </div>
#     """, unsafe_allow_html=True)
#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col1:
#         if st.button("📝 Sign Up"):
#             st.session_state.page = "signup"
#     with col2:
#         if st.button("🔐 Login"):
#             st.session_state.page = "login"
#     with col3:
#         if st.button("ℹ️ About"):
#             st.session_state.page = "about"

# def signup_page():
#     st.markdown("<div class='header'><h2>Sign Up</h2></div>", unsafe_allow_html=True)
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Register"):
#         if email in st.session_state.users:
#             st.warning("User already exists. Please log in.")
#         elif email and password:
#             st.session_state.users[email] = password
#             st.success("Registered! Please log in.")
#             st.session_state.page = "login"
#         else:
#             st.error("All fields required.")
#     if st.button("⬅️ Back"):
#         st.session_state.page = "main"

# def login_page():
#     st.markdown("<div class='header'><h2>Login</h2></div>", unsafe_allow_html=True)
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         if email in st.session_state.users and st.session_state.users[email] == password:
#             st.success("Login successful.")
#             st.session_state.auth = True
#             st.session_state.email = email
#         elif email in st.session_state.users:
#             st.error("Invalid credentials.")
#         else:
#             st.error("User not found.")
#     if st.button("⬅️ Back"):
#         st.session_state.page = "main"

# def about_page():
#     st.markdown("""
#     <div class='header'><h2>About</h2></div>
#     <p>This app uses machine learning to filter credit card fraud and identify it accurately.</p>
#     <p><strong>Dataset</strong>: Built using anonymized credit card transaction data.</p>
#     <p><strong>Model</strong>: Trained classification model using Python & Scikit-learn.</p>
#     """, unsafe_allow_html=True)
#     if st.button("⬅️ Back"):
#         st.session_state.page = "main"

# def detect_fraud():
#     st.markdown("<div class='header'><h2>Detect Fraud</h2></div>", unsafe_allow_html=True)
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         if st.button("⬅️ Back"):
#             st.session_state.auth = False
#             st.session_state.page = "main"
#     with col2:
#         if st.button("Previous History"):
#             history_files = sorted(
#                 [f for f in os.listdir(HISTORY_FOLDER) if f.startswith(st.session_state.email)],
#                 reverse=True
#             )
#             if not history_files:
#                 st.info("No history files found.")
#             else:
#                 selected_file = st.selectbox("Select a file to view", history_files)
#                 file_path = os.path.join(HISTORY_FOLDER, selected_file)
#                 df_prev = pd.read_csv(file_path)
#                 st.dataframe(df_prev.head(20))
#                 with open(file_path, "rb") as f:
#                     st.download_button("Download Selected CSV", f.read(), file_name=selected_file)
#     with col3:
#         if st.button("Clear History"):
#             for file in os.listdir(HISTORY_FOLDER):
#                 if file.startswith(st.session_state.email):
#                     os.remove(os.path.join(HISTORY_FOLDER, file))
#             st.success("History cleared!")

#     uploaded_file = st.file_uploader("Upload CSV File", type="csv")
#     threshold = st.slider("Prediction Threshold", 0.0, 1.0, 0.5, 0.01)

#     if uploaded_file:
#         df = pd.read_csv(uploaded_file)
#         if 'Class' in df.columns:
#             df.drop('Class', axis=1, inplace=True)
#         expected = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
#         if not all(col in df.columns for col in expected):
#             st.error("Missing required columns")
#             return

#         df = df[expected]
#         X_scaled = scaler.transform(df)
#         proba = model.predict_proba(X_scaled)[:, 1]
#         prediction = (proba >= threshold).astype(int)

#         df['Prediction'] = prediction
#         df['Fraud_Prob'] = proba.round(4)
#         frauds = sum(prediction)

#         suggested_thresh = round(np.percentile(proba, 95), 2)
#         st.info(f"💡 Suggestion: Try increasing the threshold to ~{suggested_thresh} to reduce false positives.")

#         st.success(f"Frauds detected: {frauds} / {len(prediction)}")
#         st.dataframe(df.head())

#         timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         filename = f"{HISTORY_FOLDER}/{st.session_state.email}_{timestamp}.csv"
#         df.to_csv(filename, index=False)

#         st.download_button("Download CSV", df.to_csv(index=False), file_name="fraud_results.csv")
#         pdf_path = generate_pdf(df, st.session_state.email, frauds)
#         with open(pdf_path, "rb") as f:
#             st.download_button("Download PDF Report", data=f.read(), file_name="fraud_report.pdf")

#         st.markdown("""
#         <h4>Share Report:</h4>
#         <a href='mailto:?subject=Fraud Detection Report&body=Report attached.'><button>📧 Email</button></a>
#         <a href='https://wa.me/?text=Check%20out%20this%20Fraud%20Detection%20report!' target='_blank'><button>💬 WhatsApp</button></a>
#         """, unsafe_allow_html=True)

#         st.subheader("📊 Visual Insights")
#         col1, col2 = st.columns(2)
#         with col1:
#             pie_data = df['Prediction'].value_counts().sort_index()
#             labels = ['Legit', 'Fraud'][:len(pie_data)]
#             fig1, ax1 = plt.subplots()
#             ax1.pie(pie_data, labels=labels, autopct='%1.1f%%', colors=['green', 'red'])
#             ax1.axis('equal')
#             st.pyplot(fig1)
#         with col2:
#             fig2, ax2 = plt.subplots()
#             sns.histplot(df[df['Prediction'] == 0]['Amount'], color="green", label="Legit", kde=True)
#             sns.histplot(df[df['Prediction'] == 1]['Amount'], color="red", label="Fraud", kde=True)
#             ax2.set_title("Amount Distribution")
#             plt.legend()
#             st.pyplot(fig2)

#         fig3, ax3 = plt.subplots()
#         sns.heatmap(df.corr(), cmap='coolwarm', ax=ax3)
#         ax3.set_title("Feature Correlation")
#         st.pyplot(fig3)

#         fig4, ax4 = plt.subplots()
#         df['Hour'] = (df['Time'] // 3600) % 24
#         sns.countplot(x='Hour', hue='Prediction', data=df, palette={0: 'green', 1: 'red'}, ax=ax4)
#         ax4.set_title("Hourly Fraud Pattern")
#         st.pyplot(fig4)

#         fig5, ax5 = plt.subplots()
#         df['log_amount'] = df['Amount'].apply(lambda x: np.log1p(x))
#         sns.kdeplot(data=df, x='log_amount', hue='Prediction', fill=True, common_norm=False, palette={0: 'green', 1: 'red'}, ax=ax5)
#         ax5.set_title("Log Amount Distribution")
#         st.pyplot(fig5)

# # --- Routing ---
# if not st.session_state.auth:
#     if st.session_state.page == "main":
#         main_page()
#     elif st.session_state.page == "signup":
#         signup_page()
#     elif st.session_state.page == "login":
#         login_page()
#     elif st.session_state.page == "about":
#         about_page()
# else:
#     detect_fraud()


from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import os
import tempfile
from datetime import datetime
from fpdf import FPDF
import numpy as np
import json
import hashlib
import shap
import plotly.express as px



# --- Load Models ---
model = joblib.load("model/fraud_model.pkl")
scaler = joblib.load("model/scaler.pkl")

# --- Folder Setup ---
HISTORY_FOLDER = "history"
USER_FILE = "users.json"
os.makedirs(HISTORY_FOLDER, exist_ok=True)

# --- Load/Save Users ---
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# --- Styling ---
st.set_page_config(page_title="Smart Fraud Detection App", layout="wide")
st.markdown("""
<style>
body {
    background-color: #f7f9fa;
    font-family: 'Segoe UI', sans-serif;
}
.stButton>button, .stDownloadButton>button {
    background-color: #006400;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    padding: 14px 36px;
    transition: all 0.3s ease;
    width: 100%;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    background-color: #004d00;
    transform: scale(1.05);
}
.header {
    background-color: #006400;
    color: white;
    padding: 40px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 30px;
    font-size: 32px;
}
.main-cover {
    background-color: #d9f2e3;
    padding: 80px;
    border-radius: 12px;
    text-align: center;
    font-size: 24px;
    margin-bottom: 40px;
}
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "auth" not in st.session_state:
    st.session_state.auth = False
if "users" not in st.session_state:
    st.session_state.users = load_users()
if "email" not in st.session_state:
    st.session_state.email = ""
if "page" not in st.session_state:
    st.session_state.page = "main"

# --- PDF Report Generator ---
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Fraud Detection Report", ln=True, align="C")
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(df, user_email, frauds):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"User: {user_email}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(200, 10, txt=f"Total Rows: {len(df)}", ln=True)
    pdf.cell(200, 10, txt=f"Frauds Detected: {frauds}", ln=True)
    pdf.ln()
    for i, row in df.head(10).iterrows():
        pdf.cell(200, 10, txt=f"Amount: {row['Amount']}, Fraud_Prob: {row['Fraud_Prob']}, Prediction: {row['Prediction']}", ln=True)
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)
    return temp_pdf.name

# --- Pages ---
def main_page():
    st.markdown("""
    <div class="main-cover">
        <h1>Smart Fraud Detection App</h1>
        <p>Detect fraudulent transactions using <span style='color: teal;'>advanced machine learning techniques</span>.</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Sign Up"):
            st.session_state.page = "signup"
    with col2:
        if st.button("🔐 Login"):
            st.session_state.page = "login"
    with col3:
        if st.button("ℹ️ About"):
            st.session_state.page = "about"

def signup_page():
    st.markdown("<div class='header'><h2>Sign Up</h2></div>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if email in st.session_state.users:
            st.warning("User already exists. Please log in.")
        # elif email and password:
        #     st.session_state.users[email] = password
        #     save_users(st.session_state.users)
        #     st.success("Registered! Please log in.")
        #     st.session_state.page = "login"
        elif email and password:

            hashed_pw = hash_password(password)
            st.session_state.users[email] = hashed_pw
            save_users(st.session_state.users)
            st.success("Registered! Please log in.")
            st.session_state.page = "login"

        else:
            st.error("All fields required.")
    if st.button("⬅️ Back"):
        st.session_state.page = "main"

def login_page():
    st.markdown("<div class='header'><h2>Login</h2></div>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    # if st.button("Login"):
    #     if email in st.session_state.users and st.session_state.users[email] == password:
    #         st.success("Login successful.")
    #         st.session_state.auth = True
    #         st.session_state.email = email
    #     elif email in st.session_state.users:
    #         st.error("Invalid password.")
    #     else:
    #         st.error("User not found.")
    if st.button("Login"):
       
       hashed_pw = hash_password(password)
       if email in st.session_state.users and st.session_state.users[email] == hashed_pw:

         st.success("Login successful.")
         st.session_state.auth = True
         st.session_state.email = email
       elif email in st.session_state.users:
 
         st.error("Invalid password.")
       else:
         st.error("User not found.")

    if st.button("⬅️ Back"):
        st.session_state.page = "main"

def about_page():
    st.markdown("""
    <div class='header'><h2>About</h2></div>
    <p>This app uses machine learning to detect and prevent credit card fraud in transaction datasets.</p>
    <p><strong>Model:</strong> Scikit-learn trained model</p>
    <p><strong>Dataset:</strong> Anonymized real-world transactions</p>
    """, unsafe_allow_html=True)
    if st.button("⬅️ Back"):
        st.session_state.page = "main"

def detect_fraud():
    st.markdown("<div class='header'><h2>Detect Fraud</h2></div>", unsafe_allow_html=True)
    st.markdown(f"### 👤 Welcome, `{st.session_state.email}`")

    if st.button("🚪 Logout"):
        # Delete user's history files
        for file in os.listdir(HISTORY_FOLDER):
            if file.startswith(st.session_state.email):
                os.remove(os.path.join(HISTORY_FOLDER, file))

        # Delete user credentials
        if st.session_state.email in st.session_state.users:
            del st.session_state.users[st.session_state.email]
            save_users(st.session_state.users)

        # Clear session state
        st.session_state.auth = False
        st.session_state.page = "main"
        st.session_state.email = ""
        return  # <--- this is okay here because it's at the end of the block

    # ✅ THIS CODE IS NOW REACHABLE
    col1, col2, col3 = st.columns(3)
    # rest of the code continues...

    col1, col2, col3 = st.columns(3)
    with col1:
       if st.button("⬅️ Back"):
            st.session_state.auth = False
            st.session_state.page = "main"
    with col2:
        if st.button("Previous History"):
            history_files = sorted([
                f for f in os.listdir(HISTORY_FOLDER) if f.startswith(st.session_state.email)
            ], reverse=True)
            if not history_files:
                st.info("No history files found.")
            else:
                selected_file = st.selectbox("Select a file to view", history_files)
                file_path = os.path.join(HISTORY_FOLDER, selected_file)
                df_prev = pd.read_csv(file_path)
                st.dataframe(df_prev.head(20))
                with open(file_path, "rb") as f:
                    st.download_button("Download Selected CSV", f.read(), file_name=selected_file)
    with col3:
        if st.button("Clear History"):
            for file in os.listdir(HISTORY_FOLDER):
                if file.startswith(st.session_state.email):
                    os.remove(os.path.join(HISTORY_FOLDER, file))
            st.success("History cleared!")

    uploaded_file = st.file_uploader("📁 Upload CSV File", type="csv")
    threshold = st.slider("⚙️ Prediction Threshold", 0.0, 1.0, 0.5, 0.01)

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "Class" in df.columns:
            df.drop("Class", axis=1, inplace=True)

        expected = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
        if not all(col in df.columns for col in expected):
            st.error("Missing required columns.")
            return

        df = df[expected]
        X_scaled = scaler.transform(df)
        proba = model.predict_proba(X_scaled)[:, 1]
        prediction = (proba >= threshold).astype(int)

        df["Prediction"] = prediction
        df["Fraud_Prob"] = proba.round(4)
        frauds = sum(prediction)

        st.success(f"✅ Frauds detected: {frauds} / {len(prediction)}")
        st.dataframe(df.head())

        suggested_thresh = round(np.percentile(proba, 95), 2)
        st.info(f"💡 Try using threshold ≈ {suggested_thresh} for fewer false positives.")

        # Save CSV + PDF
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{HISTORY_FOLDER}/{st.session_state.email}_{timestamp}.csv"
        df.to_csv(filename, index=False)

        st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="fraud_results.csv")

        pdf_path = generate_pdf(df, st.session_state.email, frauds)
        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ Download PDF Report", f.read(), file_name="fraud_report.pdf")
        st.markdown("""
<div style="margin-top: 30px;">
    <h4>📤 Share Your Report</h4>
    <ul>
        <li><strong>Step 1:</strong> Download the PDF or CSV file using the buttons above.</li>
        <li><strong>Step 2:</strong> Open WhatsApp or Gmail and attach the downloaded file manually.</li>
    </ul>
    <p>Or click below to open WhatsApp with a pre-filled message:</p>
    <a href='https://wa.me/?text=Hey!%20I%20just%20ran%20a%20smart%20fraud%20detection%20report.%20Check%20out%20the%20attached%20PDF%20or%20CSV!' target='_blank'>
        <button style="background-color:#25D366;color:white;padding:10px 20px;font-size:16px;border:none;border-radius:8px;cursor:pointer;">💬 Share via WhatsApp</button>
    </a>
</div>
""", unsafe_allow_html=True)


        # --- Visual Insights ---
        st.subheader("📊 Visual Insights")
        col1, col2 = st.columns(2)
        with col1:
            pie_data = df["Prediction"].value_counts().sort_index()
            labels = ["Legit", "Fraud"][:len(pie_data)]
            fig1, ax1 = plt.subplots()
            ax1.pie(pie_data, labels=labels, autopct="%1.1f%%", colors=["green", "red"])
            ax1.axis("equal")
            st.pyplot(fig1)
        with col2:
            fig2, ax2 = plt.subplots()
            sns.histplot(df[df["Prediction"] == 0]["Amount"], color="green", label="Legit", kde=True)
            sns.histplot(df[df["Prediction"] == 1]["Amount"], color="red", label="Fraud", kde=True)
            ax2.set_title("Amount Distribution")
            plt.legend()
            st.pyplot(fig2)
        # --- Additional Graphs ---
# Heatmap
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        sns.heatmap(df.corr(), cmap='coolwarm', ax=ax3)
        ax3.set_title("🔍 Feature Correlation Heatmap")
        st.pyplot(fig3)

       # Hourly Fraud Pattern
        df["Hour"] = (df["Time"] // 3600) % 24
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.countplot(x="Hour", hue="Prediction", data=df, palette={0: "green", 1: "red"}, ax=ax4)
        ax4.set_title("🕒 Hourly Fraud Pattern")
        st.pyplot(fig4)

# Log Amount Distribution
        df["log_amount"] = df["Amount"].apply(lambda x: np.log1p(x))
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        sns.kdeplot(data=df, x="log_amount", hue="Prediction", fill=True, common_norm=False, palette={0: "green", 1: "red"}, ax=ax5)
        ax5.set_title("💰 Log Amount Distribution by Class")
        st.pyplot(fig5)
        st.subheader("📊 Interactive Dashboard (Plotly)")

        # Interactive Fraud vs. Legit over Time
        fig6 = px.scatter(
            df.head(1000),  # limit to 1000 rows for speed
            x="Time",
            y="Amount",
            color=df["Prediction"].map({0: "Legit", 1: "Fraud"}),
            title="Fraud vs Legit Transactions Over Time",
            labels={"color": "Class"},
            hover_data=["Fraud_Prob"]
        )
        st.plotly_chart(fig6)

        # Interactive Boxplot for Amount by Class
        fig7 = px.box(
            df.head(1000),
            x=df["Prediction"].map({0: "Legit", 1: "Fraud"}),
            y="Amount",
            color=df["Prediction"].map({0: "Legit", 1: "Fraud"}),
            title="Amount Distribution by Class (Legit vs Fraud)",
            labels={"x": "Class"}
        )
        st.plotly_chart(fig7)



                                          # --- Manual Input Prediction ---
        st.markdown("<div class='header'><h2>🔍 Manual Transaction Prediction</h2></div>", unsafe_allow_html=True)
        st.info("Fill in the transaction details to get a fraud prediction.")

        with st.form("manual_input_form"):
            time = st.number_input("Time", min_value=0.0)
            amount = st.number_input("Amount", min_value=0.0)

            v_features = {}
            for i in range(1, 29):
                v_features[f"V{i}"] = st.number_input(f"V{i}", min_value=-100.0, max_value=100.0, step=0.1)

            submitted = st.form_submit_button("Predict")

        if submitted:
            # Create single-row dataframe
            input_data = pd.DataFrame({
                "Time": [time],
                **{k: [v] for k, v in v_features.items()},
                "Amount": [amount]
            })

            # Scale input using previously saved scaler
            input_scaled = scaler.transform(input_data)

            # Predict
            proba = model.predict_proba(input_scaled)[0][1]
            prediction = model.predict(input_scaled)[0]

            result = "🚨 Fraud" if prediction == 1 else "✅ Legit"
            st.success(f"**Prediction:** {result}")
            st.info(f"**Fraud Probability:** {proba:.4f}")

            st.markdown("<div class='header'><h2>⚖️ Model Comparison</h2></div>", unsafe_allow_html=True)
        st.info("Compare Logistic Regression and Random Forest on your uploaded data.")

        if st.button("Compare Models"):
            X = df.drop(["Prediction", "Fraud_Prob"], axis=1)
            y = prediction  # Use the prediction labels already made by the base model

            results = {}

            # Logistic Regression
            log_model = LogisticRegression(max_iter=1000)
            log_model.fit(X_scaled, y)
            y_pred_log = log_model.predict(X_scaled)
            results["Logistic Regression"] = {
                "accuracy": accuracy_score(y, y_pred_log),
                "conf_matrix": confusion_matrix(y, y_pred_log),
                "report": classification_report(y, y_pred_log, output_dict=True)
            }

            # Random Forest
            rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
            rf_model.fit(X_scaled, y)
            y_pred_rf = rf_model.predict(X_scaled)
            results["Random Forest"] = {
                "accuracy": accuracy_score(y, y_pred_rf),
                "conf_matrix": confusion_matrix(y, y_pred_rf),
                "report": classification_report(y, y_pred_rf, output_dict=True)
            }

            # Display results
            for model_name, res in results.items():
                st.subheader(f"📘 {model_name}")
                st.write(f"Accuracy: {res['accuracy']:.4f}")
                st.write("Confusion Matrix:")
                st.write(res["conf_matrix"])
                st.write("Classification Report:")
                st.json(res["report"])



# --- Page Routing ---
if not st.session_state.auth:
    if st.session_state.page == "main":
        main_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "about":
        about_page()
else:
    detect_fraud()
