from flask import Flask
from .utils.database import conexao_bd
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)  # Gera uma chave secreta aleatória

    # Registrar blueprints (rotas)
    from .routes.auth import auth_bp
    from .routes.clientes import clientes_bp
    from .routes.vendedores import vendedores_bp
    from .routes.vendas import vendas_bp
    from .routes.despesas import despesas_bp
    from .routes.relatorios import relatorios_bp
    from .routes.estoque import estoque_bp

    # Adicionando prefixos para evitar conflitos
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    app.register_blueprint(vendedores_bp, url_prefix='/vendedores')
    app.register_blueprint(vendas_bp, url_prefix='/vendas')
    app.register_blueprint(despesas_bp, url_prefix='/despesas')
    app.register_blueprint(relatorios_bp, url_prefix='/relatorios')
    app.register_blueprint(estoque_bp, url_prefix='/estoque')

    app = Flask(__name__, template_folder="templates")  # Dizendo onde estão os templates
    app.secret_key = os.urandom(24)

    app.config['DATABASE'] = conexao_bd()

    # Registrar blueprints (rotas)
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app

