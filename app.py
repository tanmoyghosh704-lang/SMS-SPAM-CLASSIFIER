import streamlit as st
import pickle
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk

@st.cache_resource
def download_nltk_data():
    nltk.download("punkt")
    nltk.download("punkt_tab")   # 🔥 THIS IS THE MISSING ONE
    nltk.download("stopwords")

download_nltk_data()




# nltk.download("punkt")
# nltk.download("stopwords")

ps = PorterStemmer()
stop_words = set(stopwords.words("english"))

# Load models
tfidf = pickle.load(open("word_vectorization.pkl", "rb"))
model = pickle.load(open("algorithm.pkl", "rb"))

# UI
st.title("Email / SMS Spam Classifier")
input_sms = st.text_input("Enter the message")

# Text preprocessing function
def transform_text(text):
    text=text.lower()
    text=word_tokenize(text)
    y=[]
    for el in text:
        if el.isalnum():
            y.append(el)
    text=y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words("english") and i not in string.punctuation: 
            y.append(i)
    text=y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)
# Predict only if input is not empty
if st.button("Predict"):
    if input_sms.strip() == "":
        st.warning("Please enter a message.")
    else:
        # 1. preprocess
        transformed_sms = transform_text(input_sms)

        # 2. vectorize
        vector_input = tfidf.transform([transformed_sms])

        # 3. predict
        result = model.predict(vector_input)[0]

        # 4. display
        if result == 1:
            st.error("🚨 Spam Message")
        else:
            st.success("✅ Not Spam")
