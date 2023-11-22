'''
Aluno: José Mateus Amaral
Materia: Banco de Dados 2
Professor: Hylson


                        Introducao

        No Programa a baixo estou mostrando a diferenca de desempenho entre tirar a media de um campo
    de uma tabela usando Python3 e usando o proprio sql para fazermos isto.
        No exemplo a baixo estou usando o banco de dados sqlite3 para facilitar a portabilidade do
    programa. Como podesse ver, fica obvio que é mais rapido utilizar o sqlite3 para realizar o processo
    solicitado. Muitos programadores acabam cometendo o erro de realizar esta tarefa usando o python por
    simplismente nao saber que é possivel utiliza-la usando sql.

'''

import sqlite3
import random
import time

def configDB():
    connection_obj = sqlite3.connect('banco.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("DROP TABLE IF EXISTS Usuarios")
    table = """ 
                CREATE TABLE Usuarios (
                    Id INT AUTO_INCREMENT,
                    Username VARCHAR(50)
                );
            """
    cursor_obj.execute(table)
    connection_obj.commit()
    
    for i in range(100000):

        chars = ['a','b','c','d','e','f']
        username = ''
        for cada in range(10):
            username += random.choice(chars)

        query = f"INSERT INTO Usuarios VALUES ({i},'{username}');"
        cursor_obj.execute(query)

    connection_obj.commit()
    connection_obj.close()

configDB()

# pegando a media no sql
connection_obj = sqlite3.connect('banco.db')
cursor_obj = connection_obj.cursor()
start = time.time_ns()
result = cursor_obj.execute("SELECT AVG(Id) FROM Usuarios")
media = result.fetchall()[0][0]
print('\n\nmedia usando sql e avg: ' + str(media))
print(f' tempo sql: { time.time_ns() - start }')
connection_obj.close()


# pegando a media usando python
connection_obj = sqlite3.connect('banco.db')
cursor_obj = connection_obj.cursor()
start = time.time_ns()
result = cursor_obj.execute("SELECT Id FROM Usuarios")
lista = result.fetchall()
media  = 0
counter = len(lista)
for i in lista:
    media += i[0]
media = media / counter
print('\nmedia usando python e select: ' + str(media))
print(f' tempo python: { time.time_ns() - start }\n\n')
connection_obj.close()