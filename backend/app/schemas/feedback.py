from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    collection_id: int
    stars: int
    comment: str = ""
