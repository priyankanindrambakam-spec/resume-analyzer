from flask import Flask, render_template, request, send_file, jsonify
import os
import PyPDF2
from fpdf import FPDF

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Full Jobs Database
JOBS_DB = {
    'Web Developer': ['html', 'css', 'javascript', 'react', 'flask', 'git', 'bootstrap'],
    'Data Analyst': ['python', 'sql', 'excel', 'power bi', 'tableau', 'pandas', 'statistics'],
    'Java Developer': ['java', 'spring boot', 'hibernate', 'sql', 'maven', 'junit'],
    'Python Developer': ['python', 'flask', 'django', 'postgresql', 'rest api', 'aws'],
    'Software Testing': ['manual testing', 'selenium', 'java', 'testng', 'cucumber', 'api testing'],
    'Cloud Engineer': ['aws', 'azure', 'docker', 'kubernetes', 'linux', 'terraform'],
    'Data Scientist': ['python', 'machine learning', 'deep learning', 'nlp', 'scikit-learn', 'sql'],
    'App Developer': ['flutter', 'dart', 'react native', 'android studio', 'ios', 'firebase']
}

@app.route('/')
def home():
    return render_template('index.html')

COURSE_LINKS = {
    "python": "https://www.youtube.com/results?search_query=python+full+course",
    "flask": "https://www.youtube.com/results?search_query=flask+python+tutorial",
    "django": "https://www.youtube.com/results?search_query=django+full+course",
    "aws": "https://www.youtube.com/results?search_query=aws+tutorial+for+beginners",
    "java": "https://www.youtube.com/results?search_query=java+full+course",
    "sql": "https://www.youtube.com/results?search_query=sql+tutorial+for+beginners",
    "machine learning": "https://www.youtube.com/results?search_query=machine+learning+full+course",
    "react": "https://www.youtube.com/results?search_query=react+js+full+course",
    "javascript": "https://www.youtube.com/results?search_query=javascript+full+course",
    "html": "https://www.youtube.com/results?search_query=html+css+tutorial",
    "css": "https://www.youtube.com/results?search_query=css+full+tutorial"
}
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return "No file uploaded"
    
    file = request.files['resume']
    if file.filename == '':
        return "No file selected"

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    resume_text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            resume_text += page.extract_text().lower()

    results = []
    for job_title, required_skills in JOBS_DB.items():
        matched_skills = [skill for skill in required_skills if skill.lower() in resume_text]
        missing_skills = [skill for skill in required_skills if skill.lower() not in resume_text]
        score = int((len(matched_skills) / len(required_skills)) * 100)

        recommendations = []
        for skill in missing_skills:
            link = COURSE_LINKS.get(skill.lower(), f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial")
            recommendations.append({'skill': skill, 'link': link})

        results.append({
            'role': job_title,
            'score': score,
            'matched': matched_skills,
            'missing': missing_skills,
            'recommendations': recommendations
        })

    results = sorted(results, key=lambda x: x['score'], reverse=True)
    return render_template('result.html', results=results)

@app.route('/download_report', methods=['POST'])
def download_report():
    data = request.get_json()
    results = data.get('results', [])

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AI Resume Analysis - Career Report", ln=True, align='C')
    pdf.ln(10)

    for res in results:
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, txt=f"Role: {res['role']} (Score: {res['score']}%)", ln=True)

        pdf.set_font("Arial", size=10)
        pdf.set_text_color(0, 128, 0)
        pdf.multi_cell(0, 8, txt=f"Matched Skills: {', '.join(res['matched'])}")
        
        pdf.set_text_color(255, 0, 0)
        pdf.multi_cell(0, 8, txt=f"Missing Skills: {', '.join(res['missing'])}")
        pdf.ln(5)

    report_path = os.path.join(UPLOAD_FOLDER, "analysis_report.pdf")
    pdf.output(report_path)
    return send_file(report_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)