# session.py
# Captures session context BEFORE the receiver starts pulling frames.
# This answers: what game, what track, what car, what conditions —
# so every frame stored in the database carries that context with it.

PLATFORMS = ["gt7", "ac", "acc", "iracing", "simhub", "csv"]

CATEGORIES = ["Formula", "GrandTouring", "Prototype", "TouringCar", "Drift", "Rally", "Sim"]

CARS = {
    "Formula":      ["F1", "F2", "F3", "IndyCar", "Formula E"],
    "GrandTouring": ["GT3", "GT4", "GT500"],
    "Prototype":    ["Hypercar", "LMDh", "LMP2"],
    "TouringCar":   ["TCR", "BTCC", "DTM"],
    "Drift":        ["Formula Drift", "D1GP"],
    "Rally":        ["WRC Rally1", "WRC Rally2"],
    "Sim":          ["GT7", "iRacing", "Assetto Corsa", "F1 25"],
}

TRACKS = [
    "Monaco", "Silverstone", "Spa-Francorchamps", "Monza", "Suzuka",
    "Interlagos", "Nurburgring", "Le Mans", "Daytona", "Laguna Seca",
    "Road Atlanta", "Long Beach", "Irwindale", "Trial Mountain",
    "Deep Forest", "Tokyo Expressway", "Sardegna", "Other"
]

WEATHER = ["Dry", "Wet", "Mixed"]
TIRES   = ["Sport", "Racing", "Rain", "Comfort"]
SESSION_TYPES = ["Practice", "Qualifying", "Race", "Time Trial", "Drift"]


class SessionContext:
    """
    Holds everything that should be attached to every frame
    captured during one driving session.
    """

    def __init__(self, driver, platform, track, car, weather, tires, session_type):
        self.driver       = driver
        self.platform     = platform
        self.track        = track
        self.car          = car
        self.weather      = weather
        self.tires        = tires
        self.session_type = session_type

    def to_dict(self):
        return {
            "driver":       self.driver,
            "platform":     self.platform,
            "track":        self.track,
            "car":          self.car,
            "weather":      self.weather,
            "tires":        self.tires,
            "session_type": self.session_type,
        }

    def summary(self):
        print("\n--- SESSION ---")
        for key, value in self.to_dict().items():
            print(f"  {key}: {value}")
        print("---------------\n")


def _pick(options, label):
    print(f"\n  {label}:")
    for i, opt in enumerate(options):
        print(f"    {i + 1}. {opt}")
    choice = int(input("  Pick number: ")) - 1
    return options[choice]


def setup():
    """
    Asks the driver for session context before the receiver starts.
    Returns a SessionContext object, or None if cancelled.
    """
    print("\n--- GHOSTTECH SESSION SETUP ---\n")

    driver   = input("  Driver name: ").strip()
    platform = _pick(PLATFORMS, "Platform")
    category = _pick(CATEGORIES, "Racing category")
    car      = _pick(CARS[category], f"Car ({category})")
    track    = _pick(TRACKS, "Track")
    weather  = _pick(WEATHER, "Weather")
    tires    = _pick(TIRES, "Tires")
    stype    = _pick(SESSION_TYPES, "Session type")

    session = SessionContext(
        driver=driver,
        platform=platform,
        track=track,
        car=car,
        weather=weather,
        tires=tires,
        session_type=stype,
    )
    session.summary()

    confirm = input("  Start capturing? (yes / no): ").strip().lower()
    if confirm != "yes":
        print("\n  Session cancelled.\n")
        return None

    return session


if __name__ == "__main__":
    s = setup()
    if s:
        print("Session ready:")
        print(s.to_dict())