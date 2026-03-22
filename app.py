from flask import Flask, render_template, request
import json
import io

app = Flask(__name__)

questions_data = []  # lưu tạm câu hỏi

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global questions_data

    file = request.files['file']

    if file:
        questions_data = json.load(io.TextIOWrapper(file, encoding='utf-8'))
        return render_template('quiz.html', questions=questions_data)

    return "Không có file!"

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

if __name__ == '__main__':
    app.run(debug=True)