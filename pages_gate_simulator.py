# -*- coding: utf-8 -*-

import streamlit as st
from datetime import datetime
import config
from utils import (
    check_gate_2_conditions,
    send_to_n8n_webhook,
    show_loading_animation
)

def show():
    st.title("🚪 محاكي بوابات العبور الرقمية")

    st.info(
        "💡 البوابة الثانية (الجدوى الشاملة): "
        "نقطة الفحص الحاسمة لتقرير استمرار المشروع."
    )

    st.subheader("📝 بيانات المشروع")
    col1, col2 = st.columns(2)

    with col1:
        project_name = st.text_input(
            "اسم المشروع الاستثماري",
            "محطة طاقة شمسية هجينة"
        )
        sector = st.selectbox(
            "القطاع",
            ["الطاقة", "النقل", "المياه", "الصحة", "التعليم"]
        )
        budget = st.number_input(
            "الميزانية التقديرية (مليون دولار)",
            min_value=0.1,
            value=50.0
        )

    with col2:
        risk_score = st.slider("مؤشر المخاطر (%)", 0, 100, 35)
        sustainability_score = st.slider(
            "مؤشر الاستدامة والبيئة (%)", 0, 100, 85
        )
        npv = st.number_input(
            "صافي القيمة الحالية NPV (مليون)",
            value=12.5
        )

    st.subheader("📊 معايير الجدوى الشاملة (SFM)")
    eco = st.slider("الأثر الاقتصادي", 0, 100, 75)
    soc = st.slider("الأثر الاجتماعي", 0, 100, 80)
    env = st.slider("الأثر البيئي", 0, 100, 90)

    if st.button("🚀 تقييم البوابة"):
        show_loading_animation("جاري التحليل...")

        sfm_score = (eco + soc + env) / 3

        is_passed, reason, violations = check_gate_2_conditions(
            risk_score=risk_score,
            sustainability_score=sustainability_score,
            npv=npv,
            sfm_score=sfm_score
        )

        payload = {
            "project_name": project_name,
            "sector": sector,
            "budget": budget,
            "sfm_score": round(sfm_score, 2),
            "passed": is_passed,
            "timestamp": datetime.now().isoformat()
        }

        try:
            send_to_n8n_webhook(payload)
        except Exception:
            pass

        st.divider()

        if is_passed:
            st.success("✅ المشروع اجتاز البوابة الثانية")
        else:
            st.error(f"❌ لم يجتز البوابة: {reason}")
            for v in violations:
                st.warning(v)
