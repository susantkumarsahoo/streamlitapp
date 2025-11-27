import streamlit as st

st.title("Navigation Panel")

# -------------------------------
# TOP LEVEL MENU (TABS)
# -------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([  
    "Configurations",
    "Registration",
    "Pending Request",
    "Power Outage",
    "View Status",
    "Others",
    "Reports",
    "Quick Links"
])


# -------------------------------
# CONFIGURATIONS
# -------------------------------
with tab1:
    st.subheader("Configurations")
    choice = st.radio(
        "Select Option",
        ["Business Type", "Access Manager", "Operation"],
        horizontal=True
    )
    st.info(f"You selected: {choice}")


# -------------------------------
# REGISTRATION
# -------------------------------
with tab2:
    st.subheader("Registration")
    reg_choice = st.radio(
        "Select Option",
        ["Yes", "No"],
        horizontal=True
    )
    st.info(f"You selected: {reg_choice}")


# -------------------------------
# PENDING REQUEST
# -------------------------------
with tab3:
    st.subheader("Pending Request")
    st.warning("Showing all pending requests...")


# -------------------------------
# POWER OUTAGE
# -------------------------------
with tab4:
    st.subheader("Power Outage")
    p_choice = st.radio(
        "Select Option",
        ["Individual", "Total Area"],
        horizontal=True
    )
    st.info(f"You selected: {p_choice}")


# -------------------------------
# VIEW STATUS
# -------------------------------
with tab5:
    st.subheader("View Status")
    status_choice = st.radio(
        "Select Option",
        ["Resolved", "Unresolved"],
        horizontal=True
    )
    st.info(f"You selected: {status_choice}")


# -------------------------------
# OTHERS
# -------------------------------
with tab6:
    st.subheader("Others")
    st.write("No submenu available.")


# -------------------------------
# REPORTS
# -------------------------------
with tab7:
    st.subheader("Reports")
    st.write("No submenu available.")


# -------------------------------
# QUICK LINKS
# -------------------------------
with tab8:
    st.subheader("Quick Links")
    st.write("Useful shortcuts and resources.")
