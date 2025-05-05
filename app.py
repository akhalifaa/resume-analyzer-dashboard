from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Save the resume file
        resume = request.files['resume']
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        resume.save(resume_path)

        # Get job description text
        jobdesc_text = request.form['jobdesc_text']

        # For now, just print to confirm
        print("Resume saved to:", resume_path)
        print("Job Description Text:", jobdesc_text[:100])  # Print first 100 chars

        return "Files and job description text received!"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
