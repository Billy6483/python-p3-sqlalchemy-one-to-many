import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Game, Review
from conftest import SQLITE_URL

@pytest.fixture(scope='module')
def test_db():
    engine = create_engine(SQLITE_URL)
    Base.metadata.create_all(engine)  # Create tables
    connection = engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()

@pytest.fixture()
def session(test_db):
    Session = sessionmaker(bind=test_db)
    session = Session()
    yield session
    session.close()

class TestGame:
    @pytest.fixture(autouse=True)
    def setup(self, session):
        # Add test data
        self.mario_kart = Game(
            title="Mario Kart",
            platform="Switch",
            genre="Racing",
            price=60
        )
        session.add(self.mario_kart)
        session.commit()

        self.mk_review_1 = Review(
            score=10,
            comment="Wow, what a game",
            game_id=self.mario_kart.id
        )

        self.mk_review_2 = Review(
            score=8,
            comment="A classic",
            game_id=self.mario_kart.id
        )

        session.add(self.mk_review_1)
        session.add(self.mk_review_2)
        session.commit()

    def test_game_has_correct_attributes(self):
        assert all(hasattr(self.mario_kart, attr) for attr in [
            "id", "title", "platform", "genre", "price"
        ])

    def test_has_associated_reviews(self):
        assert len(self.mario_kart.reviews) == 2
        assert self.mario_kart.reviews[0].score == 10
        assert self.mario_kart.reviews[1].score == 8
