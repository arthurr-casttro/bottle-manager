
document.addEventListener('DOMContentLoaded', () => {
    const appShell = document.getElementById('appShell');
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

    const productSearch = document.getElementById('productSearch');
    const productGrid = document.getElementById('productGrid');
    const emptyState = document.getElementById('emptyState');

    const currentDate = document.getElementById('currentDate');

    // Exibe a data atual
    if (currentDate) {
        currentDate.textContent = new Intl.DateTimeFormat('pt-BR', {
            day: '2-digit',
            month: 'long',
            year: 'numeric'
        }).format(new Date());
    }

    // Alterna a sidebar
    sidebarToggle.addEventListener('click', () => {
        if (window.innerWidth <= 800) {
            sidebar.classList.toggle('mobile-open');
        } else {
            appShell.classList.toggle('sidebar-collapsed');
        }
    });

    // Fecha a sidebar mobile ao clicar em um link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            document.querySelectorAll('.nav-link').forEach(item => {
                item.classList.remove('active');
            });

            link.classList.add('active');
            sidebar.classList.remove('mobile-open');
        });
    });

    // Pesquisa de produtos
    productSearch.addEventListener('input', () => {
        const searchTerm = productSearch.value
            .toLowerCase()
            .trim();

        const products = productGrid.querySelectorAll('.product-card');

        let visibleProducts = 0;

        products.forEach(product => {
            const productName = product.dataset.name.toLowerCase();

            const matches = productName.includes(searchTerm);

            product.hidden = !matches;

            if (matches) {
                visibleProducts++;
            }
        });

        emptyState.hidden = visibleProducts > 0;
    });

    // Garante que a sidebar não fique presa aberta ao redimensionar
    window.addEventListener('resize', () => {
        if (window.innerWidth > 800) {
            sidebar.classList.remove('mobile-open');
        }
    });
});
