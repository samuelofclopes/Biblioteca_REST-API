from models.user import db
from datetime import datetime, timezone

class Item(db.Model):
    # Modelo de Item (Livro)
    __tablename__ = 'item'
    
    id =                db.Column(db.Integer, primary_key=True) # ID do item, chave primária para procurar os dados
    title =             db.Column(db.String(100), nullable=False) # Título do item
    author =            db.Column(db.String(100), nullable=False) # Autor do item
    total_copies =      db.Column(db.Integer, default=1) # Número total de cópias do item
    available_copies =  db.Column(db.Integer, default=1) # Número de cópias disponíveis do item
    created_at =        db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) # Pega o tempo UTC no momento que é preciso ser usado, ou seja, na criação do item
    
    def __str__(self): # Representação em string do item (útil para debug)
        return f'<Item {self.title}>'
    
    def is_available(self):
        return self.available_copies > 0