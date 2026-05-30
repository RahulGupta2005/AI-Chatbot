# =========================
# FILE: Admin/admin.py
# =========================

import streamlit as st
import pandas as pd
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Admin Portal",
    page_icon="🎓",
    layout="wide"
)

# =========================
# FAQ FILE PATH
# =========================

FAQ_FILE = "DATA/faq.csv"

# =========================
# CREATE FILE IF NOT EXISTS
# =========================

if not os.path.exists(FAQ_FILE):

    df = pd.DataFrame(columns=["question", "answer"])

    df.to_csv(FAQ_FILE, index=False)

# =========================
# SESSION STATE
# =========================

if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# =========================
# LOAD DATA FUNCTION
# =========================

def load_data():

    return pd.read_csv(FAQ_FILE)

# =========================
# SAVE DATA FUNCTION
# =========================

def save_data(df):

    df.to_csv(FAQ_FILE, index=False)

# =========================
# ADMIN LOGIN FUNCTION
# =========================

def admin_login():

    st.image("logo.png", width=120)

    st.title("🎓 College Chatbot Admin Portal")

    st.subheader("🔐 Admin Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "admin" and password == "1234":

            st.session_state["admin_logged_in"] = True

            st.success("✅ Login Successful")

            st.rerun()

        else:

            st.error("❌ Invalid Username or Password")

# =========================
# LOGIN PAGE
# =========================

if st.session_state["admin_logged_in"] == False:

    admin_login()

# =========================
# ADMIN DASHBOARD
# =========================

else:

    # =========================
    # SIDEBAR
    # =========================

    st.sidebar.image("logo.png", width=100)

    st.sidebar.title("🎓 Admin Dashboard")

    menu = st.sidebar.selectbox(

        "Select Option",

        [
            "🏠 Home",
            "📄 View FAQ",
            "➕ Add FAQ",
            "✏ Edit FAQ",
            "🗑 Delete FAQ",
            "📤 Upload CSV",
            "📊 Statistics",
            "🚪 Logout"
        ]
    )

    # =========================
    # LOAD FAQ DATA
    # =========================

    df = load_data()

    # =========================
    # HOME PAGE
    # =========================

    if menu == "🏠 Home":

        st.title("🎓 College Chatbot Admin Panel")

        st.write("---")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total FAQs",
                len(df)
            )

        with col2:

            st.metric(
                "Total Questions",
                len(df["question"])
            )

        with col3:

            st.metric(
                "Total Answers",
                len(df["answer"])
            )

        st.write("---")

        st.subheader("📌 Admin Features")

        st.write("""
        ✅ View FAQs  
        ✅ Add New FAQs  
        ✅ Edit Existing FAQs  
        ✅ Delete FAQs  
        ✅ Upload CSV Files  
        ✅ Monitor Data  
        """)

    # =========================
    # VIEW FAQ
    # =========================

    elif menu == "📄 View FAQ":

        st.title("📄 FAQ Data")

        st.dataframe(
            df,
            use_container_width=True
        )

    # =========================
    # ADD FAQ
    # =========================

    elif menu == "➕ Add FAQ":

        st.title("➕ Add New FAQ")

        question = st.text_input(
            "Enter Question"
        )

        answer = st.text_area(
            "Enter Answer"
        )

        if st.button("Add FAQ"):

            if question == "" or answer == "":

                st.warning(
                    "⚠ Please fill all fields"
                )

            else:

                new_data = pd.DataFrame({

                    "question": [question],
                    "answer": [answer]

                })

                df = pd.concat(
                    [df, new_data],
                    ignore_index=True
                )

                save_data(df)

                st.success(
                    "✅ FAQ Added Successfully"
                )

    # =========================
    # EDIT FAQ
    # =========================

    elif menu == "✏ Edit FAQ":

        st.title("✏ Edit FAQ")

        selected_question = st.selectbox(

            "Select Question",

            df["question"]

        )

        selected_row = df[
            df["question"] == selected_question
        ]

        current_answer = selected_row.iloc[0]["answer"]

        new_answer = st.text_area(

            "Edit Answer",

            current_answer

        )

        if st.button("Update FAQ"):

            df.loc[
                df["question"] == selected_question,
                "answer"
            ] = new_answer

            save_data(df)

            st.success(
                "✅ FAQ Updated Successfully"
            )

    # =========================
    # DELETE FAQ
    # =========================

    elif menu == "🗑 Delete FAQ":

        st.title("🗑 Delete FAQ")

        selected_question = st.selectbox(

            "Select Question to Delete",

            df["question"]

        )

        if st.button("Delete FAQ"):

            df = df[
                df["question"] != selected_question
            ]

            save_data(df)

            st.success(
                "✅ FAQ Deleted Successfully"
            )

    # =========================
    # UPLOAD CSV
    # =========================

    elif menu == "📤 Upload CSV":

        st.title("📤 Upload New CSV File")

        uploaded_file = st.file_uploader(

            "Upload CSV File",

            type=["csv"]

        )

        if uploaded_file is not None:

            new_df = pd.read_csv(uploaded_file)

            st.write("### Preview")

            st.dataframe(new_df)

            if st.button("Replace Existing Data"):

                new_df.to_csv(
                    FAQ_FILE,
                    index=False
                )

                st.success(
                    "✅ CSV Uploaded Successfully"
                )

    # =========================
    # STATISTICS
    # =========================

    elif menu == "📊 Statistics":

        st.title("📊 Chatbot Statistics")

        st.write("### Total FAQ Records")

        st.info(f"Total FAQs : {len(df)}")

        st.write("---")

        st.write("### Sample Questions")

        st.write(df["question"].head())

    # =========================
    # LOGOUT
    # =========================

    elif menu == "🚪 Logout":

        st.session_state["admin_logged_in"] = False

        st.success("✅ Logged Out Successfully")

        st.rerun()