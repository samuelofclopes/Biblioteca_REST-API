from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    # Modelo de Utilizador
    __tablename__ = 'user'
    
    id =              db.Column(db.Integer, primary_key=True) # ID do utilizador, chave primária para procurar os dados
    username =        db.Column(db.String(80), unique=True, nullable=False) # Nome de utilizador, único
    email =           db.Column(db.String(150), unique=True, nullable=False) # Email do utilizador, único
    password_hash =   db.Column(db.String(300), nullable=False) # Hash da senha do utilizador - (300 caracteres para garantir espaço suficiente para o hash)
    is_admin =        db.Column(db.Boolean, default=False)  # Indica se o utilizador é administrador
    created_at =      db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) # Pega o tempo UTC no momento que é preciso ser usado, ou seja, na criação do utilizador.
    
    def __str__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) # Gera o hash da senha e armazena no campo password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # Verifica se a senha fornecida corresponde ao hash armazenado