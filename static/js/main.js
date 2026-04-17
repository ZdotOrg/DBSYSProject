// ============================================================
// ANIME TRACKER - MAIN JAVASCRIPT
// ============================================================

console.log('=== main.js loaded ===');

document.addEventListener('DOMContentLoaded', function() {
    console.log('=== DOM ready ===');
    
    // Initialize based on what page we're on
    initializeWatchlistButton();
    initializeWatchlistPage();
    initializeSearchPage();
    initializeRecommendationsPage();
});

// ============================================================
// ANIME DETAIL PAGE - WATCHLIST BUTTON
// ============================================================

function initializeWatchlistButton() {
    const watchlistBtn = document.getElementById('addToWatchlistBtn');
    if (!watchlistBtn) return;
    
    const animeId = watchlistBtn.dataset.animeId;
    console.log('Watchlist button found for anime ID:', animeId);
    
    // Check if animeId is valid
    if (!animeId || animeId === '') {
        console.error('ERROR: animeId is empty! Check data-anime-id attribute.');
        watchlistBtn.disabled = true;
        watchlistBtn.innerHTML = 'Error: No Anime ID';
        return;
    }
    
    checkWatchlistStatus(animeId, watchlistBtn);
    
    watchlistBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        await handleAddToWatchlist(animeId, watchlistBtn);
    });
}

async function checkWatchlistStatus(animeId, button) {
    try {
        const response = await fetch(`/watchlist/status/${animeId}`);
        
        if (response.status === 401) {
            console.log('User not logged in');
            return;
        }
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Watchlist status:', data);
        
        if (data.in_watchlist) {
            updateButtonToAddedState(button, data.status, animeId);
        }
    } catch (error) {
        console.error('Error checking watchlist status:', error);
    }
}

async function handleAddToWatchlist(animeId, button) {
    const originalHTML = button.innerHTML;
    
    console.log('Adding to watchlist - animeId:', animeId);
    
    button.disabled = true;
    button.innerHTML = '<span class="spinner"></span> Processing...';
    
    try {
        const response = await fetch('/watchlist/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                anime_id: parseInt(animeId),
                status: 'Plan to Watch'
            })
        });
        
        console.log('Response status:', response.status);
        
        const data = await response.json();
        console.log('Response data:', data);
        
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/auth/login';
                return;
            }
            throw new Error(data.error || `HTTP ${response.status}`);
        }
        
        if (data.success) {
            updateButtonToAddedState(button, 'Plan to Watch', animeId);
            showNotification('Added to watchlist!', 'success');
        } else {
            throw new Error(data.error || 'Failed to add');
        }
    } catch (error) {
        console.error('Error adding to watchlist:', error);
        button.disabled = false;
        button.innerHTML = originalHTML;
        showNotification(error.message, 'error');
    }
}

function updateButtonToAddedState(button, status, animeId) {
    button.classList.add('added');
    button.innerHTML = `
        <svg class="watchlist-icon" viewBox="0 0 24 24" width="18" height="18">
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" fill="currentColor"/>
        </svg>
        In Watchlist (${status})
    `;
    button.disabled = false;
    
    // Replace click handler
    const newButton = button.cloneNode(true);
    button.parentNode.replaceChild(newButton, button);
    
    newButton.addEventListener('click', async (e) => {
        e.preventDefault();
        if (confirm('Remove from watchlist?')) {
            await removeAnimeFromWatchlist(animeId, newButton);
        }
    });
}

async function removeAnimeFromWatchlist(animeId, button) {
    const originalHTML = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<span class="spinner"></span> Removing...';
    
    try {
        const response = await fetch('/watchlist/remove-by-anime', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ anime_id: parseInt(animeId) })
        });
        
        const data = await response.json();
        
        if (data.success) {
            button.classList.remove('added');
            button.innerHTML = `
                <svg class="watchlist-icon" viewBox="0 0 24 24" width="18" height="18">
                    <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" fill="currentColor"/>
                </svg>
                Add to Watchlist
            `;
            button.disabled = false;
            
            // Reset click handler
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);
            initializeWatchlistButton();
            
            showNotification('Removed from watchlist', 'success');
        } else {
            throw new Error(data.error || 'Failed to remove');
        }
    } catch (error) {
        console.error('Error removing:', error);
        button.disabled = false;
        button.innerHTML = originalHTML;
        showNotification(error.message, 'error');
    }
}

// ============================================================
// WATCHLIST PAGE
// ============================================================

function initializeWatchlistPage() {
    const modal = document.getElementById('editModal');
    if (!modal) return; // Not on watchlist page
    
    console.log('Initializing watchlist page');
    
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            button.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Edit modal
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.cancel-btn');
    
    document.querySelectorAll('.edit-watchlist-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const listId = btn.getAttribute('data-list-id');
            try {
                const response = await fetch(`/watchlist/item/${listId}`);
                const data = await response.json();
                
                if (response.ok) {
                    document.getElementById('edit_list_id').value = data.list_id;
                    document.getElementById('watch_status').value = data.watch_status;
                    document.getElementById('user_score').value = data.user_score || '';
                    document.getElementById('episodes_watched').value = data.episodes_watched || 0;
                    document.getElementById('notes').value = data.notes || '';
                    modal.style.display = 'block';
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error loading watchlist item');
            }
        });
    });
    
    function closeModalFunc() {
        modal.style.display = 'none';
    }
    
    closeModal?.addEventListener('click', closeModalFunc);
    cancelBtn?.addEventListener('click', closeModalFunc);
    window.addEventListener('click', (e) => { if (e.target === modal) closeModalFunc(); });
    
    // Form submission
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
            const response = await fetch('/watchlist/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            if (response.ok) {
                alert('Watchlist updated!');
                location.reload();
            } else {
                const data = await response.json();
                alert('Error: ' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error updating watchlist');
        }
    });
    
    // Remove buttons
    document.querySelectorAll('.remove-watchlist-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            if (!confirm('Remove this anime from your watchlist?')) return;
            
            const listId = btn.getAttribute('data-list-id');
            try {
                const response = await fetch(`/watchlist/remove/${listId}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    alert('Removed from watchlist');
                    location.reload();
                } else {
                    const data = await response.json();
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error removing from watchlist');
            }
        });
    });
}

// ============================================================
// SEARCH PAGE - JIKAN INTEGRATION
// ============================================================

function initializeSearchPage() {
    const jikanSection = document.getElementById('jikanSection');
    if (!jikanSection) return; // Not on search page
    
    const jikanResults = document.getElementById('jikanResults');
    const searchQuery = document.querySelector('input[name="q"]')?.value;
    
    if (!searchQuery || searchQuery.length < 2) {
        jikanSection.style.display = 'none';
        return;
    }
    
    console.log('Initializing Jikan search for:', searchQuery);
    
    async function fetchJikanResults() {
        try {
            const response = await fetch(`/api/jikan/search?q=${encodeURIComponent(searchQuery)}&limit=12`);
            const data = await response.json();
            
            if (data.success && data.results) {
                displayJikanResults(data.results);
            } else {
                jikanResults.innerHTML = '<div class="jikan-loading">No results found on MyAnimeList</div>';
            }
        } catch (error) {
            console.error('Jikan error:', error);
            jikanResults.innerHTML = '<div class="jikan-error">Failed to search MyAnimeList</div>';
        }
    }
    
    function displayJikanResults(results) {
        let html = '<div class="jikan-grid">';
        
        results.forEach(anime => {
            const inDatabase = anime.in_database;
            const imageUrl = anime.image_url || '';
            const title = anime.title || 'Unknown';
            
            html += `
                <div class="jikan-card">
                    <div class="jikan-card-image">
                        ${imageUrl ? `<img src="${imageUrl}" alt="${title}">` : '<div class="no-image">No Image</div>'}
                        ${inDatabase ? '<span class="in-db-badge">✓ In Database</span>' : ''}
                    </div>
                    <div class="jikan-card-info">
                        <div class="jikan-card-title">${title}</div>
                        <div class="jikan-card-meta">
                            <span>${anime.type || 'Unknown'}</span>
                            <span>${anime.episodes || '?'} eps</span>
                            ${anime.score ? `<span class="jikan-card-score">⭐ ${anime.score}</span>` : ''}
                        </div>
                        <div class="jikan-card-actions">
                            ${inDatabase ? 
                                `<button class="view-in-db-btn" onclick="window.viewInDatabase(${anime.mal_id})">View</button>` :
                                `<button class="import-btn" onclick="window.importAnime(${anime.mal_id}, this)">📥 Import</button>`
                            }
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        jikanResults.innerHTML = html;
    }
    
    window.importAnime = async function(malId, button) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner"></span> Importing...';
        
        try {
            const response = await fetch('/api/jikan/import', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mal_id: malId })
            });
            
            const data = await response.json();
            
            if (data.success) {
                button.innerHTML = '✓ Imported!';
                button.style.background = '#2ecc71';
                setTimeout(() => location.reload(), 1000);
            } else {
                alert('Import failed: ' + (data.message || 'Unknown error'));
                button.disabled = false;
                button.innerHTML = '📥 Import';
            }
        } catch (error) {
            alert('Failed to import');
            button.disabled = false;
            button.innerHTML = '📥 Import';
        }
    };
    
    window.viewInDatabase = function(malId) {
        fetch(`/api/jikan/check/${malId}`)
            .then(r => r.json())
            .then(data => {
                if (data.anime_id) {
                    window.location.href = `/anime/${data.anime_id}`;
                }
            });
    };
    
    fetchJikanResults();
}

