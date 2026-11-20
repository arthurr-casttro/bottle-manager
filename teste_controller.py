
from app.controllers.bebidas import BebidasController

controller = BebidasController()

# CREATE
print("\n--- CADASTRANDO ---")

bebida = controller.cadastrar(
    "Guaraná",
    "Refrigerante",
    7.50,
    40
)

print("Cadastrada:", bebida.nome)
print("ID:", bebida.id)

# READ
print("\n--- LISTANDO ---")

bebidas = controller.listar()

for item in bebidas:
    print(item.id, item.nome, item.preco, item.quantidade)

# UPDATE
print("\n--- EDITANDO ---")

resultado = controller.editar(
    bebida.id,
    "Guaraná Antárctica",
    "Refrigerante",
    8.00,
    45
)

print("Edição realizada:", resultado)

# READ
print("\n--- BUSCANDO ---")

encontrada = controller.buscar(bebida.id)

if encontrada:
    print("Encontrada:", encontrada.nome)

