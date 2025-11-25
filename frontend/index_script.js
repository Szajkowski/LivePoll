/**
 * Index page script
 * Obsługuje wyświetlanie listy ankiet oraz paginację.
 */

let currentPage = 1;
const limit = 10;

/**
 * Pobiera listę ankiet z backendu i renderuje je w DOM.
 *
 * @async
 * @param {number} [page=1] - Numer strony do załadowania.
 * @returns {Promise<void>} Nic nie zwraca, aktualizuje DOM.
 */
async function loadPolls(page = 1) {
    const res = await fetch(`/polls/list?page=${page}&limit=${limit}`);
    const data = await res.json();

    const root = document.getElementById("poll-list");
    root.innerHTML = "";

    if (data.polls.length === 0) {
        root.innerHTML = `<div class="alert alert-info">Brak ankiet do wyświetlenia.</div>`;
        return;
    }

    data.polls.forEach(p => {
        const item = document.createElement("a");
        item.className = "list-group-item list-group-item-action";
        item.href = `/${p.id}`;
        item.innerText = p.title;
        root.appendChild(item);
    });

    currentPage = data.page;
    renderPagination(currentPage, data.total);

    // disable prev/next buttons
    document.getElementById("prev-btn").disabled = currentPage <= 1;
    document.getElementById("next-btn").disabled = currentPage * limit >= data.total;
}

/**
 * Renderuje przyciski paginacji na podstawie liczby stron i aktualnej strony.
 *
 * @param {number} page - Aktualny numer strony.
 * @param {number} total - Całkowita liczba ankiet.
 */
function renderPagination(page, total) {
    const pages = Math.ceil(total / limit);
    const container = document.getElementById("pagination");
    container.innerHTML = "";

    if (pages <= 1) return;

    for (let p = 1; p <= pages; p++) {
        const btn = document.createElement("button");
        btn.className = "btn btn-sm mx-1 " + (p === page ? "btn-primary" : "btn-outline-primary");
        btn.innerText = p;

        btn.onclick = () => {
            if (p !== currentPage) loadPolls(p);
        };

        container.appendChild(btn);
    }
}

/**
 * Obsługa kliknięcia przycisku "Poprzednia strona".
 */
document.getElementById("prev-btn").onclick = () => {
    if (currentPage > 1) loadPolls(currentPage - 1);
};

/**
 * Obsługa kliknięcia przycisku "Następna strona".
 */
document.getElementById("next-btn").onclick = () => {
    loadPolls(currentPage + 1);
};

// Załaduj pierwszą stronę ankiet przy starcie
loadPolls(1);
