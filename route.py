
import os

from bottle import (
    Bottle,
    run,
    request,
    static_file,
    redirect,
    template
)

from beaker.middleware import SessionMiddleware

from app.controllers.application import Application
from app.controllers.bebidas import BebidasController
from app.controllers.usuarios import UsuariosController


# ==========================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ==========================================

app = Bottle()

ctl = Application()
bebidas_ctl = BebidasController()
usuarios_ctl = UsuariosController()


# ==========================================
# SESSÃO E AUTENTICAÇÃO
# ==========================================

def obter_sessao():
    return request.environ.get('beaker.session')


def usuario_autenticado():
    session = obter_sessao()

    if session is None:
        return False

    return bool(session.get('usuario'))


def proteger_rota():
    if not usuario_autenticado():
        return redirect('/login')

    return None


# ==========================================
# ARQUIVOS ESTÁTICOS
# ==========================================

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')


# ==========================================
# LOGIN
# ==========================================

@app.route('/login', method='GET')
def login_page():
    if usuario_autenticado():
        return redirect('/dashboard2')

    return template(
        'app/views/html/login',
        erro=None
    )


@app.route('/login', method='POST')
def login():
    email = request.forms.get('email', '').strip()
    senha = request.forms.get('senha', '')

    usuario = usuarios_ctl.login(email, senha)

    if usuario is None:
        return template(
            'app/views/html/login',
            erro='E-mail ou senha inválidos.'
        )

    session = obter_sessao()

    if session is None:
        return template(
            'app/views/html/login',
            erro='Não foi possível iniciar sua sessão.'
        )

    session['usuario'] = usuario.username
    session.save()

    print('LOGIN REALIZADO:', usuario.username)
    print('SESSÃO SALVA:', dict(session))

    return redirect('/dashboard2')


# ==========================================
# LOGOUT
# ==========================================

@app.route('/logout')
def logout():
    session = obter_sessao()

    if session is not None:
        session.delete()

    return redirect('/login')


# ==========================================
# PÁGINAS
# ==========================================

@app.route('/helper')
def helper():
    return ctl.render('helper')


@app.route('/dashboard')
def dashboard():
    bloqueio = proteger_rota()

    if bloqueio:
        return bloqueio

    return ctl.render('dashboard')


@app.route('/dashboard2')
def dashboard2():
    bloqueio = proteger_rota()

    if bloqueio:
        return bloqueio

    bebidas = bebidas_ctl.listar()
    estatisticas = bebidas_ctl.obter_estatisticas()

    return template(
        'app/views/html/dashboard2',
        bebidas=bebidas,
        estatisticas=estatisticas
    )


# ==========================================
# CRUD DE BEBIDAS
# ==========================================

@app.route('/bebidas')
def listar_bebidas():
    bloqueio = proteger_rota()

    if bloqueio:
        return bloqueio

    bebidas = bebidas_ctl.listar()

    return template(
        'app/views/html/bebidas',
        bebidas=bebidas
    )


@app.route('/bebidas/cadastrar', method='POST')
def cadastrar_bebida():
    bloqueio = proteger_rota()

    if bloqueio:
        return bloqueio

    nome = request.forms.get('nome', '').strip()
    categoria = request.forms.get('categoria', '').strip()

    try:
        preco = float(request.forms.get('preco', '0'))
        quantidade = int(request.forms.get('quantidade', '0'))

        if not nome or not categoria:
            raise ValueError

        if preco < 0 or quantidade < 0:
            raise ValueError

    except (ValueError, TypeError):
        return redirect('/bebidas')

    bebidas_ctl.cadastrar(
        nome,
        categoria,
        preco,
        quantidade
    )

    return redirect('/bebidas')


@app.route('/bebidas/editar/<id:int>', method='GET')
def pagina_editar_bebida(id):
    bloqueio = proteger_rota()

    if bloqueio:
        return bloqueio

    bebida = bebidas_ctl.buscar(id)

    if bebida is None:
        return redirect('/bebidas')

    return template(
        'app/views/html/editar_bebida',
        bebida=bebida
    )


