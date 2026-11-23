import json
import os

import app.models.usuarios as usuarios

class UsuariosRecord:   
    
    def __init__(self):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))

        pasta_db = os.path.abspath(
            os.path.join(diretorio_atual, "..", "db")
        )

        os.makedirs(pasta_db, exist_ok=True)

        self.arquivo = os.path.join(pasta_db, "usuarios.json")

        if not os.path.exists(self.arquivo):
            with open(self.arquivo, "w", encoding="utf-8") as arquivo:
                json.dump([], arquivo)

    def listar(self):
        with open(self.arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        usuarios_list = []

        for item in dados:
            usuario = usuarios.User(
                item["username"],
                item["email"],
                item["senha"]
            )

            usuarios_list.append(usuario)

        return usuarios_list

    def salvar(self, usuarios_list):
        dados = []

        for usuario in usuarios_list:
            dados.append({
                "username": usuario.username,
                "email": usuario.email,
                "senha": usuario.senha
            })

        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)