// ============================================================
// RECOMMENDATIONS PAGE
// ============================================================

function initializeRecommendationsPage() {
    const refreshBtn = document.getElementById('refreshBtn');
    if (!refreshBtn) return;
    
    refreshBtn.addEventListener('click', async function() {
        this.disabled = true;
        this.textContent = '🔄 Refreshing...';
        
        try {
            const response = await fetch('/api/recommendations/refresh', { method: 'POST' });
            
            if (response.ok) {
                alert('Recommendations refreshed!');
                location.reload();
            } else {
                const data = await response.json();
                alert('Error: ' + data.error);
                this.disabled = false;
                this.textContent = '🔄 Refresh Recommendations';
            }
        } catch (error) {
            alert('Error refreshing recommendations');
            this.disabled = false;
            this.textContent = '🔄 Refresh Recommendations';
        }
    });
}

document.getElementById('refreshBtn')?.addEventListener('click', async function() {
    this.textContent = '🔄 Refreshing...';
    this.disabled = true;
    
    try {
        const response = await fetch('/api/recommendations/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            location.reload();
        } else {
            alert('Failed to refresh: ' + data.error);
            this.textContent = '🔄 Refresh';
            this.disabled = false;
        }
    } catch (error) {
        alert('Error refreshing recommendations');
        this.textContent = '🔄 Refresh';
        this.disabled = false;
    }
});

// ============================================================
// NOTIFICATION SYSTEM
// ============================================================

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    if (!document.getElementById('notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                z-index: 10000;
                animation: slideIn 0.3s ease;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }
            .notification-success { background-color: #2ecc71; }
            .notification-error { background-color: #e74c3c; }
            .notification-info { background-color: #3498db; }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            .spinner {
                display: inline-block;
                width: 16px;
                height: 16px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                border-top-color: #fff;
                animation: spin 0.6s linear infinite;
                margin-right: 8px;
            }
            @keyframes spin { to { transform: rotate(360deg); } }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}