
const modal = document.getElementById('userModal');
const form = document.getElementById('userForm');

const newUserButton = document.getElementById('newUser');
const closeButton = document.getElementById('closeModal');
const cancelButton = document.getElementById('cancelModal');

const modalTitle = document.getElementById('modalTitle');
const modalDescription = document.getElementById('modalDescription');
const submitButton = document.getElementById('submitButton');
const passwordHint = document.getElementById('passwordHint');

const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('senha');

const searchInput = document.getElementById('userSearch');
const emptySearch = document.getElementById('emptySearch');


// ==========================================
// ABRIR MODAL PARA CADASTRO
// ==========================================

newUserButton.addEventListener('click', () => {
    form.reset();

    form.action = '/usuarios/cadastrar';

    usernameInput.readOnly = false;
    usernameInput.required = true;

    passwordInput.required = true;
    passwordInput.placeholder = 'Digite uma senha';

    modalTitle.textContent = 'Novo usuário';
    modalDescription.textContent = 'Preencha os dados da conta de acesso.';
    submitButton.textContent = 'Cadastrar usuário';
    passwordHint.textContent = 'A senha será armazenada com hash.';

    modal.showModal();
});


// ==========================================
// ABRIR MODAL PARA EDIÇÃO
// ==========================================

document.querySelectorAll('.edit-button').forEach(button => {
    button.addEventListener('click', () => {
        const username = button.dataset.username;
        const email = button.dataset.email;

        form.action = `/usuarios/editar/${encodeURIComponent(username)}`;

        usernameInput.value = username;
        usernameInput.readOnly = true;

        emailInput.value = email;

        // A edição exige uma nova senha.
        passwordInput.value = '';
        passwordInput.required = true;
        passwordInput.placeholder = 'Digite a nova senha';

        modalTitle.textContent = 'Editar usuário';
        modalDescription.textContent = 'Atualize o e-mail e a senha da conta.';
        submitButton.textContent = 'Salvar alterações';
        passwordHint.textContent = 'Informe uma nova senha para atualizar a conta.';

        modal.showModal();
    });
});


// ==========================================
// FECHAR MODAL
// ==========================================

function fecharModal() {
    modal.close();
}

closeButton.addEventListener('click', fecharModal);
cancelButton.addEventListener('click', fecharModal);


// ==========================================
// PESQUISA NA TABELA
// ==========================================

searchInput.addEventListener('input', () => {
    const termo = searchInput.value.toLowerCase().trim();

    const linhas = document.querySelectorAll('.user-row');

    let encontrados = 0;

    linhas.forEach(linha => {
        const nome = linha.querySelector('.user-name').textContent.toLowerCase();
        const email = linha.querySelector('.user-email').textContent.toLowerCase();

        const corresponde =
            nome.includes(termo) ||
            email.includes(termo);

        linha.hidden = !corresponde;

        if (corresponde) {
            encontrados++;
        }
    });

    emptySearch.hidden = encontrados > 0 || linhas.length === 0;
});


// ==========================================
// CONFIRMAÇÃO DE EXCLUSÃO
// ==========================================

document.querySelectorAll('.delete-form').forEach(formExcluir => {
    formExcluir.addEventListener('submit', event => {
        const confirmar = window.confirm(
            'Tem certeza que deseja excluir este usuário?'
        );

        if (!confirmar) {
            event.preventDefault();
        }
    });
});
