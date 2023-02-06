# import necessary libraries
from flask import Flask, request, app, jsonify, url_for, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
from nltk.stem import WordNetLemmatizer
from train import generate_greeting_response, generate_response, article_sentences
import train
import nltk
import io
import runpy
import os
import re
import docx
import importlib
import random
import string  # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
nltk.download('popular', quiet=True)  # for downloading packages
# uncomment the following only the first time
# nltk.download('punkt') # first-time use only
# nltk.download('wordnet') # first-time use only

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.docx', '.doc', '.txt']


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index1.html', files=files)


@app.route('/', methods=['POST'])
def upload_files():
    filename = False
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    # runpy.run_path(path_name='app.py')
    importlib.reload(train)
    # filename1=filename
    print(filename)
    if filename:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route("/get1")
def home():
    return render_template("index.html")

# get method


@app.route("/get")
def get_bot_response():
    importlib.reload(train)
    userText = request.args.get('msg')
    continue_dialogue = True
    # print("Hello, I am your Chatbot. You can ask me any question regarding Cricket:")
    while (continue_dialogue == True):
        human_text = userText
        human_text = human_text.lower()
        if human_text != 'bye':
            if human_text == 'thanks' or human_text == 'thank you very much' or human_text == 'thank you':
                continue_dialogue = False
                return "Chatbot: Most welcome"
            else:
                if generate_greeting_response(human_text) != None:
                    return "Chatbot: " + generate_greeting_response(human_text)
                else:
                    # print("Chatbot: ", end="")
                    # print(generate_response(human_text))
                    x = "Chatbot: "+generate_response(human_text)
                    # article_sentences.remove(human_text)
                    return x
        else:
            continue_dialogue = False
            return "Chatbot: Good bye and take care of yourself..."


# A welcome message to test our server

# # function defination for reading the word file (corpus)
if __name__ == "__main__":
    app.run(debug=True)
