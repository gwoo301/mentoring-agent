"""
멘토링 매칭 서비스 (규칙 기반)
"""

import json
from typing import List, Set
from pathlib import Path

from models import Mentor, Mentee, MentoringProgram
from models.program import RecommendedProgram


class MatchingService:
    """멘토링 매칭 서비스 (규칙 기반 알고리즘)"""
    
    def __init__(self):
        self.programs: List[MentoringProgram] = []
    
    def load_programs_from_file(self, file_path: str):
        """JSON 파일에서 프로그램 목록 로드"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"프로그램 파일을 찾을 수 없습니다: {file_path}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.programs = [MentoringProgram(**program) for program in data]
        
        print(f"✅ {len(self.programs)}개의 프로그램을 로드했습니다.")
    
    def add_program(self, program: MentoringProgram):
        """프로그램 추가"""
        self.programs.append(program)
    
    def _calculate_match_score(
        self,
        program: MentoringProgram,
        mentor: Mentor,
        mentee: Mentee
    ) -> tuple[float, str]:
        """
        프로그램의 매칭 점수 계산 (규칙 기반)
        
        Returns:
            (점수, 추천 이유)
        """
        score = 0.0
        reasons = []
        
        # 1. 지역 매칭 (30점)
        if program.location in mentor.location or program.location in mentee.location:
            score += 30
            reasons.append(f"✓ 지역이 적합합니다 ({program.location})")
        elif "전역" in program.location:
            score += 25
            reasons.append(f"✓ 지역 제약이 없습니다")
        else:
            score += 10
            reasons.append(f"△ 지역이 다소 다릅니다")
        
        # 2. 예산 적합성 (25점)
        if program.estimated_cost <= mentee.budget_limit:
            # 예산 대비 비용이 적절할수록 높은 점수
            budget_ratio = program.estimated_cost / mentee.budget_limit
            if budget_ratio <= 0.5:
                score += 25
                reasons.append(f"✓ 예산 대비 매우 저렴합니다 ({program.estimated_cost:,}원)")
            elif budget_ratio <= 0.8:
                score += 20
                reasons.append(f"✓ 예산 범위 내 적정 가격입니다 ({program.estimated_cost:,}원)")
            else:
                score += 15
                reasons.append(f"✓ 예산 내에서 가능합니다 ({program.estimated_cost:,}원)")
        
        # 3. 관심사 일치도 (30점)
        mentor_interests = set(mentor.interests)
        mentee_interests = set(mentee.interests)
        common_interests = mentor_interests & mentee_interests
        
        # 프로그램의 활동 유형과 관심사 매칭
        activity_keywords = program.activity_type.lower() + " " + " ".join(program.tags).lower()
        matching_interests = []
        
        for interest in common_interests:
            if interest.lower() in activity_keywords or any(
                interest.lower() in tag.lower() for tag in program.tags
            ):
                matching_interests.append(interest)
        
        if matching_interests:
            score += 30
            reasons.append(f"✓ 공통 관심사와 일치합니다: {', '.join(matching_interests)}")
        elif common_interests:
            score += 20
            reasons.append(f"✓ 멘토와 멘티의 공통 관심사가 있습니다: {', '.join(list(common_interests)[:2])}")
        else:
            # 개별 관심사라도 매칭되는지 확인
            all_interests = mentor_interests | mentee_interests
            matched = [i for i in all_interests if i.lower() in activity_keywords]
            if matched:
                score += 15
                reasons.append(f"△ 일부 관심사와 연관됩니다: {', '.join(matched[:2])}")
            else:
                score += 5
                reasons.append(f"△ 새로운 경험이 될 수 있습니다")
        
        # 4. 직무 적합성 (15점)
        job_match = False
        for job_type in program.recommended_for:
            if job_type in mentor.job_title or job_type in mentee.job_title:
                job_match = True
                break
        
        if job_match or "모든 직군" in program.recommended_for:
            score += 15
            reasons.append(f"✓ 직무에 적합한 활동입니다")
        else:
            score += 8
            reasons.append(f"△ 모든 직군에 열려있습니다")
        
        # 점수 정규화 (0-100)
        final_score = min(100, score)
        reason_text = " | ".join(reasons)
        
        return final_score, reason_text
    
    def find_matches(
        self,
        mentor: Mentor,
        mentee: Mentee,
        top_k: int = 5
    ) -> List[RecommendedProgram]:
        """
        멘토와 멘티에게 적합한 프로그램 추천 (규칙 기반)
        
        Args:
            mentor: 멘토 프로필
            mentee: 멘티 프로필
            top_k: 추천할 프로그램 개수
        
        Returns:
            추천된 프로그램 목록 (점수 순으로 정렬)
        """
        
        if not self.programs:
            raise ValueError("추천할 프로그램이 없습니다. 먼저 프로그램을 로드해주세요.")
        
        print(f"\n🔍 {mentor.name}(멘토)와 {mentee.name}(멘티)를 위한 프로그램을 분석 중...")
        
        # 멘티 예산 내의 프로그램만 필터링
        affordable_programs = [
            p for p in self.programs
            if p.estimated_cost <= mentee.budget_limit
        ]
        
        if not affordable_programs:
            print(f"⚠️  예산({mentee.budget_limit:,}원) 내의 프로그램이 없습니다.")
            return []
        
        print(f"💰 예산 내 프로그램: {len(affordable_programs)}개")
        
        # 각 프로그램의 점수 계산
        scored_programs = []
        for program in affordable_programs:
            score, reason = self._calculate_match_score(program, mentor, mentee)
            scored_programs.append({
                "program": program,
                "score": score,
                "reason": reason
            })
        
        # 점수 순으로 정렬
        scored_programs.sort(key=lambda x: x["score"], reverse=True)
        
        # 상위 top_k개 선택
        top_programs = scored_programs[:top_k]
        
        # RecommendedProgram 객체로 변환
        results = [
            RecommendedProgram(
                program=item["program"],
                match_score=item["score"],
                reason=item["reason"]
            )
            for item in top_programs
        ]
        
        print(f"✨ 상위 {len(results)}개 프로그램을 추천합니다!")
        
        return results

