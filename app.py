from flask import Flask, render_template, request, jsonify
import io
import contextlib
import random

app = Flask(__name__)

# ✅ 문제 리스트 (다양한 출력 예측 문제)
questions = [
    {
        'id': 1,
        'code': 'x = 3\nx += 4\nprint(x)',
        'expected_output': '7'
    },
    {
        'id': 2,
        'code': 'a = 10\nb = 3\nprint(a // b)',
        'expected_output': '3'
    },
    {
        'id': 3,
        'code': 'text = "Hello"\nprint(text[1])',
        'expected_output': 'e'
    },
    {
        'id': 4,
        'code': 'for i in range(1, 4):\n    print(i * "*")',
        'expected_output': '*\n**\n***'
    },
    {
        'id': 5,
        'code': 'total = 0\nfor i in range(1, 6):\n    total += i\nprint(total)',
        'expected_output': '15'
    },
    {
        'id': 6,
        'code': 'nums = [1, 3, 5]\nnums.append(7)\nprint(nums[-1])',
        'expected_output': '7'
    },
    {
        'id': 7,
        'code': 'x = 5\ny = x\nx = 10\nprint(y)',
        'expected_output': '5'
    },
    {
        'id': 8,
        'code': 'def greet(name):\n    return "Hi " + name\nprint(greet("Minji"))',
        'expected_output': 'Hi Minji'
    },
    {
        'id': 9,
        'code': 'for i in range(2, 7, 2):\n    print(i)',
        'expected_output': '2\n4\n6'
    },
    {
        'id': 10,
        'code': 's = "python"\nprint(s.upper())',
        'expected_output': 'PYTHON'
    }
]

# ✅ 현재 출제된 문제를 기억하기 위한 변수
current_question = {'code': '', 'expected_output': ''}

@app.route('/')
def index():
    # 문제 무작위 선택
    question = random.choice(questions)
    current_question['code'] = question['code']
    current_question['expected_output'] = question['expected_output']
    return render_template('index.html', code=question['code'])

@app.route('/check', methods=['POST'])
def check():
    user_answer = request.json.get('answer', '').strip()

    # 문제 코드 가져와서 실행
    code = current_question['code']

    output_buffer = io.StringIO()
    with contextlib.redirect_stdout(output_buffer):
        try:
            exec(code, {})  # 보안상 제한된 환경에서만 사용할 것
        except Exception as e:
            actual_output = f'Error: {e}'
        else:
            actual_output = output_buffer.getvalue().strip()

    # 정답 비교
    is_correct = user_answer == actual_output

    return jsonify({
        'correct': is_correct,
        'correct_output': actual_output
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
