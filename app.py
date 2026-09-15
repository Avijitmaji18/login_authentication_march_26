import streamlit as st
import mysql.connector
from mysql.connector import Error

# Page configuration
st.set_page_config(
    page_title="Customer Login",
    page_icon="🔐",
    layout="centered"
)

# MySQL connection function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Avijit@1234",
        database="login_auth_march_26"
    )


# Function: Customer registration
def data_entry_sql(full_name, address, ph_no, userid, pwd):
    conn_obj = None
    cur_obj = None

    try:
        conn_obj = get_connection()
        cur_obj = conn_obj.cursor()

        sql = """
            INSERT INTO cust_details11
            (full_name, address, ph_no, user_id, password)
            VALUES (%s, %s, %s, %s, %s)
        """

        data = (full_name, address, ph_no, userid, pwd)

        cur_obj.execute(sql, data)
        conn_obj.commit()

        return True, "CUSTOMER REGISTRATION SUCCESSFUL."

    except Error as e:
        if conn_obj:
            conn_obj.rollback()

        return False, f"Error inserting data to MySQL: {e}"

    finally:
        if cur_obj:
            cur_obj.close()
        if conn_obj:
            conn_obj.close()


# Function: Retrieve customer details
def data_retrieve(userid_l):
    conn_obj = None
    cur_obj = None

    try:
        conn_obj = get_connection()
        cur_obj = conn_obj.cursor()

        # Parameterized query
        query = """
            SELECT * FROM cust_details11
            WHERE user_id = %s
        """

        cur_obj.execute(query, (userid_l,))
        result = cur_obj.fetchone()

        return result

    except Error as e:
        st.error(f"Error retrieving data from MySQL: {e}")
        return None

    finally:
        if cur_obj:
            cur_obj.close()
        if conn_obj:
            conn_obj.close()


# Main Streamlit application
st.title("🔐 Customer Login & Registration")
st.write("Please select an option below.")

login_tab, registration_tab = st.tabs(
    ["🔑 Login", "📝 New User Registration"]
)


# Login window
with login_tab:
    st.subheader("Login Window")

    with st.form("login_form"):
        userid_l = st.text_input(
            "Please enter your User ID"
        )

        pwd_l = st.text_input(
            "Please enter your Password",
            type="password"
        )

        login_button = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if login_button:
        if not userid_l or not pwd_l:
            st.warning("Please enter User ID and Password.")

        else:
            cust_details11_db = data_retrieve(
                userid_l.strip()
            )

            if cust_details11_db:
                # Password is the second-last column
                pwd_db = cust_details11_db[-2]

                if pwd_l == pwd_db:
                    st.success("Access granted!")

                    st.subheader("Customer Details")

                    # Display all customer details
                    for i, cust_details11 in enumerate(
                        cust_details11_db, start=1
                    ):
                        st.write(
                            f"**Column {i}:** {cust_details11}"
                        )

                else:
                    st.error(
                        "Access denied, invalid User ID or Password."
                    )

            else:
                st.warning(
                    "User ID not found. Please check or register yourself."
                )


# New User Registration window
with registration_tab:
    st.subheader("Please fill the form to register yourself.")

    with st.form("registration_form"):
        full_name = st.text_input(
            "Please enter your full name"
        )

        address = st.text_area(
            "Please enter your address"
        )

        ph_no = st.text_input(
            "Please enter your phone number"
        )

        userid = st.text_input(
            "Please set your User ID"
        )

        pwd = st.text_input(
            "Please set your Password",
            type="password"
        )

        register_button = st.form_submit_button(
            "Register",
            use_container_width=True
        )

    if register_button:
        full_name = full_name.strip().upper()
        address = address.strip().upper()
        ph_no = ph_no.strip()
        userid = userid.strip()
        pwd = pwd.strip()

        if not all([full_name, address, ph_no, userid, pwd]):
            st.warning("Please fill in all fields.")

        else:
            success, message = data_entry_sql(
                full_name,
                address,
                ph_no,
                userid,
                pwd
            )

            if success:
                st.success(message)
            else:
                st.error(message)