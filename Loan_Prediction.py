import streamlit as st
from PIL import Image
import os
import pickle

# Load your model, ensure 'model1.pkl' is in the correct location
model = pickle.load(open('model1.pkl', 'rb'))

def run():
    # Correct path to the image
    img_path = os.path.join(os.getcwd(), 'images', 'bank.jpg')
    
    # Check if the image exists before loading
    if os.path.exists(img_path):
        img1 = Image.open(img_path)
        img1 = img1.resize((180, 180))
        st.image(img1, use_column_width=False)
    else:
        st.error(f"Image file not found at: {img_path}")
    
    # Bank and prediction title
    new_title = '<p style="font-family:sans-serif; color:Orange; font-size: 20px;">State Bank Of India</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    
    title = '<p style="font-family:sans-serif; color:orange; font-size: 30px;">Bank Loan Prediction</p>'
    st.markdown(title, unsafe_allow_html=True)

    # User input fields
    fn = st.text_input('Full Name')
    account_no = st.text_input('Account Number')

    gen_display = ('Female', 'Male')
    gen = st.selectbox("Gender", list(range(len(gen_display))), format_func=lambda x: gen_display[x])

    edu_display = ('Not Graduate', 'Graduate')
    edu = st.selectbox("Education", list(range(len(edu_display))), format_func=lambda x: edu_display[x])

    mar_display = ('No', 'Yes')
    mar = st.selectbox("Marital Status", list(range(len(mar_display))), format_func=lambda x: mar_display[x])

    dep_display = ('No', 'One', 'Two', 'More than Two')
    dep = st.selectbox("Dependents", list(range(len(dep_display))), format_func=lambda x: dep_display[x])

    emp_display = ('Job', 'Business')
    emp = st.selectbox("Employment Status", list(range(len(emp_display))), format_func=lambda x: emp_display[x])

    prop_display = ('Rural', 'Semi-Urban', 'Urban')
    prop = st.selectbox("Property Area", list(range(len(prop_display))), format_func=lambda x: prop_display[x])

    cred_display = ('Between 300 to 500', 'Above 500')
    cred = st.selectbox("Credit Score", list(range(len(cred_display))), format_func=lambda x: cred_display[x])

    mon_income = st.number_input("Applicant's Monthly Income ($)", value=0)
    co_mon_income = st.number_input("Co-Applicant's Monthly Income ($)", value=0)
    loan_amt = st.number_input("Loan Amount", value=0)

    dur_display = ['2 Month', '6 Month', '8 Month', '1 Year', '16 Month']
    dur = st.selectbox("Loan Duration", list(range(len(dur_display))), format_func=lambda x: dur_display[x])

    if st.button("Submit"):
        # Mapping duration options to actual months
        duration = [60, 180, 240, 360, 480][dur]
        
        # Prepare features for prediction
        features = [[gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt, duration, cred, prop]]
        prediction = model.predict(features)
        ans = int(prediction[0])

        # Display the result
        if ans == 0:
            st.error(f"Hello {fn}, you will not get a loan as per the calculations of the bank.")
        else:
            st.success(f"Hello {fn}, Congratulations!! You will get the loan from the bank.")

# Run the app
run()
