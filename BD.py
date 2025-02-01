import mysql.connector


# Função para conectar ao banco de dados MySQL
def conexao_bd():
    """Função para conectar a um banco de dados já criado"""
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        database='aprovcar',
        password='Oficina@user'
    )
    return conexao
