document.addEventListener('DOMContentLoaded', function () {
    const submitBtn = document.getElementById('submit-btn');
    const answerInput = document.getElementById('user-answer');
    const resultBox = document.getElementById('result');

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
});
