document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const dictionaryContent = document.querySelector('.dictionary-content');
    let originalContent = dictionaryContent.innerHTML;
    
    // Create overlay element
    const overlay = document.createElement('div');
    overlay.className = 'video-overlay';
    document.body.appendChild(overlay);
    
    // Function to normalize Arabic text
    function normalizeArabic(text) {
        if (!text) return '';
        return text
            .normalize('NFKD')
            .replace(/[\u064B-\u065F\u0670]/g, '') // Remove diacritics
            .replace(/[إأآ]/g, 'ا') // Normalize Alef variations
            .replace(/ى/g, 'ي') // Normalize Ya variations
            .replace(/ة/g, 'ه'); // Normalize Ta Marbuta
    }
    
    // Function to handle video scaling
    function handleVideoScaling() {
        const videoCards = document.querySelectorAll('.video-card');
        
        videoCards.forEach(card => {
            // Remove existing click event listeners
            const newCard = card.cloneNode(true);
            card.parentNode.replaceChild(newCard, card);
            
            newCard.addEventListener('click', function(e) {
                e.stopPropagation();
                
                if (this.classList.contains('active')) {
                    this.classList.remove('active');
                    overlay.classList.remove('active');
                } else {
                    // Remove active class from all cards
                    videoCards.forEach(c => c.classList.remove('active'));
                    // Add active class to clicked card
                    this.classList.add('active');
                    overlay.classList.add('active');
                }
            });
        });
    }
    
    // Close video when clicking overlay
    overlay.addEventListener('click', function() {
        const activeCards = document.querySelectorAll('.video-card.active');
        activeCards.forEach(card => card.classList.remove('active'));
        this.classList.remove('active');
    });
    
    // Initialize video scaling
    handleVideoScaling();
    
    // Handle search functionality
    searchInput.addEventListener('input', function() {
        const filter = this.value.trim();
        const normalizedFilter = normalizeArabic(filter).toLowerCase();
        
        // If search is empty, restore original content
        if (filter === '') {
            dictionaryContent.innerHTML = originalContent;
            handleVideoScaling();
            return;
        }
        
        const videoCards = document.querySelectorAll('.video-card');
        let visibleCount = 0;
        let resultsHTML = '<div class="videos-grid">';
        
        videoCards.forEach(function(card) {
            const title = card.querySelector('.video-title').textContent;
            const normalizedTitle = normalizeArabic(title).toLowerCase();
            
            if (normalizedTitle.includes(normalizedFilter)) {
                resultsHTML += card.outerHTML;
                visibleCount++;
            }
        });
        
        resultsHTML += '</div>';
        
        if (visibleCount === 0) {
            dictionaryContent.innerHTML = '<div class="no-results">No results found</div>';
        } else {
            dictionaryContent.innerHTML = resultsHTML;
            handleVideoScaling();
        }
    });
}); 