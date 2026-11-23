
import hashlib
import secrets
import hmac

from app.models.usuarios import User
from app.controllers.usuarios_record import UsuariosRecord


class UsuariosController:

    def __init__(self):
        self.record = UsuariosRecord()

    def gerar_hash(self, senha):
        salt = secrets.token_hex(16)

        hash_senha = hashlib.pbkdf2_hmac(
            'sha256',
            senha.encode('utf-8'),
            salt.encode('utf-8'),
            200000
        ).hex()

        return f"{salt}${hash_senha}"

    def verificar_senha(self, senha, senha_armazenada):
        try:
            salt, hash_original = senha_armazenada.split('$')

            hash_digitado = hashlib.pbkdf2_hmac(
                'sha256',
                senha.encode('utf-8'),
                salt.encode('utf-8'),
                200000
            ).hex()

            return hmac.compare_digest(hash_original, hash_digitado)

        except ValueError:
            return False

    def listar(self):
        return self.record.listar()

    def cadastrar(self, username, email, senha):
        usuarios_list = self.record.listar()

        senha_hash = self.gerar_hash(senha)

        novo_usuario = User(
            username,
            email,
            senha_hash
        )

        usuarios_list.append(novo_usuario)
        self.record.salvar(usuarios_list)

        return novo_usuario

    def buscar(self, username):
        usuarios_list = self.record.listar()

        for usuario in usuarios_list:
            if usuario.username == username:
                return usuario

        return None

    def login(self, email, senha):
        usuarios_list = self.record.listar()

        for usuario in usuarios_list:
            if usuario.email == email:
                if self.verificar_senha(senha, usuario.senha):
                    return usuario

        return None

    def editar(self, username, novo_email, novo_senha):
        usuarios_list = self.record.listar()

        for usuario in usuarios_list:
            if usuario.username == username:
                usuario.email = novo_email
                usuario.senha = self.gerar_hash(novo_senha)

                self.record.salvar(usuarios_list)

                return usuario

        return None

    def deletar(self, username):
        usuarios_list = self.record.listar()

        for usuario in usuarios_list:
            if usuario.username == username:
                usuarios_list.remove(usuario)
                self.record.salvar(usuarios_list)
                return True

        return False
