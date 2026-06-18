from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Literal


class TelemetryFrame(BaseModel):
    """
    One normalized frame. `source` tells you WHICH platform sent this.
    The session_* fields tell you the CONTEXT it was captured under —
    driver, track, car, weather, tires, session type. Without this,
    Ghost AI can't tell your Nurburgring laps from your Monza laps.
    """
    source: Literal["gt7", "ac", "acc", "iracing", "simhub", "csv"]
    timestamp: datetime
    lap: int
    speed_kph: float
    rpm: int
    gear: int
    throttle: float
    brake: float
    pos_x: float
    pos_y: float
    pos_z: float
    tire_fl: float
    tire_fr: float
    tire_rl: float
    tire_rr: float

    # Session context — same for every frame in one session
    driver: str
    track: str
    car: str
    weather: str
    tires_compound: str
    session_type: str

    @classmethod
    def from_gt7(cls, t, session):
        """
        t is a gt_telem Telemetry object.
        session is a SessionContext from session.py — carries
        driver/track/car/weather/tires/session_type for every frame.
        """
        return cls(
            source="gt7",
            timestamp=datetime.now(),
            lap=t.current_lap,
            speed_kph=t.speed_kph,
            rpm=round(t.engine_rpm),
            gear=t.current_gear,
            throttle=t.throttle,
            brake=t.brake,
            pos_x=round(t.position_x, 2),
            pos_y=round(t.position_y, 2),
            pos_z=round(t.position_z, 2),
            tire_fl=round(t.tire_fl_temp, 1),
            tire_fr=round(t.tire_fr_temp, 1),
            tire_rl=round(t.tire_rl_temp, 1),
            tire_rr=round(t.tire_rr_temp, 1),
            driver=session.driver,
            track=session.track,
            car=session.car,
            weather=session.weather,
            tires_compound=session.tires,
            session_type=session.session_type,
        )