document.addEventListener('DOMContentLoaded', function() {
    // Filter functionality
    const filterForm = document.getElementById('filterForm');
    const eventCards = document.querySelectorAll('.event-card');
    
    if(filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            filterEvents();
        });

        filterForm.addEventListener('reset', function() {
            eventCards.forEach(card => card.style.display = 'block');
        });
    }

    // Card click handling
    document.querySelectorAll('.event-card').forEach(card => {
        card.addEventListener('click', function(e) {
            if (!e.target.closest('a')) {
                window.open(this.querySelector('a').href, '_blank');
            }
        });
    });

    // Onboarding dismiss
    document.querySelectorAll('.dismiss-guide').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelector('.onboarding-steps')?.remove();
        });
    });
});

function filterEvents() {
    const artistFilter = document.getElementById('artistFilter').value.toLowerCase();
    const dateFilter = document.getElementById('dateFilter').value;
    const locationFilter = document.getElementById('locationFilter').value.toLowerCase();

    document.querySelectorAll('.event-card').forEach(card => {
        const artist = card.dataset.artist.toLowerCase();
        const date = card.dataset.date;
        const location = card.dataset.location.toLowerCase();

        const artistMatch = !artistFilter || artist.includes(artistFilter);
        const dateMatch = !dateFilter || date === dateFilter;
        const locationMatch = !locationFilter || location.includes(locationFilter);

        card.style.display = (artistMatch && dateMatch && locationMatch) ? 'block' : 'none';
    });
}