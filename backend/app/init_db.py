from backend.app.core.database import engine, Base


def init():
    Base.metadata.create_all(bind=engine)
    print("Tables created")

if __name__ == "__main__":
    init()