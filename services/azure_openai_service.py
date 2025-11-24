"""
Azure OpenAI 연동 서비스
"""

import os
import json
from typing import List, Dict, Any
from openai import AzureOpenAI
from dotenv import load_dotenv


class AzureOpenAIService:
    """Azure OpenAI를 사용한 LLM 서비스"""
    
    def __init__(self):
        load_dotenv()
        
        # Azure OpenAI 설정
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        if not self.api_key or not self.endpoint:
            raise ValueError(
                "Azure OpenAI 설정이 누락되었습니다. "
                ".env 파일에 AZURE_OPENAI_API_KEY와 AZURE_OPENAI_ENDPOINT를 추가해주세요."
            )
        
        # Azure OpenAI 클라이언트 초기화
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )
    
    def generate_recommendations(
        self,
        mentor_profile: Dict[str, Any],
        mentee_profile: Dict[str, Any],
        available_programs: List[Dict[str, Any]],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        멘토와 멘티 프로필을 기반으로 적합한 프로그램을 추천합니다.
        
        Args:
            mentor_profile: 멘토 프로필 정보
            mentee_profile: 멘티 프로필 정보
            available_programs: 사용 가능한 프로그램 목록
            top_k: 추천할 프로그램 개수
        
        Returns:
            추천된 프로그램 목록 (점수 및 이유 포함)
        """
        
        # 프롬프트 생성
        prompt = self._create_recommendation_prompt(
            mentor_profile,
            mentee_profile,
            available_programs,
            top_k
        )
        
        try:
            # Azure OpenAI API 호출
            response = self.client.chat.completions.create(
                model=self.deployment_name,  # 배포 이름 사용
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "당신은 멘토링 매칭 전문가입니다. "
                            "멘토와 멘티의 프로필을 깊이 분석하여 "
                            "가장 적합한 멘토링 프로그램을 추천해주세요. "
                            "지역, 예산, 관심사, 활동 취향, 직무 적합성을 모두 고려해야 합니다. "
                            "추천 이유는 구체적이고 설득력 있게 작성해주세요."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            # 응답 파싱
            result = json.loads(response.choices[0].message.content)
            return result.get("recommendations", [])
            
        except Exception as e:
            print(f"Azure OpenAI API 호출 중 오류 발생: {e}")
            raise
    
    def _create_recommendation_prompt(
        self,
        mentor_profile: Dict[str, Any],
        mentee_profile: Dict[str, Any],
        available_programs: List[Dict[str, Any]],
        top_k: int
    ) -> str:
        """추천 프롬프트 생성"""
        
        prompt = f"""
다음 멘토와 멘티를 위한 최적의 멘토링 프로그램을 추천해주세요.

## 멘토 프로필
{json.dumps(mentor_profile, ensure_ascii=False, indent=2)}

## 멘티 프로필
{json.dumps(mentee_profile, ensure_ascii=False, indent=2)}

## 사용 가능한 프로그램 목록
{json.dumps(available_programs, ensure_ascii=False, indent=2)}

## 요구사항
1. 상위 {top_k}개의 프로그램을 추천해주세요
2. 각 추천에 대해 다음을 고려하세요:
   - 멘티의 예산 한도 (budget_limit) 이내인가?
   - 지역이 적합한가? (멘토/멘티 거주 지역과의 접근성)
   - 멘토와 멘티의 관심사(interests)가 일치하는가?
   - 활동 유형이 두 사람 모두에게 적합한가?
   - 멘티의 학습 목표(learning_goals)와 프로그램이 연관되는가?
   - 멘토의 전문성(expertise)을 활용할 수 있는가?
3. 각 프로그램에 대해:
   - 매칭 점수(0-100): 높을수록 적합
   - 추천 이유: 구체적이고 설득력 있게 (2-3문장)

## 출력 형식 (JSON)
반드시 다음 형식으로 응답해주세요:

{{
  "recommendations": [
    {{
      "program_id": "프로그램 ID",
      "match_score": 95,
      "reason": "이 프로그램은 멘토와 멘티 모두 카페를 선호하며, 예산 범위 내에서 개발자 직무에 최적화된 활동입니다. 멘토의 코드 리뷰 전문성을 활용하여 멘티의 학습 목표인 '클린 코드 작성'에 직접적으로 도움이 될 것입니다."
    }},
    {{
      "program_id": "프로그램 ID",
      "match_score": 88,
      "reason": "추천 이유..."
    }}
  ]
}}

매칭 점수는 높은 순으로 정렬해주세요.
"""
        return prompt

