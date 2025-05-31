document.addEventListener('DOMContentLoaded', function () {
    const submitBtn = document.getElementById('submit-btn');
    const nextBtn = document.getElementById('next-btn');
    const answerInput = document.getElementById('user-answer');
    const resultBox = document.getElementById('result');
    const codeBox = document.getElementById('code');

    // 🔹 정답 제출
    submitBtn.addEventListener('click', function () {
        const userAnswer = answerInput.value.trim();

        fetch('/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ answer: userAnswer })
        })
        .then(response => response.json())
        .then(data => {
            if (data.correct) {
                resultBox.textContent = '🎉 정답입니다!';
                resultBox.style.color = 'green';
            } else {
                resultBox.textContent = `❌ 오답입니다. 정답은: ${data.correct_output}`;
                resultBox.style.color = 'red';
            }
        })
        .catch(error => {
            resultBox.textContent = '⚠️ 서버 오류가 발생했습니다.';
            resultBox.style.color = 'darkorange';
            console.error('Error:', error);
        });
    });

    // 🔹 다음 문제 불러오기
    nextBtn.addEventListener('click', function () {
        fetch('/new-question')
            .then(response => response.json())
            .then(data => {
                codeBox.textContent = data.code;  // 새 코드 표시
                answerInput.value = '';           // 입력 초기화
                resultBox.textContent = '';       // 결과 초기화
            })
            .catch(error => {
                resultBox.textContent = '⚠️ 문제를 불러오는 데 실패했습니다.';
                resultBox.style.color = 'darkorange';
                console.error('Error:', error);
            });
    });
});
