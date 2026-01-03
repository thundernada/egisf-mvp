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
    """عرض صفحة محاكي البوابات"""
    st.title("🚪 محاكي بوابات العبور الرقمية")

    # بطاقة توضيحية
    st.markdown(
        f"""
        <div style="background: linear-gradient(90deg, {config.COLORS['info']} 0%, {config.COLORS['success']} 100%);
                    color: white; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <p style="margin: 0; font-size: 1.05em;">
                💡 <strong>البوابة الثانية (الجدوى الشاملة)</strong>:
                نقطة الفحص الحرجة التي تُقرر مصير المشروع بناءً على معايير اقتصادية،
                اجتماعية وبيئية صارمة.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # نموذج إدخال البيانات
    st.subheader("📝 بيانات المشروع")
    col1, col2 = st.columns(2)

    with col1:
        project_name = st.text_input("اسم المشروع الاستثماري", "محطة طاقة شمسية هجينة")
        sector = st.selectbox(
            "القطاع",
            ["الطاقة", "النقل", "المياه", "الصحة", "التعليم"]
        )
        budget = st.number_input(
            "الميزانية التقديرية (مليون دولار)",
            min_value=0.1,
            value=50.0,
            step=0.1
        )

    with col2:
        risk_score = st.slider("مؤشر المخاطر (%)", 0, 100, 35)
        sustainability_score = st.slider("مؤشر الاستدامة والبيئة (%)", 0, 100, 85)
        npv = st.number_input(
            "صافي القيمة الحالية NPV (مليون)",
            value=12.5,
            format="%.2f"
        )

    # معايير SFM
    st.subheader("📊 معايير الجدوى الشاملة (SFM)")
    c1, c2, c3 = st.columns(3)

    with c1:
        eco_impact = st.slider("الأثر الاقتصادي", 0, 100, 75)
    with c2:
        soc_impact = st.slider("الأثر الاجتماعي", 0, 100, 80)
    with c3:
        env_impact = st.slider("الأثر البيئي", 0, 100, 90)

    if st.button("🚀 إرسال للمراجعة والعبور"):
        show_loading_animation("جاري تحليل البيانات عبر محرك القواعد...")

        sfm_score = (eco_impact + soc_impact + env_impact) / 3

        is_passed, reason, violations = check_gate_2_conditions(
            risk_score=risk_score,
            sustainability_score=sustainability_score,
            npv=npv,
            sfm_score=sfm_score
        )

        project_data = {
            "project_name": project_name,
            "sector": sector,
            "budget": budget,
            "sfm_score": round(sfm_score, 2),
            "is_passed": bool(is_passed),
            "timestamp": datetime.now().isoformat()
        }

        try:
            n8n_response = send_to_n8n_webhook(project_data) or {}
        except Exception as e:
            n8n_response = {"success": False, "error": str(e)}

        st.divider()

        if is_passed:
            st.balloons()
            st.success(
                f"✅ المشروع اجتاز البوابة الثانية بنجاح (النتيجة: {sfm_score:.1f}%)"
            )
        else:
            st.error(f"❌ فشل المشروع في اجتياز البوابة الثانية. السبب: {reason}")
            with st.expander("⚠️ تفاصيل الانتهاكات"):
                for v in violations:
                    st.warning(v)

        with st.expander("🔗 حالة الاتصال بمحرك القرارات"):
            if isinstance(n8n_response, dict) and n8n_response.get("success"):
                st.json(n8n_response.get("data", n8n_response))
            else:
                st.info(
                    n8n_response.get("error", "تم استخدام المعالجة المحلية.")
                    if isinstance(n8n_response, dict)
                    else "تم استخدام المعالجة المحلية."
                )
