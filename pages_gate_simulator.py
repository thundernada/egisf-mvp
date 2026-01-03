import streamlit as st
from datetime import datetime
import config
from utils import check_gate_2_conditions, send_to_n8n_webhook, show_loading_animation

def show():
    st.title("🚪 محاكي بوابات العبور الرقمية")
    
    st.info("💡 البوابة الثانية: نقطة الفحص الحرجة لجدوى المشروع الاستثماري.")
    
    # نموذج إدخال البيانات
    st.subheader("📝 بيانات المشروع")
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input("اسم المشروع", "محطة طاقة متجددة")
        sector = st.selectbox("القطاع", ["الطاقة", "النقل", "المياه", "الصحة"])
        budget = st.number_input("الميزانية (مليون دولار)", min_value=1.0, value=50.0)
        
    with col2:
        risk_score = st.slider("مؤشر المخاطر (%)", 0, 100, 30)
        sustainability = st.slider("الاستدامة (%)", 0, 100, 80)
        npv = st.number_input("صافي القيمة الحالية NPV", value=10.0)

    # معايير SFM
    st.subheader("📊 معايير الجدوى الشاملة")
    c1, c2, c3 = st.columns(3)
    eco = c1.slider("اقتصادي", 0, 100, 70)
    soc = c2.slider("اجتماعي", 0, 100, 70)
    env = c3.slider("بيئي", 0, 100, 70)

    if st.button("🚀 تحليل والعبور"):
        show_loading_animation("جاري الفحص...")
        
        sfm_score = (eco + soc + env) / 3
        
        # فحص الشروط
        is_passed, reason, violations = check_gate_2_conditions(
            risk_score, sustainability, npv, sfm_score
        )
        
        st.divider()
        
        if is_passed:
            st.balloons()
            st.success(f"✅ اجتاز المشروع البوابة بنتيجة {sfm_score:.1f}%")
        else:
            st.error(f"❌ فشل العبور: {reason}")
            for v in violations:
                st.warning(v)
        
        # إرسال البيانات (Webhook)
        p_data = {
            "name": project_name,
            "passed": is_passed,
            "score": round(sfm_score, 2),
            "time": datetime.now().isoformat()
        }
        res = send_to_n8n_webhook(p_data)
        
        with st.expander("🔗 حالة الربط مع n8n"):
            if res.get('success'):
                st.json(res.get('data'))
            else:
                st.write("تعذر الاتصال بالمحرك الخارجي - تم استخدام المحرك المحلي.")

# نهاية الملف
