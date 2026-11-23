
document.addEventListener('DOMContentLoaded', () => {

    // Mostrar ou ocultar senha
    const passwordInput = document.getElementById('senha');
    const togglePassword = document.getElementById('togglePassword');

    if (passwordInput && togglePassword) {
        togglePassword.addEventListener('click', () => {

            const mostrando = passwordInput.type === 'text';

            passwordInput.type = mostrando ? 'password' : 'text';

            togglePassword.textContent = mostrando ? '◉' : '◎';

            togglePassword.setAttribute(
                'aria-label',
                mostrando ? 'Mostrar senha' : 'Ocultar senha'
            );
        });
    }

    // Feedback visual no envio
    const loginForm = document.getElementById('loginForm');
    const loginButton = document.getElementById('loginButton');

    if (loginForm && loginButton) {
        loginForm.addEventListener('submit', () => {

            loginButton.disabled = true;

            loginButton.querySelector('span:first-child').textContent =
                'Verificando acesso...';

            loginButton.querySelector('.button-arrow').textContent = '...';

        });
    }

});
