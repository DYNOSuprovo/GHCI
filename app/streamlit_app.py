import streamlit as st
import pandas as pd
import os
import sys

# Add root directory to path so we can import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model import TransactionClassifier
from src.explainability import Explainer
from src.data_generator import generate_synthetic_data, load_config

st.set_page_config(page_title="Transaction Categorizer", layout="wide")

# --- Model Management ---
@st.cache_resource
def get_model():
    classifier = TransactionClassifier()
    model_path = "models/model.pkl"
    
    # Train if model doesn't exist
    if not os.path.exists(model_path):
        with st.spinner("Training model for the first time... (this takes ~30 seconds)"):
            # Ensure directories exist
            os.makedirs("data", exist_ok=True)
            os.makedirs("models", exist_ok=True)
            
            # Generate data
            generate_synthetic_data(num_samples=50000, output_path="data/transactions.csv")
            
            # Train model
            classifier.train(data_path="data/transactions.csv")
            classifier.save_model(model_path)
            st.success("Model trained successfully!")
    
    classifier.load_model(model_path)
    return classifier

@st.cache_resource
def get_explainer():
    model_path = "models/model.pkl"
    if os.path.exists(model_path):
        return Explainer(model_path)
    return None

def get_config():
    return load_config()

# Initialize
try:
    classifier = get_model()
    explainer = get_explainer()
    config = get_config()
except Exception as e:
    st.error(f"Error initializing app: {e}")
    st.stop()

# --- UI ---
st.title("💰 Transaction Categorization System (Standalone)")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Classify Transaction")
    description = st.text_input("Transaction Description", "STARBUCKS COFFEE NY")
    amount = st.number_input("Amount", min_value=0.0, value=10.0)
    
    if st.button("Categorize"):
        # Direct inference (No API call)
        result = classifier.predict(description)[0]
        
        st.success(f"Category: **{result['category']}**")
        st.info(f"Confidence: {result['confidence']:.2f}")
        
        # Feedback Loop
        st.markdown("---")
        st.write("Is this correct?")
        cat_names = [c["name"] for c in config["categories"]]
        correct_cat = st.selectbox("Correct Category", cat_names, index=cat_names.index(result['category']) if result['category'] in cat_names else 0)
        
        if st.button("Submit Feedback"):
            feedback_file = "data/feedback.csv"
            file_exists = os.path.exists(feedback_file)
            with open(feedback_file, "a") as f:
                if not file_exists:
                    f.write("description,correct_category\n")
                f.write(f"{description},{correct_cat}\n")
            st.success("Feedback recorded locally!")

        # Explanation
        st.subheader("Explanation")
        if explainer:
            explanation = explainer.explain(description)[:5]
            if explanation:
                exp_df = pd.DataFrame(explanation)
                st.bar_chart(exp_df.set_index("word"))
            else:
                st.info("No specific words contributed.")

with col2:
    st.header("Taxonomy")
    for cat in config["categories"]:
        with st.expander(cat["name"]):
            st.write(f"ID: {cat['id']}")
            st.write(f"Keywords: {', '.join(cat['keywords'])}")

st.markdown("---")
st.subheader("Batch Processing")

tab1, tab2 = st.tabs(["Upload CSV", "Manual Entry"])

with tab1:
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "description" in df.columns:
            if st.button("Process CSV"):
                descriptions = df["description"].tolist()
                results = classifier.predict(descriptions)
                result_df = pd.DataFrame(results)
                # Add original description back
                result_df.insert(0, "description", descriptions)
                st.dataframe(result_df)
