
from app.models.bebidas import Bebida
from app.controllers.bebidas_record import BebidasRecord

record = BebidasRecord()

# Criando bebidas
bebida1 = Bebida(1, "Coca-Cola", "Refrigerante", 8.00, 30)
bebida2 = Bebida(2, "Água Mineral", "Água", 4.00, 50)

# Salvando no JSON
record.salvar([bebida1, bebida2])

print("Bebidas salvas!")

# Lendo os dados do JSON
bebidas = record.listar()

for bebida in bebidas:
    print(bebida.nome, bebida.preco, bebida.quantidade)
