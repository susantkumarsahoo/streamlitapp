import streamlit as st
import datetime


# Page configuration
st.set_page_config(page_title="Power Utility Management System", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #1a1a1a;
    }
    .stButton>button {
        background-color: #5cb85c;
        color: white;
        border-radius: 4px;
        padding: 8px 20px;
    }
    .stButton>button:hover {
        background-color: #4cae4c;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Navigation Bar
st.markdown("""
    <div style='background-color: #0066cc; padding: 10px; margin-bottom: 20px; border-radius: 5px;'>
        <span style='color: white; margin-right: 20px;'>📋 Configurations</span>
        <span style='color: white; margin-right: 20px;'>📝 Registration</span>
        <span style='color: white; margin-right: 20px; background-color: #ff8800; padding: 5px 10px; border-radius: 3px;'>⏳ Pending Request</span>
        <span style='color: white; margin-right: 20px;'>⚡ Power Outage</span>
        <span style='color: white; margin-right: 20px;'>👁️ View Status</span>
        <span style='color: white; margin-right: 20px;'>📊 Others</span>
        <span style='color: white; margin-right: 20px;'>📈 Reports</span>
        <span style='color: white;'>🔗 Quick Links</span>
    </div>
    """, unsafe_allow_html=True)

# Title
st.title("New Request/Complaint Registration")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Registration Form", 
    "Bill Details", 
    "Collection Details", 
    "Complaint Details", 
    "View Documents", 
    "View Latest Bill", 
    "Power Outage Details"
])

with tab1:
    st.subheader("Request/Complaint Modification")
    
    # Request/Complaint Number Search
    col1, col2 = st.columns([4, 1])
    with col1:
        request_no = st.text_input("Request/Complaint No.", key="request_no")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search", key="search_request")
    
    st.markdown("---")
    
    # Search Section
    st.subheader("Search")
    
    col1, col2 = st.columns(2)
    
    with col1:
        consumer_no = st.text_input("Consumer No", key="consumer_no")
        phone_number = st.text_input("Phone Number", key="phone")
        house_number = st.text_input("House Number", key="house")
        meter_number = st.text_input("Meter Number", key="meter")
    
    with col2:
        account_no = st.text_input("Account No", key="account")
        consumer_name = st.text_input("Consumer Name", key="name")
        pole_number = st.text_input("Pole Number", key="pole")
        search_condition = st.selectbox("Search Condition", ["Equals", "Contains", "Starts With", "Ends With"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action Buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
    with col1:
        if st.button("🔍 Show", type="primary", use_container_width=True):
            st.success("Searching records...")
    with col2:
        if st.button("🗺️ View Map", use_container_width=True):
            st.info("Opening map view...")

with tab2:
    st.subheader("Bill Details")
    st.info("Bill details will be displayed here")
    
    # Sample bill details form
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Bill Number")
        st.text_input("Bill Amount")
        st.date_input("Bill Date")
    with col2:
        st.text_input("Due Date")
        st.selectbox("Payment Status", ["Paid", "Pending", "Overdue"])
        st.text_input("Payment Method")

with tab3:
    st.subheader("Collection Details")
    st.info("Collection details will be displayed here")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Collection ID")
        st.number_input("Amount Collected", min_value=0)
    with col2:
        st.date_input("Collection Date")
        st.text_input("Collector Name")

with tab4:
    st.subheader("Complaint Details")
    st.info("Complaint details will be displayed here")
    
    complaint_type = st.selectbox("Complaint Type", [
        "Power Outage",
        "Voltage Fluctuation",
        "Meter Issue",
        "Billing Issue",
        "Other"
    ])
    complaint_desc = st.text_area("Complaint Description", height=150)
    priority = st.select_slider("Priority", options=["Low", "Medium", "High", "Critical"])

with tab5:
    st.subheader("View Documents")
    st.info("Documents will be displayed here")
    
    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "jpg", "png", "doc"])
    if uploaded_file:
        st.success(f"File uploaded: {uploaded_file.name}")

with tab6:
    st.subheader("View Latest Bill")
    st.info("Latest bill will be displayed here")
    
    # Sample bill display
    st.markdown("""
    **Bill Summary**
    - Consumer Number: XXXX-XXXX-XXXX
    - Billing Period: November 2025
    - Amount Due: ₹ 2,500
    - Due Date: 15th December 2025
    """)

with tab7:
    st.subheader("Power Outage Details")
    st.info("Power outage information will be displayed here")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Outage ID")
        st.text_input("Affected Area")
    with col2:
        st.selectbox("Status", ["Reported", "Under Investigation", "Resolved"])
        st.text_input("Estimated Restoration Time")
        st.number_input("Affected Consumers", min_value=0)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #888;'>
        <p>Power Utility Management System © 2025</p>
    </div>
    """, unsafe_allow_html=True)