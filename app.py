from flask import Flask, render_template, request
from docx import Document

app = Flask(__name__)
questions_data = []

# 🧠 1. HÀM PARSE WORD
def parse_docx(file):
    doc = Document(file)
    lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    questions = []
    q = {}

    for line in lines:
        if line.startswith("Câu hỏi"):
            if q:
                questions.append(q)
            q = {"question": line.replace("Câu hỏi:", "").strip(), "options": [], "answer": ""}
        
        elif line.startswith(("A.", "B.", "C.", "D.")):
            q["options"].append(line[3:].strip())
        
        elif line.startswith("Đáp án"):
            ans = line.split(":")[1].strip()
            index = ord(ans) - ord('A')
            if index < len(q["options"]):
                q["answer"] = q["options"][index]

    if q:
        questions.append(q)

    return questions


# 🟢 2. ROUTE UPLOAD (DÁN Ở ĐÂY)
@app.route('/', methods=['GET', 'POST'])
def upload_page():
    global questions_data   # 👈 THÊM DÒNG NÀY

    if request.method == 'POST':
        file = request.files['file']

        if file.filename.endswith('.docx'):
            questions_data = parse_docx(file)   # 👈 LƯU LẠI
            return render_template('quiz.html', questions=questions_data)

    return render_template('upload.html')

# 🟢 3. GIỮ NGUYÊN ROUTE SUBMIT (NẾU BẠN ĐÃ CÓ)
# (đừng xoá phần chấm điểm của bạn)
@app.route('/submit', methods=['POST'])
def submit():
    results = []
    score = 0

    for i, q in enumerate(questions_data):
        user_answer = request.form.get(f"q{i}")
        correct_answer = q["answer"]

        is_correct = user_answer == correct_answer
        if is_correct:
            score += 1

        results.append({
            "question": q["question"],
            "options": q["options"],
            "correct": correct_answer,
            "user": user_answer,
            "is_correct": is_correct
        })

    return render_template(
        "result.html",
        results=results,
        score=score,
        total=len(questions_data)
    )


# 🟢 4. CHẠY APP
if __name__ == '__main__':
    app.run(debug=True)