from models import Pessoas, Usuarios

#Insere dados na tabela pessoas
def insere_pessoas():
    pessoa = Pessoas(nome='Gabriel', idade=19)
    print(pessoa)
    pessoa.save()

#Realiza consulta na tabela pessoas
def consulta_pessoas():
    pessoa = Pessoas.query.all()
    print(pessoa)
    pessoa = Pessoas.query.filter_by(nome='Klider').first()
    print(pessoa.idade)

#Altera dados na tabela pessoas
def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Klider').first()
    pessoa.idade = 19
    pessoa.save()

#Exclui dados na tabela pessoas
def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='').first()
    pessoa.delete()

def insere_users():
    user = Usuarios(login='Klider', senha='123')
    print(user)
    user.save()

if __name__ == '__main__':
    #insere_pessoas()
    insere_users()
    #consulta_pessoas()
    #altera_pessoa()
    #exclui_pessoa()