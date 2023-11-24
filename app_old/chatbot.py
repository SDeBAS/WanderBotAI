import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer

# Load your data and perform any necessary preprocessing
df = pd.read_csv('college.csv')

# Chatbot Function
lemmatizer = WordNetLemmatizer()
tfidf = TfidfVectorizer()

# Preprocess and vectorize the queries
queries = df['Query'].apply(lambda x: lemmatizer.lemmatize(re.sub('[^a-zA-Z]', ' ', x).lower()))
tfidf_matrix = tfidf.fit_transform(queries)

def chatbot(user_input):
    # Preprocess the user input
    user_input = lemmatizer.lemmatize(re.sub('[^a-zA-Z]', ' ', user_input).lower())
    
    # Vectorize the user input
    user_input_vector = tfidf.transform([user_input])
    
    # Calculate cosine similarities between user input and queries
    similarities = cosine_similarity(user_input_vector, tfidf_matrix)
    
    # Find the most similar query
    most_similar_idx = similarities.argmax()
    matching_question = df.loc[most_similar_idx]['Query']
    response = df.loc[most_similar_idx]['Response']
    
    chat_dict = {
        'match': matching_question,
        'response': response,
    }
    
    return chat_dict
