from pydantic import BaseModel


class SegmentPhoto(BaseModel):
    area: float
    age: int
    tur1h: float
    leaves: float
    conifer: float
    without_trees: float


class TrainModel(BaseModel):
    photo_path: str
    label: int