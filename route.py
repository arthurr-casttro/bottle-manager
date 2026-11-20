from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response

from app.controllers.application import Application
from app.controllers.bebidas import BebidasController



app = Bottle()
ctl = Application()

bebidas_ctl = BebidasController()   


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

@app.route('/dashboard')
def dashboard(info= None):
    return ctl.render('dashboard')

# Listar bebidas
@app.route('/bebidas')
def listar_bebidas():
    bebidas = bebidas_ctl.listar()

    return template(
        'app/views/html/bebidas',
        bebidas=bebidas,
        bebida=None
    )


# Cadastrar bebida
@app.route('/bebidas/cadastrar', method='POST')
def cadastrar_bebida():
    nome = request.forms.get('nome')
    categoria = request.forms.get('categoria')
    preco = request.forms.get('preco')
    quantidade = request.forms.get('quantidade')

    try:
        preco = float(preco)
        quantidade = int(quantidade)

        if preco < 0 or quantidade < 0:
            raise ValueError

        if not nome or not categoria:
            raise ValueError

        bebidas_ctl.cadastrar(
            nome,
            categoria,
            preco,
            quantidade
        )

        return redirect('/bebidas')

    except (ValueError, TypeError):
        return "Dados inválidos. Volte e confira o formulário."


# Abrir edição
@app.route('/bebidas/editar/<id:int>')
def abrir_edicao(id):
    bebida = bebidas_ctl.buscar(id)

    if bebida is None:
        return "Bebida não encontrada."

    bebidas = bebidas_ctl.listar()

    return template(
        'app/views/html/bebidas',
        bebidas=bebidas,
        bebida=bebida
    )


# Salvar edição
@app.route('/bebidas/editar/<id:int>', method='POST')
def editar_bebida(id):
    nome = request.forms.get('nome')
    categoria = request.forms.get('categoria')
    preco = request.forms.get('preco')
    quantidade = request.forms.get('quantidade')

    try:
        preco = float(preco)
        quantidade = int(quantidade)

        if preco < 0 or quantidade < 0:
            raise ValueError

        if not nome or not categoria:
            raise ValueError

        resultado = bebidas_ctl.editar(
            id,
            nome,
            categoria,
            preco,
            quantidade
        )

        if not resultado:
            return "Bebida não encontrada."

        return redirect('/bebidas')

    except (ValueError, TypeError):
        return "Dados inválidos. Volte e confira o formulário."


# Excluir bebida
@app.route('/bebidas/excluir/<id:int>', method='POST')
def excluir_bebida(id):
    bebidas_ctl.excluir(id)

    return redirect('/bebidas')

@app.route('/dashboard2')
def dashboard2():
    bebidas = bebidas_ctl.listar()
    estatisticas = bebidas_ctl.obter_estatisticas()

    return template(
        'app/views/html/dashboard2',
        bebidas=bebidas,
        estatisticas=estatisticas
    )


#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
