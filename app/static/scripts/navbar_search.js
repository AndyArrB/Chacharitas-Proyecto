document.addEventListener('DOMContentLoaded', function() {
    const search = document.getElementById('search');
    search.addEventListener('keyup', function() {
        const value = this.value.toLowerCase();
        const tableNames = document.querySelectorAll('.table_name');
        tableNames.forEach(function(table) {
            const text = table.textContent.toLowerCase();
            const link = table.querySelector('a');
            if (text.indexOf(value) > -1) {
                table.style.opacity = '1';
                table.style.pointerEvents = 'auto';
                link.classList.remove('disabled');
            } else {
                table.style.opacity = '0.2';
                table.style.pointerEvents = 'none';
                link.classList.add('disabled');
            }
        });
    });
});

