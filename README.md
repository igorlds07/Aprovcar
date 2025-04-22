# 🚗💼 Sistema de Gerenciamento de Garagem de Vendas de Carros

Seja bem-vindo(a)!  
Este sistema foi desenvolvido para auxiliar administradores de garagens a gerenciar:

- Veículos
- Clientes
- Funcionários
- Vendas
- Despesas
- Relatórios
- Caixa diário

Com uma interface intuitiva e recursos completos, ele oferece controle total sobre as operações da garagem.

---

## 📋 Funcionalidades

### 🔐 Autenticação de Usuários
- Login seguro para administradores
- Mensagens de erro/sucesso claras

### 👥 Gestão de Clientes
- Cadastro, edição, busca e exclusão de clientes

### 👨‍💼 Gestão de Funcionários
- Cadastro, edição, exclusão
- Controle de comissões acumulativas

### 🚙 Gestão de Veículos
- Cadastro com dados completos (FIPE, placa, status, etc)
- Listagem e exclusão de veículos (exceto os vendidos)

### 💰 Vendas
- Registro completo da venda
- Cálculo automático de comissão e valor líquido

### 📉 Despesas
- Cadastro e exclusão de despesas

### 📊 Relatórios
- Relatório de vendas, comissões e despesas por período
- Exportação para Excel
- Relatório geral consolidado

### 📆 Caixa Diário
- Visualização de entradas, saídas e saldo diário

### 📈 Cálculo de Repasse
- Sugestão de preço de venda baseado em lucro desejado

---

## 🛠️ Tecnologias Utilizadas
- **Python** (linguagem principal)
- **Flask** (framework web)
- **MySQL** (banco de dados relacional)
- **Pandas** (relatórios e exportação)
- **HTML/CSS/JavaScript** (interface do usuário)
- **Babel** (formatação de valores monetários)

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.x instalado
- MySQL instalado e configurado
- Instalar dependências:
```bash
pip install -r requisitos.txt
```

### Passos
```bash
git clone https://github.com/seu-usuario/sistema-garagem-vendas-carros.git
cd sistema-garagem-vendas-carros
```

1. Configure seu banco no `BD.py`
2. Rode o projeto:
```bash
python app.py
```
3. Acesse no navegador:  
[http://localhost:5001](http://localhost:5001)

---

## 📁 Estrutura do Projeto
```
app.py          # Arquivo principal da aplicação
BD.py           # Configuração da conexão com MySQL
/templates      # Arquivos HTML
/static         # CSS, JS, imagens
```

---

## 📎 Sobre
Projeto criado para fins de aprendizado e portfólio.  
Focado em gestão de garagens de carros, com operações completas e integradas.

---

## ✨ Dica Extra
Adicione prints de tela ou um GIF do sistema funcionando para valorizar ainda mais seu repositório!
