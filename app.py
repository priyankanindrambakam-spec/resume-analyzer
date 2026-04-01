from flask import Flask, render_template, request
import os
import PyPDF2

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Industry Standard Skills
KEYWORDS = ['python', 'java', 'html', 'css', 'javascript', 'sql', 'flask', 'git', 'react', 'aws', 'c', 'cpp', 'excel', 'communication', 'problem solving', 'agile']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['resume']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    resume_text = ""
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            resume_text += page.extract_text().lower()

    found_skills = [skill for skill in KEYWORDS if skill in resume_text]
    missing_skills = [skill for skill in KEYWORDS if skill not in found_skills]
    
    score = int((len(found_skills) / len(KEYWORDS)) * 100)

    # Professional Job Role Mapping
    job_roles = []
    if 'python' in found_skills and 'flask' in found_skills:
        job_roles.append("Python Backend Developer")
    if 'html' in found_skills and 'css' in found_skills:
        job_roles.append("UI/UX Web Developer")
    if 'sql' in found_skills:
        job_roles.append("Database Engineer")

    # Professional Feedback
    if score < 40:
        feedback = "Focus on learning core technical skills and building basic projects."
    elif score < 70:
        feedback = "Good progress! Adding more tools like Git or Cloud will improve your profile."
    else:
        feedback = "Strong profile! You are ready for entry-level professional roles."

    return f"""
    <body style="font-family: 'Segoe UI', sans-serif; text-align: center; margin-top: 50px; background-color: #f4f7f6;">
        <div style="background: white; width: 65%; margin: auto; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <h1 style="color: #2c3e50;">Analysis Report</h1>
            <div style="font-size: 48px; font-weight: bold; color: {'#27ae60' if score > 50 else '#e67e22'}; margin: 20px 0;">
                {score}%
            </div>
            <p style="color: #7f8c8d; font-size: 18px;">Overall Compatibility Score</p>
            <hr style="border: 0.5px solid #eee;">
            
            <h3 style="color: #2980b9;">Suggested Job Roles:</h3>
            <div style="margin-bottom: 20px;">
                {"".join([f"<span style='display:inline-block; background:#d6eaf8; color:#2980b9; padding:5px 15px; border-radius:20px; margin:5px;'>{role}</span>" for role in job_roles]) if job_roles else "Continue learning to unlock career paths."}
            </div>

            <table style="width: 100%; text-align: left; margin-top: 20px; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><b>Matched Skills:</b></td>
                    <td style="padding: 10px; border-bottom: 1px solid #eee; color: #27ae60;">{", ".join(found_skills).upper() if found_skills else "None"}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><b>Gap Analysis:</b></td>
                    <td style="padding: 10px; border-bottom: 1px solid #eee; color: #e74c3c;">{", ".join(missing_skills).upper()}</td>
                </tr>
            </table>

            <div style="background: #fdf2e9; padding: 20px; border-radius: 10px; margin-top: 30px; border-left: 5px solid #e67e22;">
                <h4 style="margin: 0; color: #d35400;">Career Advice:</h4>
                <p style="margin: 10px 0 0; color: #a04000;">{feedback}</p>
            </div>

            <br><br>
            <a href="/" style="text-decoration: none; background: #2c3e50; color: white; padding: 12px 30px; border-radius: 5px; font-weight: bold;">Analyze Another Resume</a>
        </div>
    </body>
    """

if __name__ == '__main__':
    app.run(debug=True)