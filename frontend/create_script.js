/**
 * Create Poll Script
 * Obsługuje tworzenie ankiety, dodawanie/usuwanie pytań i odpowiedzi,
 * oraz wysyłanie danych do backendu.
 */

let questions = [];

/**
 * Generuje losowy identyfikator dla pytania lub odpowiedzi.
 *
 * @returns {string} Unikalny identyfikator.
 */
function uuid() {
    return "_" + Math.random().toString(36).substring(2, 9);
}

/**
 * Dodaje nowe pytanie do ankiety.
 */
function addQuestion() {
    questions.push({
        id: uuid(),
        text: "",
        type: "single",
        answers: []
    });
    render();
}

/**
 * Usuwa pytanie po jego identyfikatorze.
 *
 * @param {string} qid - Id pytania do usunięcia.
 */
function removeQuestion(qid) {
    questions = questions.filter(x => x.id !== qid);
    render();
}

/**
 * Aktualizuje tekst pytania.
 *
 * @param {string} qid - Id pytania.
 * @param {string} t - Nowy tekst pytania.
 */
function updateQuestionText(qid, t) {
    questions.find(q => q.id === qid).text = t;
}

/**
 * Aktualizuje typ pytania (single/multi).
 *
 * @param {string} qid - Id pytania.
 * @param {string} t - Typ pytania ("single" lub "multi").
 */
function updateQuestionType(qid, t) {
    questions.find(q => q.id === qid).type = t;
}

/**
 * Dodaje nową odpowiedź do pytania.
 *
 * @param {string} qid - Id pytania, do którego dodajemy odpowiedź.
 */
function addAnswer(qid) {
    const q = questions.find(q => q.id === qid);
    q.answers.push({ id: uuid(), text: "" });
    render();
}

/**
 * Usuwa odpowiedź z pytania.
 *
 * @param {string} qid - Id pytania.
 * @param {string} aid - Id odpowiedzi do usunięcia.
 */
function removeAnswer(qid, aid) {
    const q = questions.find(q => q.id === qid);
    q.answers = q.answers.filter(a => a.id !== aid);
    render();
}

/**
 * Aktualizuje tekst odpowiedzi.
 *
 * @param {string} qid - Id pytania.
 * @param {string} aid - Id odpowiedzi.
 * @param {string} t - Nowy tekst odpowiedzi.
 */
function updateAnswerText(qid, aid, t) {
    const q = questions.find(q => q.id === qid);
    q.answers.find(a => a.id === aid).text = t;
}

/**
 * Renderuje wszystkie pytania i odpowiedzi w DOM.
 */
function render() {
    const container = document.getElementById("questions");
    container.innerHTML = "";

    questions.forEach(q => {
        const div = document.createElement("div");
        div.className = "card shadow-sm p-3 mb-4 question-card";

        div.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="mb-0">Pytanie</h5>
                <i class="bi bi-trash remove-btn fs-4" onclick="removeQuestion('${q.id}')"></i>
            </div>

            <div class="mb-3">
                <input type="text" class="form-control" placeholder="Treść pytania"
                       value="${q.text}"
                       oninput="updateQuestionText('${q.id}', this.value)">
            </div>

            <div class="mb-3">
                <select class="form-select"
                        onchange="updateQuestionType('${q.id}', this.value)">
                    <option value="single" ${q.type === "single" ? "selected" : ""}>Jednokrotnego wyboru</option>
                    <option value="multi" ${q.type === "multi" ? "selected" : ""}>Wielokrotnego wyboru</option>
                </select>
            </div>

            <label class="form-label fw-semibold mb-2">Odpowiedzi</label>
            <div class="answers"></div>

            <button class="btn btn-outline-primary btn-sm mt-2"
                    onclick="addAnswer('${q.id}')">
                <i class="bi bi-plus"></i> Dodaj odpowiedź
            </button>
        `;

        const answersDiv = div.querySelector(".answers");
        q.answers.forEach(a => {
            const line = document.createElement("div");
            line.className = "d-flex align-items-center gap-2 mb-2 answer-line";

            line.innerHTML = `
                <input type="text" class="form-control" placeholder="Odpowiedź"
                       value="${a.text}"
                       oninput="updateAnswerText('${q.id}', '${a.id}', this.value)">
                <i class="bi bi-x-circle remove-btn"
                   onclick="removeAnswer('${q.id}', '${a.id}')"></i>
            `;
            answersDiv.appendChild(line);
        });

        container.appendChild(div);
    });
}

/**
 * Wysyła ankietę do backendu.
 *
 * @async
 * @returns {Promise<void>} Nic nie zwraca, aktualizuje UI w zależności od wyniku.
 */
async function submitPoll() {
    const title = document.getElementById("poll-title").value;

    const payload = {
        title: title,
        questions: questions.map(q => ({
            text: q.text,
            type: q.type,
            answers: q.answers.map(a => ({ text: a.text }))
        }))
    };

    const res = await fetch("/polls/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    const box = document.getElementById("result-box");
    box.classList.remove("d-none");

    if (!data.ok) {
        box.classList.remove("alert-success");
        box.classList.add("alert-danger");

        box.innerHTML = `
            ❌ <strong>Nie udało się utworzyć ankiety.</strong><br><br>
            ${data.errors.map(e => `• ${e}`).join("<br>            ")}
        `;
        return;
    }

    const pollUrl = `/${data.poll_id}`;

    box.classList.remove("alert-danger");
    box.classList.add("alert-success");
    box.innerHTML = `
        ✅ <strong>Ankieta została utworzona!</strong><br>
        <a href="${pollUrl}" class="fw-bold">${window.location.origin}${pollUrl}</a>
    `;

    // czyszczenie formularza
    questions = [];
    render();
    document.getElementById("poll-title").value = "";
}
