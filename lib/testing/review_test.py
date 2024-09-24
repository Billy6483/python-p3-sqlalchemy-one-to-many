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

class TestReview:
    @pytest.fixture(autouse=True)
    def setup(self, session):
        # Add test data
        self.skyrim = Game(
            title="The Elder Scrolls V: Skyrim",
            platform="PC",
            genre="Adventure",
            price=20
        )
        session.add(self.skyrim)
        session.commit()

        self.skyrim_review = Review(
            score=10,
            comment="Wow, what a game",
            game_id=self.skyrim.id
        )

        session.add(self.skyrim_review)
        session.commit()

    def test_review_has_correct_attributes(self):
        assert all(hasattr(self.skyrim_review, attr) for attr in [
            "id", "score", "comment", "game_id"
        ])

    def test_knows_about_associated_game(self):
        assert self.skyrim_review.game == self.skyrim
