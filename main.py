import streamlit as st
from db_c import conn,cursor

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# TITLE
st.title("🎥 Media Platform")

# ---------------- LOGIN INPUTS ----------------

def login_inputs():

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    return email,password

# ---------------- SIGNUP INPUTS ----------------

def signup_inputs():

    name = st.text_input(
        "Name"
    )

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    return name,email,password




# ---------------- DASHBOARD ----------------

def dashboard():

    user = st.session_state.user

    st.sidebar.success(
        f"Welcome {user['name']}"
    )

    menu = st.sidebar.selectbox(
        "Select Menu",
        [
            "Dashboard",
            "Upload Files",
            "View Uploaded Files",
            "Logout"
        ]
    )

    # ---------------- HOME ----------------

    if menu == "Dashboard":

        st.subheader(
            "Dashboard"
        )

        st.info(
            "Welcome To Media Platform"
        )

    # ---------------- UPLOAD FILES ----------------

import cloudinary
import cloudinary.uploader

# CLOUDINARY CONFIG

cloudinary.config(
    cloud_name=st.secrets["CLOUD_NAME"],
    api_key=st.secrets["API_KEY"],
    api_secret=st.secrets["API_SECRET"]
)

# ---------------- UPLOAD FILES ----------------

elif menu == "Upload Files":

    st.subheader(
        "Upload Files"
    )

    uploaded_file = st.file_uploader(
        "Upload Files",
        type=[
            "pdf",
            "mp3",
            "mp4",
            "jpg",
            "jpeg",
            "png"
        ]
    )

    if uploaded_file:

        st.success(
            "File Selected Successfully"
        )

        st.write(
            "File Name:",
            uploaded_file.name
        )

        st.write(
            "File Type:",
            uploaded_file.type
        )

        st.write(
            "File Size:",
            uploaded_file.size,
            "bytes"
        )

        # ---------------- PREVIEW ----------------

        # PDF
        if uploaded_file.type == "application/pdf":

            st.info("PDF File")


        # AUDIO
        elif "audio" in uploaded_file.type:

            st.audio(uploaded_file)

        # VIDEO
        elif "video" in uploaded_file.type:

            st.video(uploaded_file)

        # IMAGE
        elif "image" in uploaded_file.type:

            st.image(
                uploaded_file,
                width=300
            )

        # ---------------- CLOUDINARY UPLOAD ----------------

        if st.button("Upload To Cloudinary"):

            result = cloudinary.uploader.upload(
                uploaded_file,
                resource_type="auto"
            )

            file_url = result["secure_url"]

            st.success(
                "File Uploaded Successfully"
            )

            st.write(
                "Cloudinary URL:",file_url
            )

            st.code(file_url)

    # ---------------- VIEW FILES ----------------

    elif menu == "View Uploaded Files":

        st.subheader(
            "View Uploaded Files"
        )

        st.info(
            "All Uploaded Files Here"
        )

    # ---------------- LOGOUT ----------------

    elif menu == "Logout":

        st.session_state.user = None

        st.success(
            "Logout Successful"
        )

        st.rerun()
# ---------------- MAIN ----------------

if st.session_state.user is None:

    tab1,tab2 = st.tabs(
        [
            "Login",
            "Signup"
        ]
    )

    # ---------------- LOGIN ----------------

    with tab1:

        st.subheader("Login")

        with st.form("login_form"):

            email,password = login_inputs()

            submit = st.form_submit_button(
                "Login"
            )

            if submit:

                query = """
                SELECT * FROM users
                WHERE email=%s
                AND password=%s
                """

                values = (
                    email,
                    password
                )

                cursor.execute(
                    query,
                    values
                )

                user = cursor.fetchone()

                if user:

                    st.session_state.user = user

                    st.success(
                        "Login Success"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid Credentials"
                    )

    # ---------------- SIGNUP ----------------

    with tab2:

        st.subheader("Signup")

        with st.form("signup_form"):

            name,email,password = signup_inputs()

            submit = st.form_submit_button(
                "Signup"
            )

            if submit:

                query = """
                INSERT INTO users(
                    name,
                    email,
                    password
                )
                VALUES(%s,%s,%s)
                """

                values = (
                    name,
                    email,
                    password
                )

                try:

                    cursor.execute(
                        query,
                        values
                    )

                    conn.commit()

                    st.success(
                        "Signup Success"
                    )

                    st.rerun()

                except:

                    st.error(
                        "Email Already Exists"
                    )

else:
    dashboard()



    # dxfzhisem cloudname
    # 543988112976599 key 
    # jjiOBtDPJgT2one9QbAiDDSE6ik secret