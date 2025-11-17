"""
멘토 데이터 모델
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class Mentor(BaseModel):
    """멘토 프로필"""
    
    name: str = Field(..., description="멘토 이름")
    age: int = Field(..., ge=20, le=100, description="나이")
    location: str = Field(..., description="거주 지역 (예: 서울, 경기, 부산)")
    job_title: str = Field(..., description="직무/직책 (예: 시니어 개발자, 팀장)")
    experience_years: int = Field(..., ge=0, description="경력 연차")
    expertise: List[str] = Field(..., description="전문 분야 (예: Python, 데이터 분석, 프로젝트 관리)")
    interests: List[str] = Field(..., description="관심사 및 활동 취향 (예: 카페, 등산, 독서)")
    available_days: List[str] = Field(
        default=["월", "화", "수", "목", "금"],
        description="활동 가능 요일"
    )
    preferred_budget: Optional[int] = Field(
        None,
        description="선호하는 활동 예산 (원)"
    )
    introduction: Optional[str] = Field(
        None,
        description="자기소개"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "김멘토",
                "age": 35,
                "location": "서울",
                "job_title": "시니어 소프트웨어 엔지니어",
                "experience_years": 10,
                "expertise": ["Python", "웹 개발", "팀 리딩"],
                "interests": ["카페", "독서", "영화"],
                "available_days": ["월", "수", "금"],
                "preferred_budget": 50000,
                "introduction": "신입 개발자들에게 실무 경험을 공유하고 싶습니다."
            }
        }

