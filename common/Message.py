class Message:
    identifier: str
    timestamp: float
    signal_strength: float

    def __init__(self, identifier: str, timestamp: float, signal_strength: float):
        self.identifier = identifier
        self.timestamp = timestamp
        self.signal_strength = signal_strength
