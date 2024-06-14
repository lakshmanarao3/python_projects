from app import app, db
from app.models import User

def create_db():
    with app.app_context():
        db.create_all()
        if not User.query.first():
            user = User(username='John Doe', email='john@example.com')
            db.session.add(user)
            db.session.commit()

if __name__ == '__main__':
    create_db()
    app.run(host='0.0.0.0', port=5000)
