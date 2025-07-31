// Wait for the DOM to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {
    // --- STATE ---
    // We will store the authentication token here in memory.
    // It will be lost on page refresh, which is a security trade-off for simplicity.
    let authToken = null;

    // --- DOM ELEMENTS ---
    const loginForm = document.getElementById('login-form');
    const loginSection = document.getElementById('login-section');
    const appSection = document.getElementById('app-section');
    const welcomeMessage = document.getElementById('welcome-message');
    const loginError = document.getElementById('login-error');
    const usernameInput = document.getElementById('username');
    const notesList = document.getElementById('notes-list');
    const createNoteForm = document.getElementById('create-note-form');
    const showCreateNoteBtn = document.getElementById('show-create-note-btn');
    const createNoteContainer = document.getElementById('create-note-container');
    // It's more efficient to get these elements once, outside the event listener.
    const noteTitleInput = document.getElementById('note-title');
    const noteDescriptionInput = document.getElementById('note-description');
    const noteTagsInput = document.getElementById('note-tags');


    // --- API FUNCTIONS ---

    /**
     * Fetches notes from the API and displays them on the page.
     */
    const fetchAndDisplayNotes = async () => {
        if (!authToken) {
            console.error("Cannot fetch notes without an auth token.");
            return;
        }

        try {
            const response = await fetch('/notes/', {
                method: 'GET',
                headers: {
                    // This is where we use the stored token!
                    'Authorization': authToken,
                },
            });

            if (response.status === 404) {
                notesList.innerHTML = '<p>Nenhuma nota encontrada. Crie uma!</p>';
                return;
            }

            const notes = await response.json();
            renderNotes(notes);

        } catch (error) {
            console.error('Failed to fetch notes:', error);
            notesList.innerHTML = '<p style="color: red;">Não foi possível carregar as notas.</p>';
        }
    };

    // --- EVENT LISTENERS ---

    // Handle showing the create note form
    showCreateNoteBtn.addEventListener('click', () => {
        // Toggle the form's visibility
        createNoteContainer.style.display = createNoteContainer.style.display === 'none' ? 'block' : 'none';
    });

    // Use event delegation to handle clicks on dynamically created buttons.
    notesList.addEventListener('click', async (event) => {
        const target = event.target;

        // Check if a delete button was the target of the click
        if (target.classList.contains('delete-btn')) {
            const noteId = target.dataset.noteId;
            // Ask for user confirmation before deleting
            if (confirm('Você tem certeza que deseja apagar esta nota?')) {
                try {
                    const response = await fetch(`/notes/${noteId}`, {
                        method: 'DELETE',
                        headers: { 'Authorization': authToken }
                    });

                    if (response.ok) {
                        // If deletion is successful, refresh the notes list
                        await fetchAndDisplayNotes();
                    } else {
                        const errorData = await response.json();
                        alert(`Erro ao apagar nota: ${errorData.detail}`);
                    }
                } catch (error) {
                    console.error('Failed to delete note:', error);
                    alert('Ocorreu um erro ao apagar a nota.');
                }
            }
        }

        // Handle showing the EDIT form
        if (target.classList.contains('edit-btn')) {
            const noteItem = target.closest('.note-item');
            noteItem.querySelector('.note-display').style.display = 'none';
            noteItem.querySelector('.note-edit-form').style.display = 'block';
        }

        // Handle CANCELING an edit
        if (target.classList.contains('cancel-edit-btn')) {
            const noteItem = target.closest('.note-item');
            const editForm = noteItem.querySelector('.note-edit-form');
            editForm.reset(); // Resets form to initial values
            editForm.style.display = 'none';
            noteItem.querySelector('.note-display').style.display = 'block';
        }
    });

    // Use event delegation for submitting the dynamically created EDIT forms
    notesList.addEventListener('submit', async (event) => {
        event.preventDefault();
        const form = event.target;

        if (form.classList.contains('note-edit-form')) {
            const noteId = form.dataset.noteId;
            const updatedNote = {
                note_title: form.querySelector('.edit-title').value,
                note_description: form.querySelector('.edit-description').value,
                note_tags: form.querySelector('.edit-tags').value
            };

            try {
                const response = await fetch(`/notes/${noteId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json', 'Authorization': authToken },
                    body: JSON.stringify(updatedNote)
                });

                if (response.ok) {
                    await fetchAndDisplayNotes(); // Refresh list on success
                } else {
                    const errorData = await response.json();
                    alert(`Erro ao atualizar nota: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Failed to update note:', error);
                alert('Ocorreu um erro ao atualizar a nota.');
            }
        }
    });

    // Handle the create note form submission
    createNoteForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const noteData = {
            note_title: noteTitleInput.value,
            note_description: noteDescriptionInput.value,
            note_tags: noteTagsInput.value
        };

        try {
            const response = await fetch('/notes/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': authToken,
                },
                body: JSON.stringify(noteData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert(`Erro ao criar nota: ${errorData.detail}`);
            } else {
                // Clear the form fields
                createNoteForm.reset();
                // Hide the form container after successful creation
                createNoteContainer.style.display = 'none';
                // Refresh the notes list to show the new note
                await fetchAndDisplayNotes();
            }
        } catch (error) {
            console.error('Failed to create note:', error);
            alert('Ocorreu um erro ao criar a nota.');
        }
    });

    // Handle the login form submission
    loginForm.addEventListener('submit', async (event) => {
        // Prevent the default form action (page reload)
        event.preventDefault();

        const username = usernameInput.value.trim();
        if (!username) {
            loginError.textContent = 'Por favor, digite um nome de usuário.';
            return;
        }

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: username }),
            });

            const data = await response.json();

            if (!response.ok) {
                // If the API returns an error (e.g., 4xx, 5xx), handle it
                loginError.textContent = data.detail || 'Ocorreu um erro desconhecido.';
            } else {
                // Login was successful
                loginError.textContent = '';

                // Store the token from the response in our variable
                authToken = data.token;
                console.log('Login successful. Token stored.');

                // Show a welcome message with the username
                welcomeMessage.textContent = `Bem-vindo(a), ${username}!`;

                // Hide the login form and show the main app content
                loginSection.style.display = 'none';
                appSection.style.display = 'block';

                // Immediately fetch and display the user's notes
                await fetchAndDisplayNotes();
            }
        } catch (error) {
            // Handle network errors or issues with the fetch call itself
            console.error('Login request failed:', error);
            loginError.textContent = 'Falha ao conectar com o servidor. Por favor, tente novamente mais tarde.';
        }
    });

    // --- RENDER FUNCTIONS ---

    /**
     * Renders a list of note objects into the DOM.
     * @param {Array<Object>} notes - The array of notes to display.
     */
    const renderNotes = (notes) => {
        notesList.innerHTML = ''; // Clear current list
        notes.forEach(note => {
            const noteElement = document.createElement('div');
            noteElement.className = 'note-item';

            const tagsString = note.note_tags || '';
            noteElement.innerHTML = `
                <!-- Part 1: The content that is normally visible -->
                <div class="note-display">
                    <h4>${note.note_title}</h4>
                    <p>${note.note_description || ''}</p>
                    <small>Tags: ${tagsString || 'nenhuma'}</small>
                    <div class="note-actions">
                        <button class="edit-btn">Editar</button>
                        <button class="delete-btn" data-note-id="${note.note_id}">Apagar</button>
                    </div>
                </div>

                <!-- Part 2: The hidden form for editing -->
                <form class="note-edit-form" data-note-id="${note.note_id}" style="display: none;">
                    <input type="text" class="edit-title" value="${note.note_title}" required>
                    <textarea class="edit-description">${note.note_description || ''}</textarea>
                    <input type="text" class="edit-tags" value="${tagsString}">
                    <div class="note-actions">
                        <button type="submit">Salvar</button>
                        <button type="button" class="cancel-edit-btn">Cancelar</button>
                    </div>
                </form>
            `;
            notesList.appendChild(noteElement);
        });
    };
});