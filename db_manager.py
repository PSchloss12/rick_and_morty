from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import json, requests
import os

CHARACTER_URL = "https://rickandmortyapi.com/api/character/"
LOCATION_URL = "https://rickandmortyapi.com/api/location/"

# Get the absolute path to the database file (works locally and on Vercel)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "rick.sqlite")

# create an engine for your DB using sqlite and storing it in a file named rick.sqlite
engine = create_engine(
    f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False}
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():  # 15 LOC
    # import your classes that represent tables in the DB and then create_all of the tables
    from rick_classes import Character, Location, Episode

    Base.metadata.create_all(bind=engine)

    js = json.loads(requests.get(CHARACTER_URL).content.decode("utf8"))
    while js["info"]["next"]:
        print(js["info"]["next"])
        js = json.loads(requests.get(js["info"]["next"]).content.decode("utf8"))
        chars = js["results"]
        for char in chars:
            character = Character(
                char["url"],
                char["id"],
                char["name"],
                char["status"],
                char["species"],
                char["type"],
                char["gender"],
                char["origin"]["url"],
                char["location"]["url"],
                char["image"],
                ",".join(i for i in char["episode"]),
            )
            db_session.add(character)

    # save the database
    db_session.commit()

    js = json.loads(requests.get(LOCATION_URL).content.decode("utf8"))
    while js["info"]["next"]:
        print(js["info"]["next"])
        js = json.loads(requests.get(js["info"]["next"]).content.decode("utf8"))
        chars = js["results"]
        for char in chars:
            character = Location(
                char["url"],
                id=char["id"],
                name=char["name"],
                type=char["type"],
                dimension=char["dimension"],
            )
            db_session.add(character)

    # save the database
    db_session.commit()


if __name__ == "__main__":
    from rick_classes import Character

    js = json.loads(requests.get(CHARACTER_URL).content.decode("utf8"))
    pages = js["info"]["pages"]
    print(pages)
    char = js["results"][0]
    character = Character(
        char["url"],
        char["id"],
        char["name"],
        char["status"],
        char["species"],
        char["type"],
        char["gender"],
        char["origin"]["url"],
        char["location"]["url"],
        char["image"],
        ",".join(i for i in char["episode"]),
    )
    print(character.episodes)
    # while js["info"]["next"]:
    #     print(js["info"]["next"])
    #     js = json.loads(requests.get(js["info"]["next"]).content.decode('utf8'))
