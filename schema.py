from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship

Base = declarative_base()


leagueplayers_table = Table("leagueplayers", Base.metadata,
    Column("league_id", Integer, ForeignKey("league.id")),
    Column("player_id", Integer, ForeignKey("player.id")),
)

teamplayers_table = Table("teamplayers", Base.metadata,
    Column("team_id", Integer, ForeignKey("team.id")),
    Column("player_id", Integer, ForeignKey("player.id")),
)


teamcaptains_table = Table("teamcaptains", Base.metadata,
    Column("team_id", Integer, ForeignKey("team.id")),
    Column("player_id", Integer, ForeignKey("player.id")),
)


matchplayers_table = Table("matchplayers", Base.metadata,
    Column("match_id", Integer, ForeignKey("match.id")),
    Column("player_id", Integer, ForeignKey("player.id")),
)


gamedecks_table = Table("gamedecks", Base.metadata,
    Column("game_id", Integer, ForeignKey("game.id")),
    Column("deckchoice_id", Integer, ForeignKey("deckchoice.id")),
)


class League(Base):
    __tablename__ = "league"
    id = Column(Integer, primary_key=True)
    players = relationship(
        "Player",
        secondary=leagueplayers_table,
        backref="leagues",
    )
    name = Column(String)
    description = Column(String)
    weeks = relationship("Week")
    teams = relationship("Team")


class Week(Base):
    __tablename__ = "week"
    id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey("league.id"))
    deck_choices = relationship("DeckChoice", backref="week")
    matches = relationship("Match", backref="week")
    name = Column(String)
    submission_opens = Column(DateTime)
    submission_closes = Column(DateTime)
    results_opens = Column(DateTime)
    results_closes = Column(DateTime)
    restrictions = Column(String)
    variant = Column(String)


class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey("league.id"))
    players = relationship(
        "Player",
        secondary=teamplayers_table,
        backref="team",
    )
    captains = relationship(
        "Player",
        secondary=teamcaptains_table,
    )
    name = Column(String, nullable=False)


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)
    deck_choices = relationship(
        "DeckChoice",
        back_populates="player",
        foreign_keys="DeckChoice.player_id",
    )
    dok_user = Column(String)
    discord_user = Column(String)
    email = Column(String)
    tco_user = Column(String)


class DeckChoice(Base):
    __tablename__ = "deckchoice"
    id = Column(Integer, primary_key=True)
    week_id = Column(Integer, ForeignKey("week.id"))
    player_id = Column(Integer, ForeignKey("player.id"))
    player = relationship(
        "Player",
        back_populates="deck_choices",
        foreign_keys=[player_id],
    )
    verified_by_id = Column(Integer, ForeignKey("player.id"))
    deck_id = Column(String)
    name = Column(String)


class Match(Base):
    __tablename__ = "match"
    id = Column(Integer, primary_key=True)
    week_id = Column(Integer, ForeignKey("week.id"))
    players = relationship(
        "Player",
        secondary=matchplayers_table,
        backref="matches",
    )
    games = relationship("Game", backref="match")
    winner_id = Column(Integer, ForeignKey("player.id"))
    winner = relationship("Player", foreign_keys=[winner_id])
    variant = Column(String)


class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("match.id"))
    winner_id = Column(Integer, ForeignKey("player.id"))
    winner = relationship("Player", foreign_keys=[winner_id])
    deckchoices = relationship(
        "DeckChoice",
        secondary=gamedecks_table,
        backref="games",
    )
    first_player_id = Column(Integer, ForeignKey("player.id"))
    first_player = relationship("Player", foreign_keys=[first_player_id])
    tracker_link = Column(String)
    chains = Column(Integer)
    reversal = Column(Boolean)
