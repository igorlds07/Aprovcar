import os

import locale

from datetime import datetime

import pandas as pd

from flask import Flask, render_template, request, redirect, url_for, flash, make_response

from BD import conexao_bd

from io import BytesIO

from babel.numbers import format_currency

# Nome da aplicação
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configura a localidade para português do Brasil
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


# fazer uma função de login e senha para adms do programa(dono da oficina)
@app.route('/', methods=['GET', 'POST'])
def login_user():
    """ Função que verifica as credenciais de login do administrador.
    Esta função autentica o usuário verificando as informações no banco de dados.
    Caso o login e senha estejam corretos, o usuário será redirecionado para a página principal."""

    error = None
    mensagem = None

    # Condição para ver se o usuário tem acesso ao app
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        conexao_bd()

        conexao = conexao_bd()
        cursor = conexao.cursor()

        # Executa o comando SQL para buscar os parâmetros indicados no login e senha
        cursor.execute('SELECT senha from aprovcar.administradores WHERE login = %s', (login,))

        usuario = cursor.fetchone()
        cursor.close()
        conexao.close()

        if usuario is None:
            error = 'Administrador não cadastrado!'  # Se não encontrado e emetido esta mensagem
        else:
            senha_bd = usuario[0]  # Verificação de senha
            if senha != senha_bd:
                error = 'Senha incorreta!'  # Se incorreta emeti está mensagem

        if error:
            return render_template('login.html', error=error, mensagem=mensagem)  # Passando a mensagem de erro para
            # o template

        mensagem = 'Acesso liberado'

        if mensagem:
            return redirect(url_for('index'))

    return render_template('login.html', mensagem=mensagem)


# Rota para exibir o formulário de cadastro
@app.route('/cadastro')
def index():
    """ Função que renderiza a página de cadastro de clientes.
    Exibe um formulário onde o usuário pode preencher as informações de um novo cliente."""

    return render_template('index.html')


# Rota para cadastrar um novo cliente
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    """ Função que cadastra um novo cliente no banco de dados.
    Recebe os dados preenchidos pelo usuário, insere-os na tabela 'clientes' e exibe uma mensagem de sucesso."""
    if request.method == 'POST':
        nome = request.form['nome']
        contato = request.form['contato']
        cpf = request.form['cpf']
        data_nascimento = request.form['data_nascimento']
        data_venda = request.form['data_venda']
        email = request.form['email']

        # CREAT
        conexao = conexao_bd()
        cursor = conexao.cursor()
        comando = (f'INSERT INTO clientes (nome, contato, cpf, data_nascimento, data_venda, email) '
                   f'VALUES (%s, %s, %s, %s, %s, %s);')
        cursor.execute(comando, (nome, contato, cpf, data_nascimento, data_venda, email))
        conexao.commit()

        cursor.close()
        conexao.close()

        message = 'Cadastrado com sucesso!'
        sucess_mesagge = 'Cliente cadastrado com sucesso'
        print(sucess_mesagge)

        # Ao clicar o botão cadastrar e emetido a mensagem de 'sucesso' e  retorna a  página de cadastro
        return render_template('index.html', message=message)

    return render_template('index.html')  # Ao finalizar o processo retorna a página de cadastro novamente


# Rota para editar os clientes já cadastrados no BANCO DE DADOS
@app.route('/editar', methods=['GET', 'POST'])
def editar_cliente():
    """Editar informações de um cliente cadastrado"""

    conexao = conexao_bd()
    cliente = None

    if request.method == 'GET' and 'cliente' in request.args:
        nome_cliente = request.args.get('cliente')
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM clientes WHERE nome = %s", (nome_cliente,))
        cliente = cursor.fetchone()
        cursor.close()
        conexao.close()

        if not cliente:
            flash('Cliente não encontrado!', 'error')
            return redirect(url_for('editar_cliente'))

    if request.method == 'POST':
        nome_original = request.form['cliente_original']
        nome = request.form['nome']
        contato = request.form['contato']
        cpf = request.form['cpf']
        data_nascimento = request.form['data_nascimento']
        data_venda = request.form['data_venda']
        email = request.form['email']

        cursor = conexao.cursor()
        cursor.execute("""UPDATE clientes SET nome = %s, contato = %s, cpf = %s, data_nascimento = %s,
                          data_venda = %s, email = %s WHERE nome = %s""",
                       (nome, contato, cpf, data_nascimento, data_venda, email, nome_original))
        conexao.commit()

        cursor.close()
        conexao.close()

        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('editar_cliente'))

    return render_template('editar.html', cliente=cliente)


# Rota para excluir clientes no banco de dados
@app.route('/excluir_cliente', methods=['GET', 'POST'])
def excluir_cliente():
    """  Função para excluir um cliente do banco de dados.
    O cliente é excluído após uma confirmação do administrador."""

    conexao = conexao_bd()
    cliente = None

    # Condição para verificar se existe o cliente específicado no banco de dados
    if request.method == 'POST':
        nome_cliente = request.form['nome']
        print(f"Nome do cliente enviado: {nome_cliente}")
        print(f"Dados do formulário: {request.form}")

        # Se o cliente for encontrado executa a exclusão
        if nome_cliente:
            cursor = conexao.cursor()

            # DELETE
            cursor.execute('SELECT * FROM clientes WHERE nome = %s;', (nome_cliente,))
            cliente = cursor.fetchone()
            print(cliente)

            # Condição para verificar se o usuário deseja confirmar o delete
            if cliente:
                if request.form.get('confirmar') == 'sim':
                    print('botão pressionado')

                    cursor = conexao.cursor()
                    # Comando em SQL para deletar o cliente
                    comando = f'DELETE FROM clientes WHERE nome = "{nome_cliente}"'
                    cursor.execute(comando)
                    print(f'excluindo cliente {nome_cliente}')

                    conexao.commit()
                    print(f'cliente excluido com  successo')
                    flash(f'Cliente {nome_cliente} excluído com sucesso!', 'success')
                    return render_template('excluir_cliente.html', cliente=None)  # Redireciona após exclusão

            else:
                flash('Cliente não encontrado!', 'error')

        else:
            flash('Por favor, informe o nome do cliente.', 'warning')  # Senão for passado
            # o nome para busca retorna esta mensagem

            return redirect(url_for('excluir_cliente'))

    return render_template('excluir_cliente.html', cliente=cliente)  # Após o procedimento retorna a
    # página excluir_cliente


# Rota para mostrar todos os clientes e algum cliente específico
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    """Função para buscar clientes no banco de dados.
    Permite buscar por nome ou exibir todos os clientes cadastrados."""

    conexao = conexao_bd()  # Conexão com o banco de dados
    cursor = conexao.cursor()

    cliente_cadastrado = []

    if request.method == 'POST':

        nome = request.form['nome']
        if nome:
            # READ
            # Comando em SQL para buscar o cliente específicado
            comando = 'SELECT  * FROM clientes WHERE nome = %s;'
            cursor.execute(comando, (nome,))

            cliente_cadastrado = cursor.fetchall()
            print(cliente_cadastrado)

        # Condição para verificar se o cliente foi encontrado
        if not cliente_cadastrado:
            cliente_cadastrado = ['Cliente não encontrado']

    # Condição para vereificar se o usuário deseja ver todos os clientes
    if request.method == 'GET' and 'ver_todos' in request.args:
        # Comando em SQL para buscar todos os clientes
        comando = 'SELECT * FROM clientes;'
        cursor.execute(comando)

        cliente_cadastrado = cursor.fetchall()
    cursor.close()
    conexao.close()  # A conexão com o banco de dados é finalizada

    # Após todas as buscas retorna a página clientes.html
    return render_template('clientes.html', clientes=cliente_cadastrado)


# Rota para cadastrar e visualizar todos os funcionários
@app.route('/funcionarios', methods=['GET', 'POST'])
def funcionarios():
    """
    Função para cadastra um novo vendedor e isererir no banco de dados, de acordo com os dados passado pelo administra
    .Também permite visualizar todos os vendedores já cadastrados quando solicitados.

    Metódos:

    GET: Busca todos os vendedores no banco de dados.
    POST: Cadastra um novo vendedor de acordo com os dados passado no formulário.

    :return: renderiza o template 'fuincionarios.html' com uma lista de vendedores ou message de sucesso ou erro.
    """

    # Conexão com o banco de dados
    conexao = conexao_bd()
    cursor = conexao.cursor()

    # Se a requisição for GET, busca todos os funcionários no banco de dados
    if request.method == 'GET' and 'ver_todos' in request.args:
        comando = 'SELECT * FROM vendedor;'  # Comando em SQL para buscar todos os vendedores
        cursor.execute(comando, )
        funcionario = cursor.fetchall()
        print(funcionario)
        if not funcionario:  # Condição se o  vendedor não for encontrado, renderiza uma mensagem de erro
            flash('Nenhum vendedor foi encontrado !', 'error')

        # Retorna a página com todos os vendedores encontrados
        return render_template('funcionarios.html', funcionarios=funcionario)

    # Se a requisição for POST, cadastra um novo vendedor no banco de dados
    if request.method == 'POST':
        nome = request.form['nome'].title()
        cpf = request.form['cpf']
        contato = request.form.get('contato')
        data_nascimento = request.form['data_nascimento']
        data_admissao = request.form['data_admissao']

        # Verifica se já existe um funcionário com esse nome (ou outro identificador)
        comando = ("INSERT INTO vendedor (nome, cpf, contato, data_nascimento, data_admissão)"
                   " VALUES (%s, %s, %s, %s, %s);")
        cursor.execute(comando, (nome, cpf, contato, data_nascimento, data_admissao))

        # Comando para salvar no banco de dados
        conexao.commit()
        flash('Funcionário cadastrado com sucesso !', 'success')
        funcionarios_cadastrados = cursor.fetchall()

        # Retorna a página com a mensagem de de sucesso
        return render_template('funcionarios.html', funcionarios=funcionarios_cadastrados)

    # Se nenhuma das condições a cima acontecer retorna a página novamente
    return render_template('funcionarios.html')


# Rota para excluir um funcionário
@app.route('/excluir_funcionario', methods=['GET', 'POST'])
def excluir_funcionario():
    """
    
    :return:
    """
    conexao = conexao_bd()
    cursor = conexao.cursor()
    vendedor = None
    if request.method == 'POST':
        nome = request.form.get('nome')

        if nome:
            cursor.execute('SELECT * FROM vendedor WHERE nome = %s;', (nome,))
            vendedor = cursor.fetchone()

            if vendedor:
                if request.form.get('confirmar') == 'sim':
                    print('botão pressionado')

                    cursor = conexao.cursor()
                    # Comando em SQL para deletar o cliente
                    comando = f'DELETE FROM vendedor WHERE nome = "{nome}"'

                    cursor.execute(comando)
                    print(f'excluindo cliente {vendedor}')

                    conexao.commit()
                    print(f'cliente excluido com  successo')
                    flash(f'Vendedor {vendedor[1]} excluído com sucesso!', 'success')
                    return render_template('excluir_funcionario.html', vendedor=None)  # Redireciona após exclusão

            else:
                flash('Funcionário não encontrado!', 'error')

        else:
            flash('Por favor, informe o nome do cliente.', 'warning')  # Senão for passado
            return redirect(url_for('excluir_funcionario'))

    return render_template('excluir_funcionario.html', vendedor=vendedor)


@app.route('/editar_funcionario', methods=['GET', 'POST'])
def editar_funcionario():
    conexao = conexao_bd()
    cursor = conexao.cursor()
    vendedor = None

    if request.method == 'GET' and 'vendedor' in request.args:
        nome_vendedor = request.args.get('vendedor')
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM vendedor WHERE nome = %s", (nome_vendedor,))
        vendedor = cursor.fetchone()
        print(vendedor)
        cursor.close()
        conexao.close()
        if not vendedor:
            flash('Funcionário não encontrado !', 'error')
            conexao.close()
            cursor.close()
            return redirect(url_for('editar_funcionario'))

    if request.method == 'POST':
        nome_original = request.form['nome_original']
        nome = request.form['nome']
        cpf = request.form['cpf']
        contato = request.form['contato']
        data_nascimento = request.form['data_nascimento']
        data_admissao = request.form['data_admissao']

        cursor.execute(
            """UPDATE vendedor SET nome = %s, cpf = %s, contato = %s,
                data_nascimento = %s, data_admissão = %s WHERE nome = %s""",
            (nome, cpf, contato, data_nascimento, data_admissao, nome_original))

        conexao.commit()
        print('ATUALIZADO COM SUCESSO')

        cursor.close()
        conexao.close()  # Fecha a conexão com o  banco de dados

        flash('Vendedor atualizado com sucesso!', 'success')  # Mensagem de sucesso com flash
        return redirect(url_for('editar_funcionario'))  # Redireciona para o formulário de edição novamente

    return render_template('editar_funcionario.html', vendedor=vendedor)


@app.route('/vendedor_atualizar', methods=['GET', 'POST'])
def vendedor_atualizar():
    """Função para atualizar a comissão do funcionário existente, com o modelo acumulativo mensalmente
    e é zerado após inicio de cada mês"""

    # Conexão com o banco de dados
    conexao = conexao_bd()
    cursor = conexao.cursor()

    # Condição para resgatar o funcionário escolhido pelo administrador
    if request.method == 'POST':
        # Obter o ID ou nome do funcionário selecionado
        vendedor_id = request.form.get('vendedor_id')
        id_carro = request.form.get('id_carro')
        data_comissao = request.form.get('data_comissao')
        valor_comissao = request.form.get('valor_comissao')

        # Condição que só é executada se algum funcionário selecionado
        if vendedor_id:

            # Comando em SQL para buscar o funcionário escolhido
            cursor.execute('SELECT * FROM vendedor  WHERE idvendedor = %s;', (vendedor_id,))
            funcionario_escolhido = cursor.fetchone()

            if funcionario_escolhido:
                cursor.execute(
                    'INSERT INTO comissão(idvendedor, idcarro, data_comissao, valor_comissao)'
                    'VALUES(%s, %s, %s, %s)', (vendedor_id, id_carro, data_comissao, valor_comissao))

                conexao.commit()
                flash('Comissão adicionada com sucesso !', 'success')
                conexao.close()
                cursor.close()
                return render_template('vendedor_atualizar.html')

            else:
                flash('Vendedor não encontrado!', 'error')

    # Carregar todos os funcionários para exibir na lista
    cursor.execute('SELECT * FROM vendedor')

    vendedores = cursor.fetchall()
    conexao.close()  # Fecha a conexão com o cursor
    conexao.close()

    # Retorna ao template o resultado de todo o procedimento
    return render_template('vendedor_atualizar.html', vendedores=vendedores)


