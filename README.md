# Sistema de Gestão de Oficina Automotiva

Este projeto é uma aplicação web desenvolvida com o framework Flask. A aplicação tem como objetivo gerenciar clientes de uma oficina automotiva, permitindo funcionalidades como cadastro, edição, exclusão e consulta de clientes, além de um sistema de login para administradores.

## Funcionalidades

- **Login de Administrador:** Apenas administradores (donos da oficina) podem acessar as funcionalidades de gerenciamento.
- **Cadastro de Clientes:** Permite cadastrar informações como nome, contato, veículo, data de entrada e saída, e valor do orçamento.
- **Edição de Clientes:** O administrador pode atualizar as informações de clientes já cadastrados.
- **Exclusão de Clientes:** O administrador pode excluir registros de clientes do banco de dados.
- **Visualização de Clientes:** Permite consultar clientes cadastrados e exibir todos os clientes ou um cliente específico.

## Tecnologias Utilizadas

- **Flask:** Framework web utilizado para a construção da aplicação.
- **MySQL:** Sistema de gerenciamento de banco de dados utilizado para armazenar as informações dos clientes.
- **HTML / Jinja2:** Para renderizar as páginas da aplicação web.
- **CSS:** Para o estilo visual da aplicação.
  
## Estrutura do Projeto

A aplicação possui as seguintes funcionalidades principais:

1. **Login de Administrador:**
   - Rota: `/`
   - Verifica o login e senha do administrador, autenticando o acesso ao sistema.
   
2. **Cadastro de Clientes:**
   - Rota: `/cadastro`
   - Permite o cadastro de novos clientes no banco de dados.
   - O formulário coleta informações como nome, contato, veículo, data de entrada, data de saída e valor do orçamento.

3. **Edição de Clientes:**
   - Rota: `/editar`
   - Permite editar os dados de um cliente já cadastrado.

4. **Exclusão de Clientes:**
   - Rota: `/excluir_cliente`
   - Permite excluir um cliente do banco de dados, após confirmação do administrador.

5. **Consulta de Clientes:**
   - Rota: `/clientes`
   - Permite visualizar todos os clientes cadastrados ou buscar um cliente específico pelo nome.

## Como Executar

### Pré-requisitos

Antes de rodar a aplicação, você precisará ter o Python e o MySQL instalados em sua máquina.

1. **Instale as dependências**:
   ```bash
   pip install flask mysql-connector-python
