#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
신입사원 멘토링 매칭 Agent - 메인 실행 파일
"""

import sys
import io

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
from pathlib import Path
from models import Mentor, Mentee, MentoringProgram
from services import MatchingService


def load_mentors_from_file(file_path: str) -> list[Mentor]:
    """JSON 파일에서 멘토 목록 로드"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"멘토 파일을 찾을 수 없습니다: {file_path}")
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Mentor(**mentor) for mentor in data]


def load_mentees_from_file(file_path: str) -> list[Mentee]:
    """JSON 파일에서 멘티 목록 로드"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"멘티 파일을 찾을 수 없습니다: {file_path}")
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Mentee(**mentee) for mentee in data]


def print_separator():
    """구분선 출력"""
    print("\n" + "="*80 + "\n")


def print_recommendations(recommendations):
    """추천 결과 출력"""
    if not recommendations:
        print("❌ 추천 가능한 프로그램이 없습니다.")
        return
    
    print(f"\n✨ 총 {len(recommendations)}개의 프로그램을 추천합니다!\n")
    
    for idx, rec in enumerate(recommendations, 1):
        program = rec.program
        print(f"【 추천 {idx} 】")
        print(f"📌 제목: {program.title}")
        print(f"📍 위치: {program.location}")
        print(f"🎯 활동: {program.activity_type}")
        print(f"💰 비용: {program.estimated_cost:,}원")
        print(f"⏱️  소요시간: {program.duration_minutes}분")
        print(f"⭐ 매칭 점수: {rec.match_score}/100")
        print(f"💡 추천 이유:")
        print(f"   {rec.reason}")
        print(f"📝 설명: {program.description}")
        print(f"🏷️  태그: {', '.join(program.tags)}")
        print_separator()


def example_scenario_1(use_ai: bool = False):
    """시나리오 1: 개발자 멘토-멘티 (카페 선호)"""
    
    print("\n🎬 시나리오 1: 개발자 멘토-멘티 매칭 (카페 선호)")
    print_separator()
    
    # JSON 파일에서 프로필 로드
    mentors = load_mentors_from_file("data/sample_mentors.json")
    mentees = load_mentees_from_file("data/sample_mentees.json")
    
    # 첫 번째 멘토와 첫 번째 멘티 사용
    mentor = mentors[0]  # 김시니어
    mentee = mentees[0]  # 이주니어
    
    print(f"👨‍💼 멘토: {mentor.name} ({mentor.job_title}, 경력 {mentor.experience_years}년)")
    print(f"   관심사: {', '.join(mentor.interests)}")
    print(f"\n👨‍🎓 멘티: {mentee.name} ({mentee.job_title}, 경력 {mentee.experience_years}년)")
    print(f"   관심사: {', '.join(mentee.interests)}")
    print(f"   예산: {mentee.budget_limit:,}원")
    
    # 매칭 실행
    matching_service = MatchingService(use_ai=use_ai)
    matching_service.load_programs_from_file("data/sample_programs.json")
    
    recommendations = matching_service.find_matches(
        mentor=mentor,
        mentee=mentee,
        top_k=3
    )
    
    print_recommendations(recommendations)


def example_scenario_2(use_ai: bool = False):
    """시나리오 2: 다양한 관심사 (운동, 문화생활)"""
    
    print("\n🎬 시나리오 2: 다양한 관심사 매칭 (운동, 문화생활)")
    print_separator()
    
    # JSON 파일에서 프로필 로드
    mentors = load_mentors_from_file("data/sample_mentors.json")
    mentees = load_mentees_from_file("data/sample_mentees.json")
    
    # 두 번째 멘토와 두 번째 멘티 사용
    mentor = mentors[1]  # 박팀장
    mentee = mentees[1]  # 최신입
    
    print(f"👨‍💼 멘토: {mentor.name} ({mentor.job_title}, 경력 {mentor.experience_years}년)")
    print(f"   관심사: {', '.join(mentor.interests)}")
    print(f"\n👨‍🎓 멘티: {mentee.name} ({mentee.job_title}, 경력 {mentee.experience_years}년)")
    print(f"   관심사: {', '.join(mentee.interests)}")
    print(f"   예산: {mentee.budget_limit:,}원")
    
    # 매칭 실행
    matching_service = MatchingService(use_ai=use_ai)
    matching_service.load_programs_from_file("data/sample_programs.json")
    
    recommendations = matching_service.find_matches(
        mentor=mentor,
        mentee=mentee,
        top_k=3
    )
    
    print_recommendations(recommendations)


def display_mentors(mentors: list[Mentor]) -> None:
    """멘토 목록 표시"""
    print("\n👥 사용 가능한 멘토 목록:")
    print("="*80)
    for idx, mentor in enumerate(mentors):
        print(f"[{idx}] {mentor.name} - {mentor.job_title} (경력 {mentor.experience_years}년)")
        print(f"    관심사: {', '.join(mentor.interests)}")
        print(f"    전문분야: {', '.join(mentor.expertise[:3])}")
        print()


def display_mentees(mentees: list[Mentee]) -> None:
    """멘티 목록 표시"""
    print("\n👤 사용 가능한 멘티 목록:")
    print("="*80)
    for idx, mentee in enumerate(mentees):
        print(f"[{idx}] {mentee.name} - {mentee.job_title} (경력 {mentee.experience_years}년)")
        print(f"    관심사: {', '.join(mentee.interests)}")
        print(f"    예산: {mentee.budget_limit:,}원")
        print(f"    학습 목표: {', '.join(mentee.learning_goals[:2])}")
        print()


def get_valid_input(prompt: str, max_value: int) -> int:
    """유효한 정수 입력 받기"""
    while True:
        try:
            value = input(prompt)
            value_int = int(value)
            if 0 <= value_int < max_value:
                return value_int
            else:
                print(f"⚠️  0부터 {max_value - 1} 사이의 숫자를 입력하세요.")
        except ValueError:
            print("⚠️  올바른 숫자를 입력하세요.")
        except KeyboardInterrupt:
            print("\n\n프로그램을 종료합니다.")
            exit(0)


def interactive_mode(use_ai: bool = False):
    """대화형 모드 - 사용자가 직접 멘토와 멘티를 선택"""
    print("\n" + "="*80)
    print(" 💬 대화형 매칭 모드 ")
    print("="*80)
    
    try:
        # 1. 데이터 로드
        mentors = load_mentors_from_file("data/sample_mentors.json")
        mentees = load_mentees_from_file("data/sample_mentees.json")
        
        # 2. 멘토 선택
        display_mentors(mentors)
        mentor_idx = get_valid_input(
            f"멘토를 선택하세요 (0-{len(mentors)-1}): ",
            len(mentors)
        )
        mentor = mentors[mentor_idx]
        print(f"\n✅ 선택된 멘토: {mentor.name} ({mentor.job_title})")
        
        # 3. 멘티 선택
        display_mentees(mentees)
        mentee_idx = get_valid_input(
            f"멘티를 선택하세요 (0-{len(mentees)-1}): ",
            len(mentees)
        )
        mentee = mentees[mentee_idx]
        print(f"\n✅ 선택된 멘티: {mentee.name} ({mentee.job_title})")
        
        # 4. 매칭 실행
        print_separator()
        print(f"🎯 {mentor.name}(멘토)와 {mentee.name}(멘티)의 매칭 분석")
        print_separator()
        
        print(f"👨‍💼 멘토: {mentor.name} ({mentor.job_title}, 경력 {mentor.experience_years}년)")
        print(f"   관심사: {', '.join(mentor.interests)}")
        print(f"\n👨‍🎓 멘티: {mentee.name} ({mentee.job_title}, 경력 {mentee.experience_years}년)")
        print(f"   관심사: {', '.join(mentee.interests)}")
        print(f"   예산: {mentee.budget_limit:,}원")
        
        # 5. 추천 프로그램 찾기
        matching_service = MatchingService(use_ai=use_ai)
        matching_service.load_programs_from_file("data/sample_programs.json")
        
        recommendations = matching_service.find_matches(
            mentor=mentor,
            mentee=mentee,
            top_k=5
        )
        
        print_recommendations(recommendations)
        
        # 6. 다시 실행 여부
        print("\n" + "="*80)
        retry = input("\n다른 조합으로 다시 시도하시겠습니까? (y/n): ").strip().lower()
        if retry == 'y' or retry == 'yes':
            interactive_mode(use_ai=use_ai)  # 재귀 호출
        else:
            print("\n✅ 프로그램을 종료합니다. 감사합니다!")
            
    except FileNotFoundError as e:
        print(f"\n❌ 파일을 찾을 수 없습니다: {e}")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


def main():
    """메인 함수"""
    print("="*80)
    print(" 🎯 신입사원 멘토링 매칭 Agent ")
    print("="*80)
    
    print("\n이 프로그램은 멘토와 멘티의 프로필을 분석하여")
    print("최적의 멘토링 프로그램을 추천합니다.")
    print("(지역, 예산, 관심사 등을 종합적으로 고려합니다)\n")
    
    # 매칭 방식 선택
    print("매칭 방식을 선택하세요:")
    print("1. 🤖 AI 기반 (Azure OpenAI) - 더 정교한 분석")
    print("2. 📊 규칙 기반 (점수 계산) - 빠르고 예측 가능")
    
    try:
        mode_choice = input("\n선택 (1/2): ").strip()
        
        if mode_choice == "1":
            use_ai = True
            print("\n✨ AI 기반 매칭 모드를 선택했습니다!")
        elif mode_choice == "2":
            use_ai = False
            print("\n📊 규칙 기반 매칭 모드를 선택했습니다!")
        else:
            print("\n⚠️  잘못된 선택입니다. 규칙 기반 모드로 진행합니다.")
            use_ai = False
        
        print()
        
        # 실행 모드 선택
        print("실행 모드를 선택하세요:")
        print("1. 대화형 모드 (직접 멘토/멘티 선택)")
        print("2. 예시 시나리오 실행 (자동)")
        print("3. 종료")
        
        choice = input("\n선택 (1/2/3): ").strip()
        
        if choice == "1":
            interactive_mode(use_ai=use_ai)
        elif choice == "2":
            example_scenario_1(use_ai=use_ai)
            example_scenario_2(use_ai=use_ai)
            print("\n✅ 모든 시나리오 실행 완료!")
        elif choice == "3":
            print("\n프로그램을 종료합니다. 👋")
        else:
            print("\n⚠️  잘못된 선택입니다. 1, 2, 3 중 하나를 입력하세요.")
            main()  # 재귀 호출
        
    except KeyboardInterrupt:
        print("\n\n프로그램을 종료합니다. 👋")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

