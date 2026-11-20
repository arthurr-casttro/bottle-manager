
import json
import os

from app.models.bebidas import Bebida


class BebidasRecord:

  
    def __init__(self):
                diretorio_atual = os.path.dirname(os.path.abspath(__file__))

                pasta_db = os.path.abspath(
                    os.path.join(diretorio_atual, "..", "db")
                )

                os.makedirs(pasta_db, exist_ok=True)

                self.arquivo = os.path.join(pasta_db, "bebidas.json")

                if not os.path.exists(self.arquivo):
                    with open(self.arquivo, "w", encoding="utf-8") as arquivo:
                        json.dump([], arquivo)



    def listar(self):
        with open(self.arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        bebidas = []

        for item in dados:
            bebida = Bebida(
                item["id"],
                item["nome"],
                item["categoria"],
                item["preco"],
                item["quantidade"]
            )

            bebidas.append(bebida)

        return bebidas

    def salvar(self, bebidas):
        dados = []

        for bebida in bebidas:
            dados.append({
                "id": bebida.id,
                "nome": bebida.nome,
                "categoria": bebida.categoria,
                "preco": bebida.preco,
                "quantidade": bebida.quantidade
            })

        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )
