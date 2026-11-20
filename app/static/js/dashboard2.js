
document.addEventListener('DOMContentLoaded', () => {
    // Data atual
    const currentDate = document.getElementById('currentDate');

    if (currentDate) {
        currentDate.textContent = new Date().toLocaleDateString('pt-BR', {
            weekday: 'long',
            day: '2-digit',
            month: 'long',
            year: 'numeric'
        });
    }

    // Menu lateral
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // Pesquisa de produtos
    const searchInput = document.getElementById('productSearch');
    const productGrid = document.getElementById('productGrid');
    const emptyState = document.getElementById('emptyState');

    if (searchInput && productGrid) {
        const products = productGrid.querySelectorAll('.product-card');

        searchInput.addEventListener('input', () => {
            const search = searchInput.value
                .toLowerCase()
                .trim();

            let visibleProducts = 0;

            products.forEach(product => {
                const name = product.dataset.name || '';
                const visible = name.includes(search);

                product.style.display = visible ? '' : 'none';

                if (visible) {
                    visibleProducts++;
                }
            });

            if (emptyState) {
                emptyState.hidden = visibleProducts > 0;
            }
        });
    }
});
