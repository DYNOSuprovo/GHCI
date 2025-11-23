import streamlit as st
import requests
import pandas as pd
import yaml

st.set_page_config(page_title="Transaction Categorizer", layout="wide")

API_URL = "http://localhost:8000"

def get_categories():
    try:
        response = requests.get(f"{API_URL}/categories")
        if response.status_code == 200:
            return response.json()
    except:
        return []
    return []

st.title("💰 Transaction Categorization System")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Classify Transaction")
    description = st.text_input("Transaction Description", "STARBUCKS COFFEE NY")
    amount = st.number_input("Amount", min_value=0.0, value=10.0)
    
    if st.button("Categorize"):
        try:
            response = requests.post(f"{API_URL}/predict", json={"description": description, "amount": amount})
            if response.status_code == 200:
                data = response.json()
                st.success(f"Category: **{data['category']}**")
                st.info(f"Confidence: {data['confidence']:.2f}")
                
                # Feedback Loop
                st.markdown("---")
                st.write("Is this correct?")
                
                # Get category names for dropdown
                cat_names = [c["name"] for c in get_categories()]
                correct_cat = st.selectbox("Correct Category", cat_names, index=cat_names.index(data['category']) if data['category'] in cat_names else 0)
                
                if st.button("Submit Feedback"):
                    try:
                        fb_response = requests.post(f"{API_URL}/feedback", json={"description": description, "correct_category": correct_cat})
                        if fb_response.status_code == 200:
                            st.success("Thank you! Feedback recorded.")
                        else:
                            st.error("Failed to save feedback.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                
                st.subheader("Explanation")
                if data['explanation']:
                    exp_df = pd.DataFrame(data['explanation'])
                    st.bar_chart(exp_df.set_index("word"))
                else:
                    st.info("No specific words contributed to this prediction (likely unknown words).")
            else:
                st.error("Error classifying transaction")
        except Exception as e:
            st.error(f"Could not connect to API: {e}")

with col2:
    st.header("Taxonomy")
    categories = get_categories()
    if categories:
        for cat in categories:
            with st.expander(cat["name"]):
                st.write(f"ID: {cat['id']}")
                st.write(f"Keywords: {', '.join(cat['keywords'])}")
    else:
        st.warning("Could not load categories. Is the backend running?")

st.markdown("---")
st.markdown("---")
st.subheader("Batch Processing")

tab1, tab2 = st.tabs(["Upload CSV", "Manual Entry"])

with tab1:
    uploaded_file = st.file_uploader("Upload CSV (must contain 'description' column)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "description" in df.columns:
            st.write("Preview:", df.head())
            if st.button("Process CSV"):
                transactions = [{"description": desc, "amount": 0.0} for desc in df["description"].tolist()]
                try:
                    response = requests.post(f"{API_URL}/predict_batch", json={"transactions": transactions})
                    if response.status_code == 200:
                        results = response.json()
                        result_df = pd.DataFrame(results)
                        st.success("Batch processing complete!")
                        st.dataframe(result_df)
                        
                        csv = result_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "Download Results",
                            csv,
                            "categorized_transactions.csv",
                            "text/csv",
                            key='download-csv'
                        )
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
        else:
            st.error("CSV must contain a 'description' column")

with tab2:
    st.write("Enter multiple transaction descriptions (one per line):")
    manual_input = st.text_area("Descriptions", height=150, placeholder="UBER TRIP\nNETFLIX.COM\nSTARBUCKS")
    if st.button("Process Manual Entry"):
        if manual_input:
            lines = [line.strip() for line in manual_input.split('\n') if line.strip()]
            transactions = [{"description": line, "amount": 0.0} for line in lines]
            
            try:
                response = requests.post(f"{API_URL}/predict_batch", json={"transactions": transactions})
                if response.status_code == 200:
                    results = response.json()
                    result_df = pd.DataFrame(results)
                    st.success("Processing complete!")
                    st.dataframe(result_df)
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please enter some text.")
