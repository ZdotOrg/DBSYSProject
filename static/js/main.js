// ... 
//  WATCHLIST PAGE JAVASCRIPT
//  ...
 
 // Tab switching functionality
    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');

            // Remove active class from all tabs and contents
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

            // Add active class to clicked tab and corresponding content
            button.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Edit modal functionality
    const modal = document.getElementById('editModal');
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.cancel-btn');

    document.querySelectorAll('.edit-watchlist-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const listId = btn.getAttribute('data-list-id');

            // Fetch current watchlist item data
            try {
                const response = await fetch(`/api/watchlist/${listId}`);
                const data = await response.json();

                if (response.ok) {
                    document.getElementById('edit_list_id').value = data.list_id;
                    document.getElementById('watch_status').value = data.watch_status;
                    document.getElementById('user_score').value = data.user_score || '';
                    document.getElementById('episodes_watched').value = data.episodes_watched || 0;
                    document.getElementById('notes').value = data.notes || '';

                    modal.style.display = 'block';
                } else {
                    alert('Error loading watchlist item data');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error loading watchlist item data');
            }
        });
    });

    // Close modal
    function closeModalFunc() {
        modal.style.display = 'none';
    }

    closeModal?.addEventListener('click', closeModalFunc);
    cancelBtn?.addEventListener('click', closeModalFunc);

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            closeModalFunc();
        }
    });

    // Handle form submission
    document.getElementById('editWatchlistForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            list_id: document.getElementById('edit_list_id').value,
            watch_status: document.getElementById('watch_status').value,
            user_score: document.getElementById('user_score').value || null,
            episodes_watched: document.getElementById('episodes_watched').value,
            notes: document.getElementById('notes').value
        };

        try {
            const response = await fetch('/api/watchlist/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                alert('Watchlist updated successfully!');
                location.reload(); // Refresh to show updated data
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error updating watchlist');
        }
    });

    // Remove from watchlist
    document.querySelectorAll('.remove-watchlist-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            if (confirm('Are you sure you want to remove this anime from your watchlist?')) {
                const listId = btn.getAttribute('data-list-id');

                try {
                    const response = await fetch(`/api/watchlist/remove/${listId}`, {
                        method: 'DELETE'
                    });

                    const data = await response.json();

                    if (response.ok) {
                        alert('Removed from watchlist');
                        location.reload();
                    } else {
                        alert('Error: ' + data.error);
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error removing from watchlist');
                }
            }
        });
    });



    ///
/// RECOMMENDATION PAGE JAVASCRIPT
    ///

    // Refresh recommendations button
    document.getElementById('refreshBtn')?.addEventListener('click', async function () {
        const btn = this;
        btn.disabled = true;
        btn.textContent = '🔄 Refreshing...';

        try {
            const response = await fetch('/api/recommendations/refresh', {
                method: 'POST'
            });

            const data = await response.json();

            if (response.ok) {
                alert('Recommendations refreshed! Reloading page...');
                location.reload();
            } else {
                alert('Error: ' + data.error);
                btn.disabled = false;
                btn.textContent = '🔄 Refresh Recommendations';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error refreshing recommendations');
            btn.disabled = false;
            btn.textContent = '🔄 Refresh Recommendations';
        }
    });