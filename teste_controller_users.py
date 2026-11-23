from app.controllers.usuarios import UsuariosController

controller = UsuariosController()

# CREATE
print("\n--- CADASTRANDO ---")  

usuario = controller.cadastrar(
    "arthur lenda",
    "admin@bottle.com",
    "12356"
)

print("Cadastrado:", usuario.username)

# READ
print("\n--- LISTANDO ---")

usuarios = controller.listar()
for user in usuarios:
    print(user.username, user.email, user.senha)

# UPDATE
print("\n--- EDITANDO ---")
controller.editar("arthur-lenda", "admin@bottle.com", "123456")


#buscar
print("\n--- BUSCANDO ---")
encontrado = controller.buscar("arthur lenda")
if encontrado:
    print("Encontrado:", encontrado.username, encontrado.email, encontrado.senha)


""" #delete
print("\n--- DELETANDO ---")

controller.deletar("arthur lenda")   """


