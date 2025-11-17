"""
멘토링 프로그램 데이터 모델
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class MentoringProgram(BaseModel):
    """멘토링 프로그램"""
    
    program_id: str = Field(..., description="프로그램 ID")
    title: str = Field(..., description="프로그램 제목")
    description: str = Field(..., description="프로그램 설명")
    location: str = Field(..., description="활동 지역")
    activity_type: str = Field(
        ...,
        description="활동 유형 (예: 카페 미팅, 식사, 운동, 문화생활)"
    )
    estimated_cost: int = Field(..., ge=0, description="예상 비용 (원)")
    duration_minutes: int = Field(..., ge=30, description="예상 소요 시간 (분)")
    recommended_for: List[str] = Field(
        ...,
        description="추천 대상 (예: 개발자, 마케터, 디자이너)"
    )
    tags: List[str] = Field(
        default=[],
        description="태그 (예: 실내, 실외, 캐주얼, 포멀)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "program_id": "PROG001",
                "title": "강남 카페에서 커피 한잔하며 커리어 고민 나누기",
                "description": "편안한 카페에서 커피를 마시며 자유롭게 대화하는 멘토링",
                "location": "서울 강남",
                "activity_type": "카페 미팅",
                "estimated_cost": 15000,
                "duration_minutes": 90,
                "recommended_for": ["개발자", "마케터", "기획자"],
                "tags": ["실내", "캐주얼", "대화 중심"]
            }
        }


class RecommendedProgram(BaseModel):
    """추천된 프로그램 (추천 이유 포함)"""
    
    program: MentoringProgram
    match_score: float = Field(..., ge=0, le=100, description="매칭 점수 (0-100)")
    reason: str = Field(..., description="추천 이유")
    
    class Config:
        json_schema_extra = {
            "example": {
                "program": {
                    "program_id": "PROG001",
                    "title": "강남 카페에서 커피 한잔하며 커리어 고민 나누기",
                    "description": "편안한 카페에서 커피를 마시며 자유롭게 대화하는 멘토링",
                    "location": "서울 강남",
                    "activity_type": "카페 미팅",
                    "estimated_cost": 15000,
                    "duration_minutes": 90,
                    "recommended_for": ["개발자"],
                    "tags": ["실내", "캐주얼"]
                },
                "match_score": 95,
                "reason": "멘토와 멘티 모두 카페를 선호하며, 예산과 지역이 적합합니다."
            }
        }

