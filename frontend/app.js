const API_BASE = "http://127.0.0.1:8000/api";
const userId = localStorage.getItem("user_id");

// ------------------ REDIRECT IF NOT LOGGED IN ------------------
// Only redirect if not on login/signup pages
if (!userId && !["/index.html", "/signup.html"].includes(window.location.pathname)) {
    window.location.href = "index.html";
}


// ------------------ LOGIN HANDLER ------------------

// ------------------ LOGIN HANDLER ------------------

// LOGIN HANDLER
if (window.location.pathname === "/index.html") {
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();

            
            const email = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            fetch(`${API_BASE}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }) //
            })
            .then(res => res.json())
            .then(data => {
                if (data.user_id) {
                    localStorage.setItem("user_id", data.user_id);
                    window.location.href = "dashboard.html";
                } else {
                    alert("Invalid login");
                }
            });
        });
    }
}


// ------------------ SIGNUP HANDLER ------------------
if (window.location.pathname === "/signup.html") {
    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const email = document.getElementById("signupEmail").value;
            const password = document.getElementById("signupPassword").value;

            fetch(`${API_BASE}/signup`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            })
            .then(res => res.json())
            .then(data => {
                if (data.user_id) {
                    localStorage.setItem("user_id", data.user_id);
                    window.location.href = "dashboard.html";
                } else {
                    alert("Signup failed");
                }
            });
        });
    }
}

// ------------------ LOGOUT ------------------
function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}

// ------------------ DASHBOARD (NOTES PAGE) ------------------
if (userId && window.location.pathname === "/dashboard.html") {

    // Add Note
    const noteForm = document.getElementById("noteForm");
    if (noteForm) {
        noteForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const title = document.getElementById("noteTitle").value;
            const content = document.getElementById("noteContent").value;

            fetch(`${API_BASE}/notes`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, title, content })
            })
            .then(res => res.json())
            .then(() => {
                alert("Note added!");
                loadNotes();
                noteForm.reset();
            });
        });
    }

    // Load Notes
    function loadNotes() {
        fetch(`${API_BASE}/notes?user_id=${userId}`)
            .then(res => res.json())
            .then(data => renderNotes(data.notes || data));
    }

    // Render Notes
    function renderNotes(notes) {
        const list = document.getElementById("notesList");
        if (!list) return;
        list.innerHTML = "";

        notes.forEach(note => {
            list.innerHTML += `
                <div class="note-card">
                    <h4>${note.title}</h4>
                    <p>${note.content}</p>
                    <small>${note.created_at}</small><br><br>
                    <button onclick="openEditModal('${note.id}','${note.title}','${note.content}')">Edit</button>
                    <button onclick="deleteNote('${note.id}')">Delete</button>
                </div>
            `;
        });
    }

    // Filter Notes
    window.filterNotes = function() {
        const date = document.getElementById("filterDate").value;
        if (!date) { alert("Select a date"); return; }
        fetch(`${API_BASE}/notes/by-date?user_id=${userId}&date=${date}`)
            .then(res => res.json())
            .then(data => renderNotes(data));
    }

    // Delete Note
    window.deleteNote = function(id) {
        if (!confirm("Delete this note?")) return;
        fetch(`${API_BASE}/notes/${id}`, { method: "DELETE" })
            .then(res => res.json())
            .then(() => { alert("Note deleted"); loadNotes(); });
    }

    // Edit Note
    let editNoteId = "";
    window.openEditModal = function(id, title, content) {
        editNoteId = id;
        document.getElementById("editTitle").value = title;
        document.getElementById("editContent").value = content;
        document.getElementById("editModal").style.display = "block";
    }
    window.closeModal = function() { document.getElementById("editModal").style.display = "none"; }
    window.saveEdit = function() {
        const newTitle = document.getElementById("editTitle").value;
        const newContent = document.getElementById("editContent").value;

        fetch(`${API_BASE}/notes/${editNoteId}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: newTitle, content: newContent })
        })
        .then(res => res.json())
        .then(() => { alert("Note updated!"); closeModal(); loadNotes(); });
    }

    // Initial load
    loadNotes();
}
