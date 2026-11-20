
from app.models.bebidas import Bebida
from app.controllers.bebidas_record import BebidasRecord


class BebidasController:

    def __init__(self):
        self.record = BebidasRecord()

    # READ: listar todas as bebidas
    def listar(self):
        return self.record.listar()

    # READ: buscar uma bebida pelo ID
    def buscar(self, id):
        bebidas = self.record.listar()

        for bebida in bebidas:
            if bebida.id == id:
                return bebida

        return None

    # CREATE: cadastrar uma nova bebida
    def cadastrar(self, nome, categoria, preco, quantidade):
        bebidas = self.record.listar()

        novo_id = max(
            [bebida.id for bebida in bebidas],
            default=0
        ) + 1

        nova_bebida = Bebida(
            novo_id,
            nome,
            categoria,
            preco,
            quantidade
        )

        bebidas.append(nova_bebida)

        self.record.salvar(bebidas)

        return nova_bebida

    # UPDATE: editar uma bebida existente
    def editar(self, id, nome, categoria, preco, quantidade):
        bebidas = self.record.listar()

        for bebida in bebidas:
            if bebida.id == id:
                bebida.nome = nome
                bebida.categoria = categoria
                bebida.preco = preco
                bebida.quantidade = quantidade

                self.record.salvar(bebidas)

                return True

        return False

    # DELETE: excluir uma bebida
    def excluir(self, id):
        bebidas = self.record.listar()

        for bebida in bebidas:
            if bebida.id == id:
                bebidas.remove(bebida)

                self.record.salvar(bebidas)

                return True

        return False
    

    def obter_estatisticas(self):
        bebidas = self.listar()

        total_produtos = len(bebidas)

        total_estoque = sum(
             bebida.quantidade for bebida in bebidas
         )

        estoque_baixo = sum(
            1 for bebida in bebidas
            if bebida.quantidade <= 5
        )

        return {
            "total_produtos": total_produtos,
            "total_estoque": total_estoque,
            "estoque_baixo": estoque_baixo
        }
