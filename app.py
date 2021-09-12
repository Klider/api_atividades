from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.wrappers import response
from models import Pessoas, Atividades

app = Flask(__name__)
api = Api(app)

class Pessoa(Resource):
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
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
        return response
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        pessoa.delete()
        response = {
            'status': "Sucesso",
            'message': "A Pessoa {} foi excluida com sucesso".format(nome)
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
                'nome': i.nome
            }
            for i in atividades
        ]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id
        }
        return response


api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(Pessoas2, '/pessoa')
api.add_resource(ListaAtividades, '/atividades')

if __name__ == '__main__':
    app.run(debug=True)