@app.route('/bebidas/editar/<id:int>', method='POST')
def editar_bebida(id):
    bloqueio = proteger_rota()

    if bloqueio:
        return bloqueio

    nome = request.forms.get('nome', '').strip()
    categoria = request.forms.get('categoria', '').strip()

    try:
        preco = float(request.forms.get('preco', '0'))
        quantidade = int(request.forms.get('quantidade', '0'))

        if not nome or not categoria:
            raise ValueError

        if preco < 0 or quantidade < 0:
            raise ValueError

    except (ValueError, TypeError):
        return redirect('/bebidas')

    bebidas_ctl.editar(
        id,
        nome,
        categoria,
        preco,
        quantidade
    )

    return redirect('/bebidas')


@app.route('/bebidas/excluir/<id:int>', method='POST')
def excluir_bebida(id):
    bloqueio = proteger_rota()

    if bloqueio:
        return bloqueio

    bebidas_ctl.excluir(id)

    return redirect('/bebidas')


# ==========================================
# CRUD DE USUÁRIOS
# ==========================================

@app.route('/usuarios')
def listar_usuarios():
    bloqueio = proteger_rota()

    if bloqueio:
        return bloqueio

    usuarios = usuarios_ctl.listar()

    return template(
        'app/views/html/usuarios',
        usuarios=usuarios
    )


@app.route('/usuarios/cadastrar', method='POST')
def cadastrar_usuario():
    bloqueio = proteger_rota()

    if bloqueio:
        return bloqueio

    username = request.forms.get('username', '').strip()
    email = request.forms.get('email', '').strip()
    senha = request.forms.get('senha', '')

    if not username or not email or len(senha) < 6:
        return redirect('/usuarios')

    usuarios = usuarios_ctl.listar()

    # Verifica se o nome de usuário já existe.
    if any(
        usuario.username.lower() == username.lower()
        for usuario in usuarios
    ):
        return redirect('/usuarios')

    # Verifica se o e-mail já está cadastrado.
    if any(
        usuario.email.strip().lower() == email.lower()
        for usuario in usuarios
    ):
        return redirect('/usuarios')

    usuarios_ctl.cadastrar(
        username,
        email,
        senha
    )

    return redirect('/usuarios')


@app.route('/usuarios/editar/<username>', method='POST')
def editar_usuario(username):
    bloqueio = proteger_rota()

    if bloqueio:
        return bloqueio

    email = request.forms.get('email', '').strip()
    senha = request.forms.get('senha', '')

    if not email or len(senha) < 6:
        return redirect('/usuarios')

    usuario_atual = usuarios_ctl.buscar(username)

    if usuario_atual is None:
        return redirect('/usuarios')

    usuarios = usuarios_ctl.listar()

    # Impede que dois usuários tenham o mesmo e-mail.
    if any(
        usuario.email.strip().lower() == email.lower()
        and usuario.username != username
        for usuario in usuarios
    ):
        return redirect('/usuarios')

    usuarios_ctl.editar(
        username,
        email,
        senha
    )

    return redirect('/usuarios')


@app.route('/usuarios/excluir/<username>', method='POST')
def excluir_usuario(username):
    bloqueio = proteger_rota()

    if bloqueio:
        return bloqueio

    session = obter_sessao()
    usuario_logado = session.get('usuario') if session else None

    # Impede que o usuário exclua a própria conta.
    if username == usuario_logado:
        return redirect('/usuarios')

    usuarios_ctl.deletar(username)

    return redirect('/usuarios')



# ==========================================
# INICIALIZAÇÃO DO SERVIDOR COM BEAKER
# ==========================================

if __name__ == '__main__':

    pasta_sessoes = os.path.abspath('./app/sessions')
    os.makedirs(pasta_sessoes, exist_ok=True)

    session_opts = {
        'session.type': 'file',
        'session.data_dir': pasta_sessoes,

        'session.auto': True,
        'session.timeout': 3600,

        'session.key': 'bottlemanager_session',
        'session.secret': 'bottle-manager-chave-local-2026',

        'session.cookie_expires': 3600,
        'session.cookie_path': '/',
        'session.cookie_httponly': True,
        'session.cookie_secure': False,

        'session.invalidate_corrupt': True
    }

    app_com_sessao = SessionMiddleware(
        app,
        session_opts
    )

    print('Bottle Manager iniciado!')
    print('Acesse: http://127.0.0.1:8080/login')

    run(
        app_com_sessao,
        host='127.0.0.1',
        port=8080,
        debug=True,
        reloader=False
    )
