from . import create_app
from . import db
from .models.users import User
import bcrypt

app = create_app()

with app.app_context():

    hashed_pw = bcrypt.hashpw(
        "admin123".encode(),
        bcrypt.gensalt()
    ).decode()

    admin = User(
        username="admin",
        email="admin@email.com",
        password=hashed_pw,
        role="admin"
    )

    db.session.add(admin)
    db.session.commit()

    print("Admin created")