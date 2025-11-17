"""
멘티 데이터 모델
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class Mentee(BaseModel):
    """멘티 프로필"""
    
    name: str = Field(..., description="멘티 이름")
    age: int = Field(..., ge=18, le=100, description="나이")
    location: str = Field(..., description="거주 지역 (예: 서울, 경기, 부산)")
    job_title: str = Field(..., description="직무/직책 (예: 신입 개발자, 주니어 마케터)")
    experience_years: int = Field(default=0, ge=0, description="경력 연차")
    learning_goals: List[str] = Field(
        ...,
        description="배우고 싶은 것 (예: Python 기초, 커리어 방향성, 업무 스킬)"
    )
    interests: List[str] = Field(
        ...,
        description="관심사 및 활동 취향 (예: 카페, 등산, 게임)"
    )
    available_days: List[str] = Field(
        default=["월", "화", "수", "목", "금"],
        description="활동 가능 요일"
    )
    budget_limit: int = Field(
        ...,
        ge=0,
        description="예산 한도 (원)"
    )
    preferred_mentor_style: Optional[str] = Field(
        None,
        description="선호하는 멘토 스타일 (예: 친근한, 체계적인, 실용적인)"
    )
    introduction: Optional[str] = Field(
        None,
        description="자기소개"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "이멘티",
                "age": 25,
                "location": "서울",
                "job_title": "주니어 개발자",
                "experience_years": 1,
                "learning_goals": ["코드 리뷰 방법", "효율적인 학습법", "커리어 방향성"],
                "interests": ["카페", "운동", "독서"],
                "available_days": ["월", "수", "금"],
                "budget_limit": 30000,
                "preferred_mentor_style": "친근하고 실용적인",
                "introduction": "개발 실력을 키우고 싶은 신입 개발자입니다."
            }
        }

