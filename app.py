from flask import Flask, render_template, request
import os
import PyPDF2

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Step 2: Multiple Job Roles Database
JOBS_DB = {
    'Web Developer': ['html', 'css', 'javascript', 'react', 'flask', 'git', 'bootstrap'],
    'Data Analyst': ['python', 'sql', 'excel', 'power bi', 'tableau', 'pandas', 'statistics'],
    'Java Developer': ['java', 'spring boot', 'hibernate', 'sql', 'maven', 'junit'],
    'Python Developer': ['python', 'flask', 'django', 'postgresql', 'rest api', 'aws']
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return "No file uploaded"
    
    file = request.files['resume']
    if file.filename == '':
        return "No file selected"

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract Text
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text().lower()

    # Smart Matching Logic
    results = []
    for job_title, required_skills in JOBS_DB.items():
        matched_skills = [skill for skill in required_skills if skill in text]
        missing_skills = [skill for skill in required_skills if skill not in text]
        score = int((len(matched_skills) / len(required_skills)) * 100)
        
        results.append({
            'role': job_title,
            'score': score,
            'matched': matched_skills,
            'missing': missing_skills
        })

    # Sort results to show highest score first
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    return render_template('result.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)