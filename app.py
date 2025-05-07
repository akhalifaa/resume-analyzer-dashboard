from flask import Flask, render_template, request
import os
from pdfminer.high_level import extract_text
import docx
import spacy
from collections import Counter
import string
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from auth import auth, User

# flask app for login management
app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Required for sessions
app.register_blueprint(auth)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text.lower())
    # Keep nouns and proper nouns, filter punctuation and stop words
    keywords = [
        token.lemma_ for token in doc
        if token.pos_ in ['NOUN', 'PROPN'] and
           token.text not in string.punctuation and
           not token.is_stop
    ]
    return Counter(keywords)


def extract_resume_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text(file_path)
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        return "Unsupported file format"


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        resume = request.files['resume']
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        resume.save(resume_path)

        resume_text = extract_resume_text(resume_path)
        jobdesc_text = request.form['jobdesc_text']

        # Keyword extraction
        resume_keywords = extract_keywords(resume_text)
        jobdesc_keywords = extract_keywords(jobdesc_text)

        # Matching keywords
        matched = set(resume_keywords) & set(jobdesc_keywords)
        missing = set(jobdesc_keywords) - set(resume_keywords)
        match_percentage = round(len(matched) / len(set(jobdesc_keywords)) * 100, 2) if jobdesc_keywords else 0

        print("Matched Keywords:", matched)
        print("Match Percentage:", match_percentage)

        return render_template('results.html', match_percentage=match_percentage, matched_keywords=matched, missing_keywords=missing)


    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
