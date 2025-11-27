import streamlit as st
import pandas as pd
import numpy as np


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, time

# Page configuration
st.set_page_config(
    page_title="Streamlit Techniques Demo",
    page_icon="🚀",
    layout="wide"
)

# Initialize session state
if 'counter' not in st.session_state:
    st.session_state.counter = 0
if 'submitted_data' not in st.session_state:
    st.session_state.submitted_data = []

# Title and headers
st.title("🚀 Streamlit Techniques Demo")
st.markdown("*A comprehensive showcase of Streamlit capabilities*")
st.divider()

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Select Demo Section:", [
        "Text & Display",
        "Input Widgets",
        "Data Display",
        "Charts",
        "Layouts",
        "Status & Progress",
        "Session State"
    ])
    st.divider()
    st.info("👈 Select a section to explore different techniques")

# ===== TEXT & DISPLAY =====
if page == "Text & Display":
    st.header("📝 Text & Display Techniques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Text")
        st.write("st.write() - most versatile")
        st.text("st.text() - fixed width")
        st.markdown("**st.markdown()** - *supports* `markdown`")
        st.caption("st.caption() - small text")
        
        st.subheader("Code Display")
        code = '''def hello():
    print("Hello, Streamlit!")'''
        st.code(code, language='python')
        
    with col2:
        st.subheader("LaTeX")
        st.latex(r'\sum_{i=1}^{n} x_i^2')
        
        st.subheader("JSON")
        st.json({"name": "Streamlit", "version": "1.0", "features": ["fast", "easy"]})
        
        st.subheader("Containers")
        with st.expander("Click to expand"):
            st.write("Hidden content inside expander!")

# ===== INPUT WIDGETS =====
elif page == "Input Widgets":
    st.header("🎛️ Input Widgets")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Buttons & Selection")
        if st.button("Click me!"):
            st.success("Button clicked!")
        
        checkbox = st.checkbox("I agree to terms")
        toggle = st.toggle("Enable feature")
        
        radio = st.radio("Choose one:", ["Option A", "Option B", "Option C"])
        
        select = st.selectbox("Select item:", ["Item 1", "Item 2", "Item 3"])
        
        multi = st.multiselect("Select multiple:", ["Red", "Green", "Blue", "Yellow"])
        
    with col2:
        st.subheader("Text & Number Input")
        text = st.text_input("Enter your name:")
        
        textarea = st.text_area("Enter description:", height=100)
        
        number = st.number_input("Enter number:", min_value=0, max_value=100, value=50)
        
        slider = st.slider("Select range:", 0, 100, (25, 75))
        
        date = st.date_input("Select date:")
        
        time_val = st.time_input("Select time:")
        
        color = st.color_picker("Pick a color:", "#00f900")
    
    st.divider()
    st.subheader("File Upload")
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'txt', 'png'])
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

# ===== DATA DISPLAY =====
elif page == "Data Display":
    st.header("📊 Data Display Techniques")
    
    # Sample data
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'Salary': [50000, 60000, 70000, 80000],
        'Department': ['IT', 'HR', 'IT', 'Finance']
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("st.dataframe()")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("st.table()")
        st.table(df.head(2))
        
    with col2:
        st.subheader("st.metric()")
        met1, met2, met3 = st.columns(3)
        met1.metric("Revenue", "$50K", "+10%")
        met2.metric("Users", "1.2K", "-5%")
        met3.metric("Rating", "4.8", "+0.2")
        
        st.subheader("st.data_editor()")
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# ===== CHARTS =====
elif page == "Charts":
    st.header("📈 Chart Techniques")
    
    # Sample data
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Line Chart")
        st.line_chart(chart_data)
        
        st.subheader("Bar Chart")
        st.bar_chart(chart_data)
        
    with col2:
        st.subheader("Area Chart")
        st.area_chart(chart_data)
        
        st.subheader("Scatter Chart")
        scatter_data = pd.DataFrame({
            'x': np.random.randn(50),
            'y': np.random.randn(50),
            'size': np.random.randint(10, 100, 50)
        })
        st.scatter_chart(scatter_data, x='x', y='y', size='size')
    
    st.divider()
    st.subheader("Plotly Chart")
    fig = px.scatter(scatter_data, x='x', y='y', size='size', 
                     title="Interactive Plotly Chart")
    st.plotly_chart(fig, use_container_width=True)

# ===== LAYOUTS =====
elif page == "Layouts":
    st.header("🎨 Layout Techniques")
    
    st.subheader("Columns")
    col1, col2, col3 = st.columns(3)
    col1.metric("Column 1", "100", "+10")
    col2.metric("Column 2", "200", "-5")
    col3.metric("Column 3", "300", "+15")
    
    st.divider()
    
    st.subheader("Tabs")
    tab1, tab2, tab3 = st.tabs(["🐱 Cat", "🐶 Dog", "🦉 Owl"])
    with tab1:
        st.write("Content about cats")
    with tab2:
        st.write("Content about dogs")
    with tab3:
        st.write("Content about owls")
    
    st.divider()
    
    st.subheader("Expander")
    with st.expander("See explanation"):
        st.write("This is hidden content that can be expanded!")
        st.image("https://via.placeholder.com/300x200", caption="Placeholder image")
    
    st.divider()
    
    st.subheader("Container")
    container = st.container(border=True)
    container.write("This is inside a bordered container")
    container.button("Container button")
    
    st.divider()
    
    st.subheader("Form")
    with st.form("my_form"):
        st.write("Form example")
        name = st.text_input("Name")
        age = st.slider("Age", 0, 100, 25)
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success(f"Form submitted! Name: {name}, Age: {age}")

# ===== STATUS & PROGRESS =====
elif page == "Status & Progress":
    st.header("⚡ Status & Progress")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Status Messages")
        st.success("✅ Success message")
        st.info("ℹ️ Info message")
        st.warning("⚠️ Warning message")
        st.error("❌ Error message")
        
        st.subheader("Toast")
        if st.button("Show toast"):
            st.toast("This is a toast notification!", icon="🎉")
        
    with col2:
        st.subheader("Progress Bar")
        progress = st.progress(0)
        if st.button("Run progress"):
            import time
            for i in range(100):
                progress.progress(i + 1)
                time.sleep(0.01)
            st.success("Complete!")
        
        st.subheader("Celebrations")
        if st.button("🎈 Balloons"):
            st.balloons()
        if st.button("❄️ Snow"):
            st.snow()
    
    st.divider()
    
    st.subheader("Spinner")
    if st.button("Run with spinner"):
        with st.spinner("Processing..."):
            import time
            time.sleep(2)
        st.success("Done!")

# ===== SESSION STATE =====
elif page == "Session State":
    st.header("💾 Session State")
    
    st.write("Session state persists data across reruns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Counter Example")
        st.write(f"Current count: {st.session_state.counter}")
        
        if st.button("Increment"):
            st.session_state.counter += 1
            st.rerun()
        
        if st.button("Reset"):
            st.session_state.counter = 0
            st.rerun()
    
    with col2:
        st.subheader("Data Collection")
        with st.form("data_form"):
            item = st.text_input("Add item:")
            if st.form_submit_button("Add"):
                if item:
                    st.session_state.submitted_data.append(item)
        
        if st.session_state.submitted_data:
            st.write("Collected items:")
            for i, data in enumerate(st.session_state.submitted_data):
                st.write(f"{i+1}. {data}")
            
            if st.button("Clear all"):
                st.session_state.submitted_data = []
                st.rerun()

# Footer
st.divider()
st.caption("Built with Streamlit 🎈 | Explore different sections from the sidebar")