@app.route('/relatorio_vendas', methods=['GET', 'POST'])
def relatorio_vendas():
    conexao = conexao_bd()
    cursor = conexao.cursor()
    resultados = None

    if request.method == 'POST':
        data_inicio = request.form['data_entrada']
        data_fim = request.form['data_saida']
        gerar_excel = request.form.get('gerar_excel')

        if data_inicio and data_fim:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')

            if data_inicio > data_fim:
                flash('A data de inicío não pode ser maior que a data de fim!', 'error')
                return render_template(
                    'relatorio_vendas.html', )

        # Consulta SQL para buscar orçamentos no período
        query = """
                    SELECT 
                v.idvendas, 
                vend.nome AS Nome_Vendedor, 
                est.Marca_modelo_ano AS Modelo_Carro,
                v.idCliente,
                v.Nome_cliente, 
                v.Data_venda, 
                v.Comissao_carro, 
                v.Retorno_finaciamento, 
                v.taxa_financiamento, 
                v.Comissao_total, 
                v.Transferencia, 
                v.Comissao_vendedor,
                v.Corretor, 
                v.Dizimo, 
                v.Valor_liquido
            FROM vendas v
            JOIN vendedor vend ON v.idvendedor = vend.idvendedor
            JOIN estoque est ON v.idcarro = est.idcarro
            WHERE v.Data_venda BETWEEN %s AND %s
                """
        cursor.execute(query, (data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')))
        resultados = cursor.fetchall()
        print(resultados)

        if not resultados:
            flash('Não foi encontrado nenhuma venda dentro do período!', 'error')
            return render_template('relatorio_vendas.html')

            # Se o botão para gerar Excel foi pressionado
        if gerar_excel:
            # Cria um DataFrame com os resultados
            colunas = [
                "Id vendas", "Id vendedor", "Id carro", "Id cliente", "Nome Cliente", "Data Venda",
                "Comissão Carro", "Retorno finaciamento", "Taxa Financiamento",
                "Comissão Total", "Transfêrencia", "Comissão Vendedor", "Corretor", "Dízimo", "Valor Liquído"]

            df = pd.DataFrame(resultados, columns=colunas)
            print(df)

            # Salva o DataFrame em um arquivo Excel na memória
            output = BytesIO()
            df.to_excel(output, index=False, sheet_name='Relatório de Vendas')
            output.seek(0)

            # Configura a resposta para download
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=relatorio_vendas.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response

        query = """
                       SELECT SUM(valor_liquido) 
                       FROM vendas
                        WHERE data_venda BETWEEN %s AND %s
                   """
        cursor.execute(query, (data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')))
        total_entradas = cursor.fetchone()[0] or 0

        total = len(resultados)

        data_inicio_formatada = data_inicio.strftime('%d/%m/%Y')
        data_fim_formatada = data_fim.strftime('%d/%m/%Y')

        message = (
            f'Data inicío: {data_inicio_formatada} <br>'
            f'Data fim: {data_fim_formatada} <br>'
            f'Foram realizados {total} Venda(s) !<br>'
            f'Total Liquído: {format_currency(total_entradas, "BRL", locale="pt_BR")}')

        conexao.close()
        cursor.close()

        return render_template('relatorio_vendas.html', resultados=resultados, message=message)

    return render_template('relatorio_vendas.html', resultados=resultados)


@app.route('/relatorio_despesas', methods=['GET', 'POST'])
def relatorio_despesas():
    conexao = conexao_bd()
    cursor = conexao.cursor()
    resultado = None
    despesa = []
    total_despesas = 0

    if request.method == 'POST':
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')
        gerar_excel = 'gerar_excel' in request.form

        if data_inicio and data_fim:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
            print(data_inicio, data_fim)

            if data_fim < data_inicio:
                flash('A data do fim não pode ser menor que a data de inicío!', 'error')
                return render_template('relatorio_despesas.html')

        query = """
                    SELECT iddespesas, descrição, valor_despesa, data_despesa
                    FROM despesas
                    WHERE data_despesa BETWEEN %s AND %s
                """
        print(data_inicio, data_fim)
        cursor.execute(query, (data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')))
        resultado = cursor.fetchall()
        print(resultado)

        if not resultado:
            flash('Não foi encontrada nenhuma despesa no período!', 'error')
            return render_template('relatorio_despesas.html')

        if gerar_excel:
            # Cria um DataFrame com os resultados
            colunas = [
                "Id despesa", "Descrição", "Valor despesa", "Data despesa"
            ]
            df = pd.DataFrame(resultado, columns=colunas)

            print(df)

            # Salva o DataFrame em um arquivo Excel na memória
            output = BytesIO()
            df.to_excel(output, index=False, sheet_name='Relatório de Despesas')
            output.seek(0)

            # Configura a resposta para download
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=relatorio_despesas.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            flash('Relatório gerado com sucesso!', 'success')
            return response

        total = sum(despesa[2] for despesa in resultado)  # Despesa[2] é o valor

        total_despesas = total

        return render_template('relatorio_despesas.html', despesas=resultado, total_despesas=total_despesas)

    return render_template('relatorio_despesas.html', despesa=despesa, total_despesas=total_despesas)


@app.route('/relatorio_vendedor', methods=['GET', 'POST'])
def relatorio_vendedor():
    conexao = conexao_bd()
    cursor = conexao.cursor()

    resultado = None

    if request.method == 'POST':
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        gerar_excel = 'gerar_excel' in request.form

        if data_fim and data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')

            if data_fim < data_inicio:
                flash('A data fim não pode ser maior que a data inicío!', 'error')
                return render_template('relatorio_vendedor.html')

        query = """SELECT c.idcomissão, v.nome AS vendedor_nome, ca.`Marca_modelo_ano` AS carro_modelo, 
                          c.data_comissao, c.valor_comissao
                   FROM comissão c
                   JOIN vendedor v ON c.idvendedor = v.idvendedor
                   JOIN estoque ca ON c.idcarro = ca.idcarro
                   WHERE c.data_comissao BETWEEN %s AND %s"""

        cursor.execute(query, (data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')))
        resultado = cursor.fetchall()

        if not resultado:
            flash('Nenhum resultado encontrado no período!', 'error')
            return render_template('relatorio_vendedor.html')

        if gerar_excel:
            # Cria um DataFrame com os resultados
            colunas = [
                "Id comissão", "Vendedor", "Marca/modelo/ano", "Data comissão", "Valor Comissão"
            ]
            df = pd.DataFrame(resultado, columns=colunas)

            # Salva o DataFrame em um arquivo Excel na memória
            output = BytesIO()
            df.to_excel(output, index=False, sheet_name='Relatório de Comissão')
            output.seek(0)

            # Configura a resposta para download
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=relatorio_comissão.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            flash('Relatório gerado com sucesso!', 'success')
            return response

        print(resultado)

        return render_template('relatorio_vendedor.html', resultado=resultado)

    return render_template('relatorio_vendedor.html', resultado=resultado)


'''@app.route('/relatorio_geral', methods=['GET', 'POST'])
def relatorio_geral():
    conexao = conexao_bd()
    cursor = conexao.cursor()

    if request.method == 'POST':
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        gerar_excel = 'gerar_excel' in request.form

        if data_inicio and data_fim:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')

            if data_fim < data_inicio:
                flash('A data final não pode ser menor que a data de início', 'error')
                return render_template('relatorio_geral.html')

        # Consulta para consolidar vendas, despesas e comissões
        query = """
            SELECT 
                'Venda' AS tipo,
                v.idvendas AS id,
                v.Data_venda AS data,
                v.Valor_liquido AS valor
            FROM vendas v
            WHERE v.Data_venda BETWEEN %s AND %s
            UNION ALL
            SELECT 
                'Despesa' AS tipo,
                d.iddespesas AS id,
                d.data_despesa AS data,
                -d.valor_despesa AS valor
            FROM despesas d
            WHERE d.data_despesa BETWEEN %s AND %s
            UNION ALL
            SELECT 
                'Comissão' AS tipo,
                c.idcomissão AS id,
                c.data_comissao AS data,
                -c.valor_comissao AS valor
            FROM comissão c
            WHERE c.data_comissao BETWEEN %s AND %s
            ORDER BY data;
        """
        cursor.execute(query, (data_inicio, data_fim, data_inicio, data_fim, data_inicio, data_fim))
        resultados = cursor.fetchall()

        if not resultados:
            flash('Nenhum resultado encontrado no período!', 'error')
            return render_template('relatorio_geral.html')

        if gerar_excel:
            # Cria um DataFrame com os resultados
            colunas = ["Tipo", "ID", "Data", "Valor"]
            df = pd.DataFrame(resultados, columns=colunas)

            # Salva o DataFrame em um arquivo Excel na memória
            output = BytesIO()
            df.to_excel(output, index=False, sheet_name='Relatório Geral')
            output.seek(0)

            # Configura a resposta para download
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=relatorio_geral.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            flash('Relatório gerado com sucesso!', 'success')
            return response

        # Calcula totais
        total_vendas = sum(row[3] for row in resultados if row[0] == 'Venda')
        total_despesas = sum(row[3] for row in resultados if row[0] == 'Despesa')
        total_comissoes = sum(row[3] for row in resultados if row[0] == 'Comissão')
        saldo_final = total_vendas + total_despesas + total_comissoes

        # Formata as datas para exibição
        data_inicio_formatada = data_inicio.strftime('%d/%m/%Y')
        data_fim_formatada = data_fim.strftime('%d/%m/%Y')

        message = (
            f'Data início: {data_inicio_formatada} <br>'
            f'Data fim: {data_fim_formatada} <br>'
            f'Total Vendas: {format_currency(total_vendas, "BRL", locale="pt_BR")} <br>'
            f'Total Despesas: {format_currency(total_despesas, "BRL", locale="pt_BR")} <br>'
            f'Total Comissões: {format_currency(total_comissoes, "BRL", locale="pt_BR")} <br>'
            f'Saldo Final: {format_currency(saldo_final, "BRL", locale="pt_BR")}'
        )

        conexao.close()
        cursor.close()

        return render_template('relatorio_geral.html', resultados=resultados, message=message)

    return render_template('relatorio_geral.html')'''


@app.route('/despesas', methods=['GET', 'POST'])
def despesas():
    conexao = conexao_bd()
    cursor = conexao.cursor()

    if request.method == 'POST':
        descricao = request.form['descrição']
        data = request.form['data']
        valor = request.form['valor']

        valor_numerico = float(valor.replace(",", "."))

        cursor.execute('INSERT INTO despesas(descrição, valor_despesa, data_despesa)'
                       'VALUES(%s, %s,%s);', (descricao, valor_numerico, data))

        conexao.commit()
        conexao.close()
        cursor.close()
        print(f'Despesas foram inseridas {descricao} , {data}, {valor} ')
        flash('Despesa adicionada com sucesso!', 'sucess')

        return render_template('despesas.html')

    return render_template('despesas.html')


@app.route('/excluir_despesa', methods=['GET', 'POST'])
def excluir_despesa():
    conexao = conexao_bd()
    cursor = conexao.cursor()
    buscar = []

    if request.method == 'POST':
        despesa = request.form.get('descrição')  # Nome da despesa para busca
        descricao_confirmada = request.form.get('descricao')  # Nome da despesa ao excluir
        confirmar = request.form.get('confirmar')

        print(f"Despesa: {despesa}, Confirmar: {confirmar}, Descrição Confirmada: {descricao_confirmada}")

        # Se o usuário buscou uma despesa
        if despesa:
            cursor.execute('SELECT * FROM despesas WHERE descrição = %s;', (despesa,))
            buscar = cursor.fetchall()
            if not buscar:
                flash('Despesa não encontrada!', 'error')
                return render_template('excluir_despesa.html')

        # Se o usuário confirmou a exclusão
        if descricao_confirmada and confirmar == 'sim':
            print("Excluindo despesa:", descricao_confirmada)
            comando = 'DELETE FROM despesas WHERE descrição = %s;'
            cursor.execute(comando, (descricao_confirmada,))
            conexao.commit()

            flash(f'Despesa "{descricao_confirmada}" excluída com sucesso!', 'success')
            buscar = []  # Limpa a busca após exclusão

    return render_template('excluir_despesa.html', buscar=buscar)


@app.route('/vendas', methods=['GET', 'POST'])
def vendas():
    conexao = conexao_bd()
    cursor = conexao.cursor()

    # Rota para registrar uma venda
    if request.method == 'POST':
        idvendedor = request.form.get('idvendedor')
        idcarro = request.form.get('idcarro')
        idcliente = request.form.get('idCliente')
        nome_cliente = request.form['Nome_cliente']
        data_venda = request.form['data_venda']
        comissao_carro = float(request.form['Comissao_carro'])
        retorno_financiamento = float(request.form['Retorno_financiamento'])
        taxa_financiamento = float(request.form['Taxa_financiamento'])
        transferencia = float(request.form['Transferencia'])
        comissao_vendedor = float(request.form['comissao_vendedor'])
        corretor = float(request.form['Corretor'])
        dizimo = float(request.form['Dizimo'])

        # Validar se o vendedor existe
        cursor.execute("SELECT * FROM vendedor WHERE idvendedor = %s", (idvendedor,))
        vendedor = cursor.fetchone()
        if not vendedor:
            flash("Vendedor não encontrado!", "error")
            return redirect(url_for('vendas'))

        cursor.execute("SELECT status from estoque WHERE idcarro = %s;", (idcarro, ))

        status_atual = cursor.fetchone()
        print(status_atual)

        status = "Disponível"

        if status_atual:

            status_atual = status_atual[0]
            print(status_atual)

            if status_atual != status:
                flash("Este carro já foi vendido !", 'error')
                return render_template('vendas.html')

        # Validar se o carro existe e não foi vendido
        cursor.execute("SELECT * FROM estoque WHERE idcarro = %s", (idcarro,))
        carro = cursor.fetchone()
        if not carro:
            flash("Carro não encontrado!", "error")
            return redirect(url_for('vendas'))

        # Calcular comissão total e valor líquido
        comissao_total = comissao_carro + retorno_financiamento - taxa_financiamento
        valor_liquido = comissao_total - transferencia - corretor - comissao_vendedor - dizimo

        # Inserir venda no banco de dados
        comando = """
        INSERT INTO vendas 
        (idvendedor, idcarro, idCliente, Nome_cliente, Data_venda, Comissao_carro, Retorno_finaciamento, 
         Taxa_financiamento, Comissao_total, Transferencia, Comissao_vendedor, Corretor, Dizimo, Valor_liquido) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (idvendedor, idcarro, idcliente, nome_cliente, data_venda, comissao_carro, retorno_financiamento,
                   taxa_financiamento, comissao_total, transferencia, comissao_vendedor, corretor, dizimo,
                   valor_liquido)

        comando2 = """
        INSERT INTO comissão(idvendedor, idcarro, data_comissao, valor_comissao)
        VALUES(%s, %s, %s, %s);
        """
        valores2 = (idvendedor, idcarro, data_venda, comissao_vendedor)

        cursor.execute(comando, valores)
        cursor.execute(comando2, valores2)
        status = "Vendido"
        # Atualizar status do carro para vendido
        cursor.execute(
            "UPDATE estoque SET `status` = %s WHERE idcarro = %s",
            (status, idcarro,))

        # Commit e fechar conexão
        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Venda registrada com sucesso!", "success")
        return redirect(url_for('vendas'))

    return render_template('vendas.html')


@app.route('/estoque', methods=['GET', 'POST'])
def estoque():
    conexao = conexao_bd()
    cursor = conexao.cursor()

    carros = None

    if request.method == 'GET' and 'ver_todos' in request.args:
        comando = 'SELECT * FROM estoque'

        cursor.execute(comando)

        carros = cursor.fetchall()

        cursor.close()
        conexao.close()
        return render_template('estoque.html', carros=carros)

    if request.method == 'POST':
        proprietario = request.form['proprietario'].title()
        marca_modelo_ano = request.form['marca_modelo_ano']
        fipe = float(request.form['fipe'])
        placa = request.form['placa']
        data_entrada = request.form['data_entrada']
        status = request.form['status']

        cursor.execute(
            """INSERT INTO estoque(proprietario, `Marca_modelo_ano`, fipe, placa, data_entrada, status)
            VALUES(%s, %s, %s, %s, %s, %s)""", (proprietario, marca_modelo_ano, fipe, placa, data_entrada, status))

        conexao.commit()
        print('CARRO CADASTRADO COM SUCEESO')
        conexao.close()
        cursor.close()

        flash('Carro adicionado no estoque!', 'sucess')
        return render_template('estoque.html', carros=carros)

    return render_template('estoque.html', carros=None)


@app.route('/excluir_veiculo', methods=['GET', 'POST'])
def excluir_veiculo():
    conexao = conexao_bd()
    cursor = conexao.cursor()
    carro = []

    if request.method == 'POST':
        id_carro = request.form.get('id_veiculo')
        confirmar = request.form.get('confirmar')

        print(f"id_carro: {id_carro}, Confirmar: {confirmar}")

        if id_carro:
            id_veiculo = int(id_carro)
            cursor.execute('SELECT * FROM estoque WHERE idcarro = %s;', (id_veiculo, ))
            carro = cursor.fetchall()
            print(carro)
            if not carro:
                flash('Veículo não encontrado!', 'error')
                print('não encontrado')
                return render_template('excluir_veiculo.html')

        if confirmar == 'sim':
            status = carro[0][6]
            if status == "Vendido":
                flash('O veículo não pode ser excluido', 'error')
                return render_template('excluir_veiculo.html')
            id_veiculo = int(id_carro)
            print('Confirmado')
            cursor.execute('DELETE FROM estoque WHERE idcarro = %s;', (id_veiculo, ))
            conexao.commit()
            flash('Veículo excluido com sucesso', 'success')
            carro = []

    return render_template('excluir_veiculo.html', carro=carro)


@app.template_filter('real')
def formatar_real(valor):
    return format_currency(valor, 'BRL', locale='pt_BR')


# Filtro personalizado para formatar a data
@app.template_filter('to_date')
def to_date(value, format='%d de %B de %Y'):
    if isinstance(value, str):  # Verifica se é uma string
        value = datetime.strptime(value, '%Y-%m-%d')  # Converte a string para datetime
    return value.strftime(format)  # Formata a data para o formato desejado


@app.route('/caixa_diario', methods=['GET'])
def caixa_diario():
    conexao = conexao_bd()
    cursor = conexao.cursor()

    # Obtendo a data de hoje
    data = datetime.now().strftime('%Y-%m-%d')
    data_hoje = datetime.now().strftime('%Y-%m-%d')

    # Consulta para buscar entradas (pagamentos ou orçamentos com valor pago)
    cursor.execute("""
        SELECT SUM(valor_liquido) 
        FROM vendas
        WHERE DATE(data_venda) = %s;
    """, (data_hoje,))
    total_entradas = cursor.fetchone()[0] or 0  # Caso não haja entradas, soma como 0

    # Consulta para buscar despesas do dia
    cursor.execute("""
        SELECT SUM(valor_despesa) 
        FROM despesas 
        WHERE DATE(data_despesa) = %s;
    """, (data_hoje,))
    total_despesas = cursor.fetchone()[0] or 0  # Caso não haja despesas, soma como 0

    # Calculando o saldo do caixa
    saldo_caixa = total_entradas - total_despesas

    # Fechando a conexão com o banco
    conexao.close()
    cursor.close()

    # Exibindo na interface
    return render_template(
        'caixa_diario.html',
        data=data,
        data_hoje=data_hoje,
        total_entradas=total_entradas,
        total_despesas=total_despesas,
        saldo_caixa=saldo_caixa
    )


@app.route('/calcular_repasse', methods=['GET', 'POST'])
def calcular_repasse():

    if request.method == 'POST':
        print(request.form)
        carro = request.form.get('carro')
        despesas = request.form.get('despesas')
        porcentagem = request.form.get('porcentagem')

        if not carro or not despesas or not porcentagem:
            flash('Preencha todos os campos necessários', 'error')
            return render_template('calcular_repasse.html')

        valor_carro = float(carro)
        valor_despesas = float(despesas)
        lucro_porcentagem = float(porcentagem)

        caluculo = valor_carro + valor_despesas
        repasse = caluculo * (lucro_porcentagem / 100) + caluculo

        print(repasse)

        message = (
            f'Veículo = {format_currency(valor_carro, "BRL", locale="pt_BR")}<br>'
            f'                               +      <br>'
            f'Despesas = {format_currency(valor_despesas, "BRL", locale="pt_BR")}<br>'
            f'                              +        <br>'
            f'Porcentagem lucro = {lucro_porcentagem}%<br>'
            f'  <br>       '
            f'O valor sugerido para venda é de {format_currency(repasse, "BRL", locale="pt_BR")}.')
        return render_template('calcular_repasse.html', lucro=repasse, message=message)

    return render_template('calcular_repasse.html')


# Condição para verificar se o projeto esta sendo executado diretamente
if __name__ == '__main__':
    app.run(port=5001, debug=True)
