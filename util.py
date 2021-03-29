import configparser
from schema import (
    Base,
    DeckChoice,
    Game,
    League,
    Match,
    Player,
    Team,
    Week,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    Session,
)


def read_config(path: str) -> configparser.ConfigParser:
    cparser = configparser.ConfigParser()
    cparser.read(path)
    return cparser


class SessionFactory:
    def __init__(
        self,
        host: str = "localhost",
        port: int = None,
        user: str = None,
        password: str = None,
        database: str = "teamforge",
    ):
        driver = "postgresql"
        uri_bits = [driver, "://"]
        if user is not None:
            uri_bits.append(user)
            if password is not None:
                uri_bits.append(":")
                uri_bits.append(password)
        uri_bits.append("@")
        uri_bits.append(host)
        if port is not None:
            uri_bits.append(":")
            uri_bits.append(port)
        uri_bits.append("/")
        uri_bits.append(database)
        self.uri = "".join(uri_bits)

    def __call__(self) -> Session:
        engine = create_engine(self.uri, echo=False)
        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        return scoped_session(session_factory)()


def create_test_data(session: Session):
    league = League(name="Test League", description="Fake league for testing")
