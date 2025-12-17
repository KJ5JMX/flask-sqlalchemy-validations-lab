from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()


ALLOWED_KEYWORDS = [
    "won't believe",
    "secret",
    "top",
    "guess"
]

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number is None:
            return phone_number
        

       
        if not phone_number.isdigit() or len(phone_number) != 10:
             raise ValueError("Phone number must be exactly 10 digits")
    

        return phone_number
    
    @validates('name')
    def validate_name(self, key, name):
       if not name or not name.strip():
           raise ValueError("Name is required")
       

       name = name.strip()

       existing_author = Author.query.filter_by(name=name).first()
       if existing_author:
             raise ValueError("Author name must be unique")
       
       return name


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError("Content must be at least 250 characters long")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary must be at most 250 characters long")
        return summary 
    
    @validates('category')
    def validate_category(self, key, category):
        allowed_categories = ['Fiction', 'Non-Fiction']
        if category not in allowed_categories:
            raise ValueError(f"Category must be one of {allowed_categories}")
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError("Title is required")
        
        lower_title = title.lower()

        if not any(keyword in lower_title for keyword in ALLOWED_KEYWORDS):
            raise ValueError(
            'Title must contain "Won\'t Believe", "Secret", "Top", or "Guess"'
        )

        return title.strip()
        


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
