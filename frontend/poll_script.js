/**
 * Poll page script
 * Obsługuje wyświetlanie pytań, głosowanie i aktualizację wyników ankiety.
 */

const pathParts = window.location.pathname.split('/');
const pollId = pathParts[1];  // /<poll_id>

/**
 * Pobiera dane ankiety z backendu i renderuje pytania w DOM.
 *
 * @async
 * @returns {Promise<void>} Nic nie zwraca, aktualizuje DOM.
 */
async function fetchPoll() {
    const sessionId = getSessionId();
    const res = await fetch(`/polls/${pollId}?session_id=${sessionId}`);
    const data = await res.json();

    document.getElementById("poll-title").innerText = data.title;

    const container = document.getElementById("questions-container");
    container.innerHTML = "";

    let alreadyVoted = false;

    data.questions.forEach(q => {
        if (q.user_selected && q.user_selected.length > 0)
            alreadyVoted = true;
    });

    data.questions.forEach(q => {
        const qDiv = document.createElement("div");
        qDiv.classList.add("question-container");
        qDiv.dataset.qid = q.id;

        const textDiv = document.createElement("div");
        textDiv.classList.add("question-text");
        const qTitle = document.createElement("h3");
        qTitle.innerText = q.text;
        textDiv.appendChild(qTitle);

        const answersDiv = document.createElement("div");
        answersDiv.classList.add("question-answers");

        q.answers.forEach(a => {
            const label = document.createElement("label");
            label.classList.add("modern-option");

            const input = document.createElement("input");
            input.type = q.type === "single" ? "radio" : "checkbox";
            input.name = `question-${q.id}`;
            input.value = a.id;

            if (q.user_selected && q.user_selected.includes(a.id))
                input.checked = true;

            const text = document.createElement("span");
            text.innerText = a.text;

            label.appendChild(input);
            label.appendChild(text);
            answersDiv.appendChild(label);
        });

        textDiv.appendChild(answersDiv);
        qDiv.appendChild(textDiv);

        const resultDiv = document.createElement("div");
        resultDiv.classList.add("question-result");
        qDiv.appendChild(resultDiv);

        container.appendChild(qDiv);
    });

    if (alreadyVoted) {
        hideVoteButton();
        showResults();
    }
}

/**
 * Ukrywa przycisk głosowania.
 */
function hideVoteButton() {
    const btn = document.getElementById("vote-btn");
    if (btn) btn.style.display = "none";
}

/**
 * Generuje losowy UUID.
 *
 * @returns {string} Nowy identyfikator UUID.
 */
function uuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

/**
 * Pobiera lub tworzy unikalny identyfikator sesji użytkownika.
 *
 * @returns {string} Identyfikator sesji.
 */
function getSessionId() {
    let id = localStorage.getItem("sessionId");
    if (!id) {
        id = uuid();
        localStorage.setItem("sessionId", id);
    }
    return id;
}

/**
 * Obsługuje wysyłanie głosów po submitcie formularza.
 *
 * @param {Event} e - Obiekt zdarzenia submit.
 */
document.getElementById("poll-form").addEventListener("submit", async e => {
    e.preventDefault();

    const votes = [];
    const sessionId = getSessionId();

    document.querySelectorAll("#questions-container > .question-container").forEach(qDiv => {
        const qid = qDiv.dataset.qid;
        qDiv.querySelectorAll("input:checked").forEach(inp => {
            votes.push({
                poll_id: pollId,
                question_id: parseInt(qid),
                answer_id: parseInt(inp.value),
                session_id: sessionId
            });
        });
    });

    await fetch("/votes/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ votes })
    });

    hideVoteButton();
    showResults();
});

/**
 * Generuje tablicę kolorów HSL dla wykresów.
 *
 * @param {number} n - Liczba kolorów do wygenerowania.
 * @returns {string[]} Tablica kolorów w formacie HSL.
 */
function generateColors(n) {
    return Array.from({ length: n }, (_, i) =>
        `hsl(${(i * 47) % 360}, 70%, 55%)`
    );
}

