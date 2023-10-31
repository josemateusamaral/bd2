import sqlite3

# Função para criar a tabela de Pessoa_versionada e a visão Pessoa
def criar_tabela_e_visao():
    conn = sqlite3.connect('pessoa_versionada.db')
    cursor = conn.cursor()
    
    # Criação da tabela Pessoa_versionada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pessoa_versionada (
            cpf TEXT PRIMARY KEY,
            nome TEXT,
            email TEXT,
            telefone TEXT,
            versao INTEGER DEFAULT 1
        )
    ''')
    
    # Criação da visão Pessoa para acessar a versão mais recente dos registros
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS Pessoa AS
        SELECT p.cpf, p.nome, p.email, p.telefone
        FROM Pessoa_versionada p
        WHERE p.versao = (SELECT MAX(versao) FROM Pessoa_versionada p2 WHERE p.cpf = p2.cpf)
    ''')
    
    conn.commit()
    conn.close()

# Função para inserir um novo registro ou atualizar a versão
def inserir_ou_atualizar_registro(cpf, nome, email, telefone):
    conn = sqlite3.connect('pessoa_versionada.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO Pessoa_versionada (cpf, nome, email, telefone, versao)
        SELECT ?, ?, ?, ?, IFNULL((SELECT MAX(versao) FROM Pessoa_versionada WHERE cpf = ?), 0) + 1
    ''', (cpf, nome, email, telefone, cpf))
    
    conn.commit()
    conn.close()

# Função para consultar a visão Pessoa e imprimir os registros
def consultar_pessoa():
    conn = sqlite3.connect('pessoa_versionada.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Pessoa')
    registros = cursor.fetchall()
    
    if not registros:
        print("Nenhum registro encontrado.")
    else:
        print("Registros da Pessoa:")
        for registro in registros:
            print(f"CPF: {registro[0]}, Nome: {registro[1]}, Email: {registro[2]}, Telefone: {registro[3]}")
    
    conn.close()

# Função para excluir um registro
def excluir_registro(cpf):
    conn = sqlite3.connect('pessoa_versionada.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM Pessoa_versionada WHERE cpf = ?', (cpf,))
    
    conn.commit()
    conn.close()

# Cria a tabela e a visão
criar_tabela_e_visao()

# Inserir ou atualizar registros
inserir_ou_atualizar_registro('12345', 'João', 'joao@example.com', '123-456-7890')
inserir_ou_atualizar_registro('12345', 'João Novo', 'joao_novo@example.com', '987-654-3210')

# Consulta a visão Pessoa
consultar_pessoa()

# Exclui um registro
excluir_registro('12345')

# Consulta a visão Pessoa novamente
consultar_pessoa()
