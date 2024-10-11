import streamlit as st
from PIL import Image
import os
import pickle

# Load your model
model = pickle.load(open('model1.pkl', 'rb'))

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #e8f5e9;  /* Soft green background */
        font-family: Arial, sans-serif;
    }
    .title {
        color: #d32f2f;  /* Dark Red */
        font-size: 36px;
        font-weight: bold;
        text-align: center;
    }
    .subtitle {
        color: #ff9800;  /* Orange */
        font-size: 24px;
        text-align: center;
        margin-bottom: 40px;
    }
    .stButton > button {
        background-color: #ff9800;  /* Orange */
        color: white;
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #fb8c00;
        cursor: pointer;
    }
    .floating-news {
        position: fixed;
        bottom: 10px;
        right: 10px;
        background-color: #e8f5e9;  /* Matching soft green background */
        border: 1px solid #d0d0d0;
        padding: 20px;  /* Increased padding */
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        max-width: 400px;  /* Increased width */
        height: 500px;  /* Increased height for the news section */
        overflow: hidden;  /* Hide overflow */
    }
    .news-container {
        height: 470px;  /* Height to accommodate more items */
        overflow: hidden;  /* Hide overflow for smooth scrolling */
        animation: scrollUp 30s linear infinite;  /* Continuous upward scrolling */
    }
    @keyframes scrollUp {
        0% { transform: translateY(0); }
        100% { transform: translateY(-100%); }
    }
    .news-item {
        margin: 5px 0;
        padding: 15px;  /* Increased padding */
        border: 1px solid #ccc;
        border-radius: 5px;
        transition: background-color 0.2s;
        cursor: pointer;  /* Change cursor to pointer */
    }
    .news-item:hover {
        background-color: #f1f1f1;  /* Highlight on hover */
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript to pause scrolling
st.markdown("""
    <script>
    let newsContainer = null;
    function pauseScroll() {
        console.log("Paused scrolling");
        if (newsContainer) {
            newsContainer.style.animationPlayState = 'paused';
        }
    }
    function resumeScroll() {
        console.log("Resumed scrolling");
        if (newsContainer) {
            newsContainer.style.animationPlayState = 'running';
        }
    }
    window.onload = function() {
        newsContainer = document.querySelector('.news-container');
        newsContainer.addEventListener('mouseenter', pauseScroll);
        newsContainer.addEventListener('mouseleave', resumeScroll);
        console.log("News container loaded");
    }
    
    function showDetail(detail) {
        window.alert(detail);  // Show news detail in an alert
    }
    </script>
""", unsafe_allow_html=True)

def run():
    # Header
    st.markdown('<p class="title">Bank Loan Prediction</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">State Bank of India</p>', unsafe_allow_html=True)

    # Display Bank Logo
    img_path = os.path.join(os.getcwd(), 'images', 'bank.jpg')
    if os.path.exists(img_path):
        img1 = Image.open(img_path)
        img1 = img1.resize((180, 180))
        st.image(img1, use_column_width=False)
    else:
        st.error(f"Image file not found at: {img_path}")

    # User input fields
    st.subheader("Fill in the details below:")

    fn = st.text_input('Full Name')
    account_no = st.text_input('Account Number')

    # Split columns for Gender and Education
    col1, col2 = st.columns(2)
    with col1:
        gen_display = ('Female', 'Male')
        gen = st.selectbox("Gender", list(range(len(gen_display))), format_func=lambda x: gen_display[x])
    with col2:
        edu_display = ('Not Graduate', 'Graduate')
        edu = st.selectbox("Education", list(range(len(edu_display))), format_func=lambda x: edu_display[x])

    # Marital Status and Dependents
    col3, col4 = st.columns(2)
    with col3:
        mar_display = ('No', 'Yes')
        mar = st.selectbox("Marital Status", list(range(len(mar_display))), format_func=lambda x: mar_display[x])
    with col4:
        dep_display = ('No', 'One', 'Two', 'More than Two')
        dep = st.selectbox("Dependents", list(range(len(dep_display))), format_func=lambda x: dep_display[x])

    # Employment Status and Property Area
    col5, col6 = st.columns(2)
    with col5:
        emp_display = ('Job', 'Business')
        emp = st.selectbox("Employment Status", list(range(len(emp_display))), format_func=lambda x: emp_display[x])
    with col6:
        prop_display = ('Rural', 'Semi-Urban', 'Urban')
        prop = st.selectbox("Property Area", list(range(len(prop_display))), format_func=lambda x: prop_display[x])

    # Credit Score, Income, Loan Amount, and Duration
    cred_display = ('Between 300 to 500', 'Above 500')
    cred = st.selectbox("Credit Score", list(range(len(cred_display))), format_func=lambda x: cred_display[x])

    col7, col8 = st.columns(2)
    with col7:
        mon_income = st.number_input("Applicant's Monthly Income ($)", value=0)
        co_mon_income = st.number_input("Co-Applicant's Monthly Income ($)", value=0)
    with col8:
        loan_amt = st.number_input("Loan Amount", value=0)

    dur_display = ['2 Month', '6 Month', '8 Month', '1 Year', '16 Month']
    dur = st.selectbox("Loan Duration", list(range(len(dur_display))), format_func=lambda x: dur_display[x])

    # Submit button with hover effect
    if st.button("Submit"):
        duration = [60, 180, 240, 360, 480][dur]
        features = [[gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt, duration, cred, prop]]
        prediction = model.predict(features)
        ans = int(prediction[0])

        # Display the result
        if ans == 0:
            st.error(f"Hello {fn}, you will not get a loan as per the bank's calculations.")
        else:
            st.success(f"Hello {fn}, Congratulations! You will get the loan from the bank.")

    # Floating news section with offers and news
    st.markdown("""
        <div class="floating-news">
            <p><strong>Latest News & Offers:</strong></p>
            <div class="news-container">
                <div class="news-item" onclick="showDetail('🌟 Special Loan Offers for New Customers!')">🌟 Special Loan Offers for New Customers!</div>
                <div class="news-item" onclick="showDetail('📈 Interest rates reduced for Home Loans!')">📈 Interest rates reduced for Home Loans!</div>
                <div class="news-item" onclick="showDetail('📰 Read our latest financial advice articles!')">📰 Read our latest financial advice articles!</div>
                <div class="news-item" onclick="showDetail('✅ Apply now for a free financial consultation!')">✅ Apply now for a free financial consultation!</div>
                <div class="news-item" onclick="showDetail('📊 Tips for managing your finances better!')">📊 Tips for managing your finances better!</div>
                <div class="news-item" onclick="showDetail('🏦 Join our rewards program for better benefits!')">🏦 Join our rewards program for better benefits!</div>
                <div class="news-item" onclick="showDetail('💡 Explore new investment options with us!')">💡 Explore new investment options with us!</div>
                <div class="news-item" onclick="showDetail('📅 Upcoming financial literacy workshops!')">📅 Upcoming financial literacy workshops!</div>
                <div class="news-item" onclick="showDetail('🌍 Join our sustainable finance initiatives!')">🌍 Join our sustainable finance initiatives!</div>
                <div class="news-item" onclick="showDetail('📞 Get personalized advice from our experts!')">📞 Get personalized advice from our experts!</div>
                <div class="news-item" onclick="showDetail('🎉 Enjoy exclusive discounts on services!')">🎉 Enjoy exclusive discounts on services!</div>
                <div class="news-item" onclick="showDetail('📊 Free webinar on investment strategies!')">📊 Free webinar on investment strategies!</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == '__main__':
    run()
