# course.py
from typing import List, Optional

from pydantic import BaseModel, Field


# TODO for student: Convert this to Pydantic
# TODO for student: Make sure to add a small description, like I did in the comments. You can do that by adapting the Field... . Search the Pydantic documentation for this.
class Course(BaseModel):
    title: str = Field(
        "MLOps", description="The name of the Course, also my name is here! 👋 Cedric Hermans")  # e.g.: "MLOps"
    semester: int = Field(
        5, description="The semester the course is taught in. As there are 2 semesters in one year, semester 5 means --> Year 3, semester 1")  # e.g.: 5 --> Year 3, semester 1
    weight: int  # e.g.: 10 (where to be in a sorted array)
    # e.g.: ["Kubernetes", "CI/CD", "AutomatedAI"]
    tags: List[str]
    # e.g.: "code" --> The MCT pillar to classify this course in.
    pillar: str
    # e.g.: ["ai-engineer"] --> The MCT tracks this course is taught in

    preview: str  # e.g.: "In de module MLOps leren we AI modellen deployen."
    basename: str  # e.g.: "mlops" A short name
    tracks: Optional[List[str]]
