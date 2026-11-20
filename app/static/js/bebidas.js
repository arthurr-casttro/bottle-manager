
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('beverageModal');
    const form = document.getElementById('beverageForm');

    const modalTitle = document.getElementById('modalTitle');
    const modalDescription = document.getElementById('modalDescription');
    const submitButton = document.getElementById('submitButton');

    const searchInput = document.getElementById('productSearch');
    const rows = document.querySelectorAll('.product-row');
    const emptySearch = document.getElementById('emptySearch');

    function openCreateModal() {
        form.reset();
        form.action = '/bebidas/cadastrar';

        modalTitle.textContent = 'Nova bebida';
        modalDescription.textContent = 'Preencha os dados do produto.';
        submitButton.textContent = 'Cadastrar bebida';

        modal.showModal();
    }

    function openEditModal(button) {
        form.reset();

        const { id, nome, categoria, preco, quantidade } = button.dataset;

        form.action = `/bebidas/editar/${id}`;

        form.elements.nome.value = nome;
        form.elements.categoria.value = categoria;
        form.elements.preco.value = preco;
        form.elements.quantidade.value = quantidade;

        modalTitle.textContent = 'Editar bebida';
        modalDescription.textContent = 'Atualize as informações do produto.';
        submitButton.textContent = 'Salvar alterações';

        modal.showModal();
    }

    function closeModal() {
        modal.close();
    }

    document.getElementById('newBeverage')
        .addEventListener('click', openCreateModal);

    document.getElementById('closeModal')
        .addEventListener('click', closeModal);

    document.getElementById('cancelModal')
        .addEventListener('click', closeModal);

    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', () => openEditModal(button));
    });

    // Pesquisa local na tabela
    searchInput.addEventListener('input', () => {
        const term = searchInput.value.toLowerCase().trim();
        let visible = 0;

        rows.forEach(row => {
            const name = row.querySelector('.product-name')
                .textContent.toLowerCase();

            const category = row.querySelector('.product-category')
                .textContent.toLowerCase();

            const matches = name.includes(term) || category.includes(term);

            row.hidden = !matches;

            if (matches) visible++;
        });

        emptySearch.hidden = visible > 0 || term === '';
    });

    // Confirma exclusão antes de enviar o formulário
    document.querySelectorAll('.delete-form').forEach(form => {
        form.addEventListener('submit', event => {
            if (!confirm('Deseja realmente excluir esta bebida?')) {
                event.preventDefault();
            }
        });
    });
});
