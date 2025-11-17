#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
신입사원 멘토링 매칭 Agent - Streamlit 웹 애플리케이션
"""

import streamlit as st
import json
from pathlib import Path
from models import Mentor, Mentee
from services import MatchingService


# 페이지 설정
st.set_page_config(
    page_title="멘토링 매칭 Agent",
    page_icon="🎯",
    layout="wide"
)


@st.cache_data
def load_mentors():
    """멘토 데이터 로드 (캐싱)"""
    with open("data/sample_mentors.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Mentor(**mentor) for mentor in data]


@st.cache_data
def load_mentees():
    """멘티 데이터 로드 (캐싱)"""
    with open("data/sample_mentees.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Mentee(**mentee) for mentee in data]


def main():
    """메인 애플리케이션"""
    
    # 헤더
    st.title("🎯 신입사원 멘토링 매칭 Agent")
    st.markdown("---")
    st.markdown("""
    이 시스템은 멘토와 멘티의 프로필을 분석하여 최적의 멘토링 프로그램을 추천합니다.  
    **지역, 예산, 관심사, 직무**를 종합적으로 고려한 규칙 기반 알고리즘을 사용합니다.
    """)
    
    # 데이터 로드
    try:
        mentors = load_mentors()
        mentees = load_mentees()
    except Exception as e:
        st.error(f"❌ 데이터 로드 실패: {e}")
        return
    
    # 사이드바: 멘토/멘티 선택
    st.sidebar.header("👥 프로필 선택")
    
    # 멘토 선택
    st.sidebar.subheader("멘토 선택")
    mentor_options = [f"{m.name} - {m.job_title}" for m in mentors]
    selected_mentor_idx = st.sidebar.selectbox(
        "멘토를 선택하세요:",
        range(len(mentors)),
        format_func=lambda x: mentor_options[x]
    )
    mentor = mentors[selected_mentor_idx]
    
    # 멘티 선택
    st.sidebar.subheader("멘티 선택")
    mentee_options = [f"{m.name} - {m.job_title}" for m in mentees]
    selected_mentee_idx = st.sidebar.selectbox(
        "멘티를 선택하세요:",
        range(len(mentees)),
        format_func=lambda x: mentee_options[x]
    )
    mentee = mentees[selected_mentee_idx]
    
    # 추천 개수 선택
    st.sidebar.subheader("⚙️ 설정")
    top_k = st.sidebar.slider("추천 프로그램 개수", 1, 10, 5)
    
    # 매칭 버튼
    if st.sidebar.button("🔍 매칭 시작", type="primary", use_container_width=True):
        st.session_state['run_matching'] = True
    
    # 선택된 프로필 표시
    st.markdown("---")
    st.header("📋 선택된 프로필")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👨‍💼 멘토")
        st.markdown(f"**이름**: {mentor.name}")
        st.markdown(f"**직책**: {mentor.job_title}")
        st.markdown(f"**경력**: {mentor.experience_years}년")
        st.markdown(f"**지역**: {mentor.location}")
        st.markdown(f"**관심사**: {', '.join(mentor.interests)}")
        st.markdown(f"**전문분야**: {', '.join(mentor.expertise)}")
        with st.expander("자기소개 보기"):
            st.write(mentor.introduction)
    
    with col2:
        st.subheader("👨‍🎓 멘티")
        st.markdown(f"**이름**: {mentee.name}")
        st.markdown(f"**직책**: {mentee.job_title}")
        st.markdown(f"**경력**: {mentee.experience_years}년")
        st.markdown(f"**지역**: {mentee.location}")
        st.markdown(f"**관심사**: {', '.join(mentee.interests)}")
        st.markdown(f"**예산**: {mentee.budget_limit:,}원")
        st.markdown(f"**학습 목표**: {', '.join(mentee.learning_goals)}")
        with st.expander("자기소개 보기"):
            st.write(mentee.introduction)
    
    # 매칭 실행
    if st.session_state.get('run_matching', False):
        st.markdown("---")
        st.header("✨ 추천 프로그램")
        
        with st.spinner("🔍 최적의 프로그램을 찾는 중..."):
            try:
                # 매칭 서비스 실행
                matching_service = MatchingService()
                matching_service.load_programs_from_file("data/sample_programs.json")
                
                recommendations = matching_service.find_matches(
                    mentor=mentor,
                    mentee=mentee,
                    top_k=top_k
                )
                
                if not recommendations:
                    st.warning("❌ 예산 내에서 추천 가능한 프로그램이 없습니다.")
                else:
                    st.success(f"🎉 {len(recommendations)}개의 프로그램을 찾았습니다!")
                    
                    # 추천 프로그램 표시
                    for idx, rec in enumerate(recommendations, 1):
                        program = rec.program
                        
                        with st.container():
                            st.markdown(f"### 🏆 추천 {idx}: {program.title}")
                            
                            # 점수 프로그레스 바
                            st.progress(rec.match_score / 100)
                            st.markdown(f"**매칭 점수**: {rec.match_score:.1f}/100")
                            
                            # 프로그램 정보
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("📍 위치", program.location)
                                st.metric("🎯 활동", program.activity_type)
                            with col2:
                                st.metric("💰 비용", f"{program.estimated_cost:,}원")
                                st.metric("⏱️ 시간", f"{program.duration_minutes}분")
                            with col3:
                                st.metric("👥 추천 직군", ", ".join(program.recommended_for[:2]))
                            
                            # 추천 이유
                            st.markdown("**💡 추천 이유:**")
                            st.info(rec.reason)
                            
                            # 프로그램 설명
                            with st.expander("📝 상세 설명"):
                                st.write(program.description)
                                st.markdown(f"**태그**: {', '.join(program.tags)}")
                            
                            st.markdown("---")
                
            except Exception as e:
                st.error(f"❌ 매칭 중 오류 발생: {e}")
        
        # 초기화
        st.session_state['run_matching'] = False
    
    # 푸터
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>🎯 신입사원 멘토링 매칭 Agent | 규칙 기반 추천 시스템</p>
        <p style='font-size: 0.8em; color: gray;'>지역, 예산, 관심사, 직무를 고려한 최적의 매칭</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

