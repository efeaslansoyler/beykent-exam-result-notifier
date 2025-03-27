from dataclasses import dataclass

@dataclass
class Result:
    lesson_id: str
    lesson_name: str
    exam_type: str
    score: float