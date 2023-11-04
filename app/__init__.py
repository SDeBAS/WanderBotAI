from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
import re
import pandas as pd

app = Flask(__name__)

# Load your data and perform any necessary preprocessing (if not already done in chatbot.py)

# Example data loading:
df = pd.read_csv('college.csv', encoding='latin1')  # or 'iso-8859-1', depending on the actual encoding of the CSV file

# Chatbot responses dictionary
chatbot_responses = {}  # You can load your responses here

# Implement a function to load your responses into chatbot_responses dictionary
# Example function:
# def load_responses():
#     global chatbot_responses
#     # Load your responses into chatbot_responses here

# Load your responses
# load_responses()

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chatting')
def chatting():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    
    # Call the chatbot function to get the response
    chatbot_response = chatbot(user_input)
    
    # Extract the matching question and response
    matching_question = chatbot_response['match']
    bot_response = chatbot_response['response']
    
    # You can add more logic here if needed
    
    # Return the bot's response as JSON
    return jsonify({
        'user_input': user_input,
        'matching_question': matching_question,
        'bot_response': bot_response
    })

if __name__ == "__main__":
    app.run(debug=True)
