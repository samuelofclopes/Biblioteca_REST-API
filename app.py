from flask import Flask, request, jsonify, render_template
from models.user import db, User
from models.item import Item
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# ============================================================================
# INICIALIZAÇÃO DA APP
# ============================================================================

app = Flask(__name__)

# Configuração
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///biblioteca.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "382o4yv2340n23948xc230ic234jc238ryhc23c12ieuws80qdsaid12hych12333c12udshqhwdiai89wdajs"

# Inicializa extensões
db.init_app(app)
jwt = JWTManager(app)

# Cria as tabelas quando inicia
with app.app_context():
    db.create_all()

# ============================================================================
# ROTAS PRINCIPAIS (Públicas)
# ============================================================================

@app.route("/", methods=["GET"])
def home():
    """Rota de teste - verifica se a API está funcionando"""
    return jsonify({
        "status": "OK",
        "message": "Biblioteca API está a funcionar.",
        "version": "1.0.0"
    }), 200


# ============================================================================
# ROTAS DE AUTENTICAÇÃO (/api/auth/...)
# ============================================================================

@app.route("/api/auth/signup", methods=["POST"])
def signup():
    """
    Registar novo utilizador
    Necessário para criar conta e obter token de acesso:
        "username": "XYZ",
        "email": "XyZ@email.com",
        "password": "senha123XYz"
    """
    
    # Pega os dados do request
    data = request.get_json()
    
    # Valida se os dados estão presentes
    if not data or not data.get("username") or not data.get("email") or not data.get("password") or not data.get("confirm_password"):
        return jsonify({"error": "Username, email, password e confirm_password são obrigatórios"}), 400 # Bad Request - dados faltando ou inválidos
    
    # Verifica se o username já existe
    if User.query.filter_by(username=data["username"]).count() > 0:
        return jsonify({"error": "Username já existe"}), 409 # Conflict - username já existe
    
    # Verifica se o email já existe
    if User.query.filter_by(email=data["email"]).count() > 0:
        return jsonify({"error": "Email já existe"}), 409 # Conflict - email já existe
    
    if data.get("password") != data.get("confirm_password"):
        return jsonify({"error": "Passwords não coincidem"}), 400 # Bad Request - password e confirm_password não coincidem
    
    if len(data.get("password")) < 6 and any(c.isalpha() for c in data.get("password")) and any(c.isdigit() for c in data.get("password")):
        return jsonify({"error": "Password deve ter pelo menos 6 caracteres, incluindo letras e números"}), 400 # Bad Request - password fraca
    # Cria novo utilizador
    novo_user = User(
        username=data["username"],
        email=data["email"]
    )
    novo_user.set_password(data["password"])  # Hasheia a password
    
    # Guarda na BD
    db.session.add(novo_user)
    db.session.commit()
    
    # Retorna sucesso
    return jsonify({
        "message": "Utilizador registado com sucesso",
        "user": {
            "id": novo_user.id,
            "username": novo_user.username,
            "email": novo_user.email
        }
    }), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    """
    Fazer login e receber JWT token
    Necessário para obter token de acesso:
        "username": "XYZ",
        "password": "senha123ZYz"
    """
    
    # Pega os dados do request
    data = request.get_json()
    
    # Valida se os dados estão presentes
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username e password são obrigatórios"}), 400 # Bad Request - dados faltando ou inválidos
    
    # Procura o utilizador
    user = User.query.filter_by(username=data["username"]).first()
    
    # Verifica se existe e se a password está correta
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Username ou password incorretos"}), 401 # Unauthorized - credenciais inválidas
    
    # Cria JWT token
    access_token = create_access_token(identity=user.id)
    
    # Retorna o token
    return jsonify({"token": access_token}), 200 # OK - login bem-sucedido


@app.route("/api/auth/me", methods=["GET"])
@jwt_required()
def me():

    # Ver dados do utilizador autenticado

    
    # Pega o ID do utilizador do token
    user_id = get_jwt_identity()
    
    # Procura o utilizador
    user = User.query.get(user_id)
    
    # Se não existe, retorna erro
    if not user:
        return jsonify({"error": "Utilizador não encontrado"}), 404 # Not Found - utilizador não encontrado
    
    # Retorna dados do utilizador
    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat()
        }
    }), 200


