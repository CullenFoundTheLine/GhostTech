# database.py
import os
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ghostai.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class TelemetryFrameDB(Base):
    """
    The stored version of models.py's TelemetryFrame.
    Now includes session context — driver, track, car, weather,
    tires, session type — so frames from different tracks/cars
    never get mixed together during analysis.
    """
    __tablename__ = "telemetry_frames"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    timestamp = Column(DateTime)
    lap = Column(Integer)
    speed_kph = Column(Float)
    rpm = Column(Integer)
    gear = Column(Integer)
    throttle = Column(Float)
    brake = Column(Float)
    pos_x = Column(Float)
    pos_y = Column(Float)
    pos_z = Column(Float)
    tire_fl = Column(Float)
    tire_fr = Column(Float)
    tire_rl = Column(Float)
    tire_rr = Column(Float)

    # Session context columns
    driver = Column(String, index=True)
    track = Column(String, index=True)
    car = Column(String, index=True)
    weather = Column(String)
    tires_compound = Column(String)
    session_type = Column(String)


def init_db():
    """Creates the table on startup if it doesn't exist yet."""
    Base.metadata.create_all(bind=engine)