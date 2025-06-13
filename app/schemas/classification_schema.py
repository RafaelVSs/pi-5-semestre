from pydantic import BaseModel

class PlayerStatsInput(BaseModel):
    position: str
    points_per_game: float
    assists_per_game: float
    rebounds_per_game: float

class ClassificationResult(BaseModel):
    player_name: str
    classification: str
    message: str