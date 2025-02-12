### Sistema de Gerenciamento de Garagem de Vendas de Carros 🚗💼

Bem-vindo ao Sistema de Gerenciamento de Garagem de Vendas de Carros! Este projeto foi desenvolvido para ajudar administradores de garagens a gerenciar veículos, clientes, funcionários, vendas, despesas e muito mais. Com uma interface amigável e funcionalidades robustas, você pode manter tudo organizado e sob controle. Vamos conhecer um pouco mais sobre o que ele faz?

## 📋 Funcionalidades Principais

### 1. Autenticação de Usuários
- **Login de Administradores**: Acesso seguro ao sistema com autenticação de login e senha.
- **Mensagens de Erro e Sucesso**: Feedback claro para o usuário em caso de sucesso ou erro no login.

### 2. Gestão de Clientes
- **Cadastro de Clientes**: Adicione novos clientes com informações como nome, contato, CPF, data de nascimento, data de venda e e-mail.
- **Edição de Clientes**: Atualize as informações dos clientes já cadastrados.
- **Exclusão de Clientes**: Remova clientes do banco de dados de forma segura.
- **Busca de Clientes**: Encontre clientes específicos ou liste todos os clientes cadastrados.

### 3. Gestão de Funcionários
- **Cadastro de Funcionários**: Registre novos vendedores com informações como nome, CPF, contato, data de nascimento e data de admissão.
- **Edição de Funcionários**: Atualize os dados dos funcionários.
- **Exclusão de Funcionários**: Remova vendedores do sistema.
- **Comissões**: Acompanhe e atualize as comissões dos vendedores de forma acumulativa.

### 4. Gestão de Veículos
- **Cadastro de Veículos**: Adicione veículos ao estoque com informações como proprietário, marca/modelo/ano, valor FIPE, placa, data de entrada e status.
- **Exclusão de Veículos**: Remova veículos do estoque (exceto os já vendidos).
- **Listagem de Veículos**: Visualize todos os veículos cadastrados.

### 5. Vendas
- **Registro de Vendas**: Registre vendas de veículos, incluindo informações como vendedor, cliente, data da venda, comissões, taxas e valor líquido.
- **Cálculo Automático**: O sistema calcula automaticamente a comissão total e o valor líquido da venda.

### 6. Despesas
- **Cadastro de Despesas**: Registre despesas com descrição, valor e data.
- **Exclusão de Despesas**: Remova despesas cadastradas.

### 7. Relatórios
- **Relatório de Vendas**: Gere relatórios de vendas por período, com opção de exportar para Excel.
- **Relatório de Despesas**: Visualize despesas por período e exporte para Excel.
- **Relatório de Comissões**: Acompanhe as comissões dos vendedores por período.
- **Relatório Geral**: Consolide informações de vendas, despesas e comissões em um único relatório.

### 8. Caixa Diário
- **Resumo Financeiro**: Visualize o total de entradas (vendas), despesas e o saldo do caixa do dia.

### 9. Cálculo de Repasse
- **Sugestão de Preço de Venda**: Calcule o valor sugerido para venda de um veículo com base no valor do carro, despesas e porcentagem de lucro desejada.

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Flask**: Framework web para criar a aplicação.
- **Pandas**: Manipulação de dados para geração de relatórios em Excel.
- **MySQL**: Banco de dados para armazenamento das informações.
- **HTML/CSS/JavaScript**: Para a interface do usuário.
- **Babel**: Formatação de valores monetários e datas.

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.x instalado.
- MySQL instalado e configurado.
- Bibliotecas Python necessárias (listadas no arquivo `requirements.txt`).

### Passos para Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/sistema-garagem-vendas-carros.git
   cd sistema-garagem-vendas-carros
Instalar as dependências:

pip install -r requirements.txt


Configurar o banco de dados:

Crie um banco de dados MySQL.

Configure como credenciais no arquivo BD.py.
Executar uma aplicação:

python app.py
Acesse o aplicativo:

Abra o navegador e acesse http ://localhost :5001 .
📂 Estrutura do Projeto
app.py: Arquivo principal da aplicação Flask.
BD.py: Configurações de conexão com o banco de dados.
templates/: Pasta contendo os arquivos HTML para as páginas da aplicação.
static/: Pasta para arquivos estáticos (CSS, imagens).