# ============================================================================
# ROTAS DE ITEMS/LIVROS (/api/items/...)
# ============================================================================

@app.route("/api/items", methods=["GET"])
@jwt_required()
def get_items():

    # Listar todos os livros

    items = Item.query.all()
    return jsonify([{
        "id": i.id,
        "title": i.title,
        "author": i.author,
        "total_copies": i.total_copies,
        "available_copies": i.available_copies,
        "is_available": i.is_available()
    } for i in items]), 200 # OK - lista de livros retornada com sucesso


@app.route("/api/items/<int:item_id>", methods=["GET"])
@jwt_required()
def get_item(item_id):

    # Ver detalhes de um livro específico

    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({"error": "Livro não encontrado"}), 404 # Not Found - livro não encontrado
    
    return jsonify({
        "item": {
            "id": item.id,
            "title": item.title,
            "author": item.author,
            "total_copies": item.total_copies,
            "available_copies": item.available_copies,
            "is_available": item.is_available(),
            "created_at": item.created_at.isoformat()
        }
    }), 200 # OK - livro encontrado


@app.route("/api/items", methods=["POST"])
@jwt_required()
def create_item():
    """
    Criar novo livro (requer autenticação)
    Necessário para criar livro:
        "title": "Harry Potter",
        "author": "J.K. Rowling",
        "total_copies": 5
    """
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Apenas admins podem criar livros
    if not user or not user.is_admin:
        return jsonify({"error": "Apenas administradores podem criar livros"}), 403 # Forbidden - utilizador não tem permissão para entrar aqui
    
    data = request.get_json()
    
    # Valida dados
    if not data or not data.get("title") or not data.get("author"):
        return jsonify({"error": "Title e author são obrigatórios"}), 400 # Bad Request - dados faltando ou inválidos
    
    # Cria novo item

    novo_item = Item(
        title=data["title"],
        author=data["author"],
        total_copies=data.get("total_copies", 1)
    )
    novo_item.available_copies = novo_item.total_copies
    # Guarda na BD
    db.session.add(novo_item)
    db.session.commit()
    
    return jsonify({
        "message": "Livro criado com sucesso",
        "item": {
            "id": novo_item.id,
            "title": novo_item.title,
            "author": novo_item.author,
            "total_copies": novo_item.total_copies,
            "available_copies": novo_item.available_copies
        }
    }), 201 # Created - livro criado com sucesso


@app.route("/api/items/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id):
    """
    Editar um livro (requer admin)
    Necessário para editar livro:
        "title": "Novo Título",
        "author": "Novo Autor",
        "total_copies": 10
    """
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Apenas admins podem editar
    if not user or not user.is_admin:
        return jsonify({"error": "Apenas administradores podem editar livros"}), 403 # Forbidden - utilizador não tem permissão para entrar aqui
    
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({"error": "Livro não encontrado"}), 404 # Not Found - livro não encontrado
    
    data = request.get_json()
    
    # Atualiza os campos
    if data.get("title"):
        item.title = data["title"]
    if data.get("author"):
        item.author = data["author"]
    if data.get("total_copies"):
        item.total_copies = data["total_copies"]
    
    db.session.commit()
    
    return jsonify({
        "message": "Livro atualizado com sucesso",
        "item": {
            "id": item.id,
            "title": item.title,
            "author": item.author,
            "total_copies": item.total_copies,
            "available_copies": item.available_copies
        }
    }), 200


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(item_id):

    # Apagar um livro (requer admin)

    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Apenas admins podem apagar
    if not user or not user.is_admin:
        return jsonify({"error": "Apenas administradores podem apagar livros"}), 403 # Forbidden - utilizador não tem permissão para entrar aqui
    
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({"error": "Livro não encontrado"}), 404 # Not Found - livro não encontrado
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({"message": "Livro apagado com sucesso"}), 200 # OK - livro apagado

# =====================================================================================================================================
# ROTAS HTML / FRONTEND
# =====================================================================================================================================

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

@app.route("/profile")
def profile_page():
    return render_template("profile.html")
# ============================================================================
# INICIAR APP
# ============================================================================

if __name__ == "__main__":
    app.run(debug=True, port=8000)