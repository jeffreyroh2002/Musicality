const questions = [
    "How would you rate the mood of the music?",
    // Add more questions as needed
];

let currentQuestionIndex = 0;

function loadCurrentQuestion() {
    const currentQuestionContainer = document.getElementById('current-question-container');
    currentQuestionContainer.innerHTML = `
        <div class="question">
            <label for="question${currentQuestionIndex + 1}">${questions[currentQuestionIndex]}</label>
            <input type="range" id="question${currentQuestionIndex + 1}" name="question${currentQuestionIndex + 1}" min="1" max="10">
            <span id="question${currentQuestionIndex + 1}Value">5</span>
        </div>
    `;
}

function nextQuestion() {
    // Collect and store the user's rating for the current question
    const currentRating = document.getElementById(`question${currentQuestionIndex + 1}`).value;
    // Store or send the rating to the backend as needed

    // Move to the next question
    currentQuestionIndex++;

    // Check if there are more questions
    if (currentQuestionIndex < questions.length) {
        loadCurrentQuestion();
    } else {
        // If all questions are answered, submit the ratings
        submitRating();
    }
}

function submitRating() {
    // Collect and store the user's rating for the last question
    const lastRating = document.getElementById(`question${currentQuestionIndex}`).value;
    // Store or send the rating to the backend as needed

    // Perform additional actions if necessary before displaying the analysis results

    // Display loading message or spinner if needed

    // After receiving the analysis results from the backend, update the DOM
    // Example: Replace the following lines with actual analysis results
    document.getElementById('genreResult').innerText = 'Genre: Pop';
    document.getElementById('moodResult').innerText = 'Mood: Happy';

    // Display the analysis results section
    document.getElementById('questionnaire').style.display = 'none';
    document.getElementById('analysis-results').style.display = 'block';
}

// Load the first question when the page loads
window.onload = loadCurrentQuestion;