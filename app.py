from flask import Flask, render_template, request
import os
from pdfminer.high_level import extract_text
import docx

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def extract_resume_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text(file_path)
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        return "Unsupported file format"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume = request.files['resume']
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        resume.save(resume_path)

        # Extract text from uploaded resume
        resume_text = extract_resume_text(resume_path)

        # Get job description from textarea
        jobdesc_text = request.form['jobdesc_text']

        # For now, just print them (truncate long text)
        print("RESUME TEXT (first 300 chars):", resume_text[:300])
        print("JOB DESC TEXT (first 300 chars):", jobdesc_text[:300])

        return "Resume and job description received and parsed!"
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
