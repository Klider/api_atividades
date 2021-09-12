from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy.sql.expression import delete
from werkzeug.wrappers import response
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

"""
USUARIOS = {
    'Klider':'123',
    'Gabriel': '123',
    'Daniel': '123'
}

@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return USUARIOS.get(login) == senha
"""
@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()

class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status': "Error",
                'message': "Pessoa não cadastrada"
            }
        return response

    def put(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            dados = request.json
            if 'nome' in dados:
                pessoa.nome = dados['nome']
                pessoa.save()
            if 'idade' in dados:
                pessoa.idade = dados['idade']
                pessoa.save()
            response = {
                'id':pessoa.id,
                'nome':pessoa.nome,
                'idade':pessoa.idade
            }
        except AttributeError:
            response = {
                'status': "Error",
                'message': "Pessoa não cadastrada"
            }
        return response

    def delete(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            pessoa.delete()
            response = {
                'status': "Sucesso",
                'message': "A Pessoa {} foi excluida com sucesso".format(nome)
            }
        except AttributeError:
            response = {
                'status': "Error",
                'message': "Pessoa não cadastrada"
            }
        return response

class Pessoas2(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [
            {
                'id': i.id,
                'nome': i.nome,
                'idade': i.idade
            }
            for i in pessoas
        ]
        return response

    def post(self):
        dados = request.json
        if 'nome' and 'idade' in dados:
            nome = dados['nome']
            idade = dados['idade']
            pessoateste = Pessoas.query.filter_by(nome=nome).first()
            try:
                response = {
                    'status': "Error",
                    'message': "A pessoa {} já está cadastrada".format(pessoateste.nome)
                }
            except AttributeError:
                    pessoa = Pessoas(nome=nome, idade=idade)
                    pessoa.save()
                    response = {
                    'status': "Sucesso",
                    'message': "A Pessoa {} foi adicionada com sucesso".format(nome)
                    }
        else:
            response = {
                    'status': "Erro",
                    'message': "Alguma informação está faltando"
                    }

        return response

class ListaAtividades (Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [
            {
                'id': i.id,
                'pessoa': i.pessoa.nome,
                'nome': i.nome,
                'status': i.status
            }
            for i in atividades
        ]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], status=dados['status'],pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id,
            'status':atividade.status
        }
        return response

class Atividadesinhas (Resource):
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            atividade = Atividades.query.filter_by(pessoa=pessoa)
            response = [
            {
                'id': i.id,
                'pessoa': i.pessoa.nome,
                'nome': i.nome,
                'status': i.status
            }
            for i in atividade
            ]
        except AttributeError:
            response = {
                'status': "Error",
                'message': "Pessoa/atividade não cadastrada"
            }
        return response

class Atividadesinhas2 (Resource):
    @auth.login_required
    def get(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id)
            response = [
            {
                'id': i.id,
                'pessoa': i.pessoa.nome,
                'nome': i.nome,
                'status': i.status
            }
            for i in atividade
            ]
        except AttributeError:
            response = {
                'status': "Error",
                'message': "Não existe nenhuma atividade com esse ID"
            }
        return response

    def delete(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            atividade.delete()
            response = {
                'status': "Sucesso",
                'message': "A atividade com o index {} foi excluida com sucesso".format(id)
            }
        except AttributeError:
            response = {
            'status': "Erro",
            'message': "Não existe nenhuma atividade com esse ID"
            }
        return response
        

    def put(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            dados = request.json
            if 'status' in dados:
                atividade.status = dados['status']
                atividade.save()
            response = {
                    'id': atividade.id,
                    'pessoa': atividade.pessoa.nome,
                    'nome': atividade.nome,
                    'status': atividade.status
                }
        except AttributeError:
            response = {
            'status': "Erro",
            'message': "Não existe nenhuma atividade com esse ID"
            }
        return response

api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(Pessoas2, '/pessoa')
api.add_resource(ListaAtividades, '/atividades')
api.add_resource(Atividadesinhas, '/atividades/<string:nome>')
api.add_resource(Atividadesinhas2, '/atividades/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)