/**
 * Mapa przechowująca instancje Chart dla każdego pytania.
 * @type {Map<number, Chart>}
 */
const CHARTS = new Map();

/**
 * Renderuje wyniki ankiety w postaci wykresów.
 *
 * @async
 * @returns {Promise<void>} Nic nie zwraca, aktualizuje DOM i wykresy.
 */
async function showResults() {
    const res = await fetch(`/polls/${pollId}/results`);
    const data = await res.json();

    data.forEach(q => {
        const qDiv = document.querySelector(`.question-container[data-qid='${q.id}']`);
        if (!qDiv) return;

        const resultDiv = qDiv.querySelector(".question-result");
        resultDiv.innerHTML = "";

        const canvas = document.createElement("canvas");
        const canvasId = `chart-${q.id}`;
        canvas.id = canvasId;
        resultDiv.appendChild(canvas);

        const ctx = canvas.getContext("2d");

        if (CHARTS.has(q.id)) {
            try { CHARTS.get(q.id).destroy(); } catch (e) {}
            CHARTS.delete(q.id);
        }

        const cfg = q.type === "single" ? {
            type: "pie",
            data: {
                labels: q.answers.map(a => a.text),
                datasets: [{ label: "Głosy", data: q.answers.map(a => a.votes), backgroundColor: generateColors(q.answers.length) }]
            },
            options: { responsive: true, plugins: { legend: { display: true, position: 'bottom' } } }
        } : {
            type: "bar",
            data: {
                labels: q.answers.map(a => a.text),
                datasets: [{ label: "Głosy", data: q.answers.map(a => a.votes), backgroundColor: generateColors(q.answers.length) }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: { legend: { display: false } },
                scales: { x: { beginAtZero: true, ticks: { precision: 0, stepSize: 1 }, suggestedMin: 0 } }
            }
        };

        const chart = new Chart(ctx, cfg);
        CHARTS.set(q.id, chart);
    });
}

/**
 * Inicjalizuje połączenie WebSocket do ankiety.
 */
function initWebSocket() {
    const ws = new WebSocket(`ws://${window.location.host}/polls/${pollId}/ws`);

    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.results) updateResultsUI(msg.results);
    };

    ws.onclose = () => {
        setTimeout(initWebSocket, 1000);
    };
}

/**
 * Aktualizuje UI wykresów po otrzymaniu danych z WebSocket.
 *
 * @param {Object[]} results - Tablica pytań z danymi wyników.
 */
function updateResultsUI(results) {
    results.forEach(q => {
        const qDiv = document.querySelector(`.question-container[data-qid='${q.id}']`);
        if (!qDiv) return;

        const resultDiv = qDiv.querySelector(".question-result");
        resultDiv.innerHTML = "";

        const canvas = document.createElement("canvas");
        resultDiv.appendChild(canvas);

        const ctx = canvas.getContext("2d");

        if (CHARTS.has(q.id)) {
            try { CHARTS.get(q.id).destroy(); } catch (e) {}
            CHARTS.delete(q.id);
        }

        const cfg = q.type === "single" ? {
            type: "pie",
            data: { labels: q.answers.map(a => a.text), datasets: [{ label: "Głosy", data: q.answers.map(a => a.votes), backgroundColor: generateColors(q.answers.length) }] },
            options: { responsive: true, plugins: { legend: { display: true, position: 'bottom' } } }
        } : {
            type: "bar",
            data: { labels: q.answers.map(a => a.text), datasets: [{ label: "Głosy", data: q.answers.map(a => a.votes), backgroundColor: generateColors(q.answers.length) }] },
            options: { responsive: true, indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, ticks: { precision: 0, stepSize: 1 }, suggestedMin: 0 } } }
        };

        const chart = new Chart(ctx, cfg);
        CHARTS.set(q.id, chart);
    });
}

// Start po fetchu danych ankiety
fetchPoll().then(() => {
    initWebSocket();
});
