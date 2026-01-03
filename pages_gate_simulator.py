"""
صفحة محاكي بوابات العبور
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import config
from utils import (
    calculate_sfm_score,
    check_gate_2_conditions,
    send_to_n8n_webhook,
    show_loading_animation
)

def show():
    """عرض صفحة محاكي البوابات"""
    
    st.title("🚪 محاكي بوابات العبور الرقمية")
    
    st.markdown("""
        <div style="background: linear-gradient(90deg, #3498db 0%, #2ecc71 100%); 
                    color: white; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <p style="margin: 0; font-size: 1.1em;">
                💡 <strong>البوابة الثانية (الجدوى الشاملة)</strong>: 
                نقطة الفحص الحرجة التي تُقرر مصير المشروع بناءً على معايير اقتصادية 
                واجتماعية وبيئية صارمة.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # نموذج إدخال البيانات
    st.subheader("📝 بيانات المشروع")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input(
            "اسم المشروع",
            placeholder="مثال: مستشفى الشمال التخصصي",
            help="أدخل اسماً واضحاً ووصفياً للمشروع"
        )
        
        project_cost = st.number_input(
            "التكلفة التقديرية (مليون دولار)",
            min_value=0.1,
            max_value=1000.0,
            value=20.0,
            step=0.5,
            help="التكلفة الإجمالية المقدرة للمشروع"
        )
        
        project_location = st.text_input(
            "الموقع",
            placeholder="مثال: المنطقة الشمالية",
            help="الموقع الجغرافي للمشروع"
        )
    
    with col2:
        project_sector = st.selectbox(
            "القطاع",
            ["الصحة", "التعليم", "البنية التحتية", "الإسكان", "الطاقة", "الصناعة"]
        )
        
        project_duration = st.number_input(
            "المدة المتوقعة (أشهر)",
            min_value=1,
            max_value=120,
            value=24,
            help="المدة الزمنية المتوقعة لإنجاز المشروع"
        )
        
        npv = st.number_input(
            "صافي القيمة الحالية (مليون دولار)",
            min_value=-100.0,
            max_value=500.0,
            value=8.5,
            step=0.1,
            help="NPV المحسوب من دراسة الجدوى المالية"
        )
    
    st.markdown("---")
    
    # مؤشرات الأداء (Sliders)
    st.subheader("📊 مؤشرات الأداء والجدوى")
    
    st.markdown("""
        <p style="color: gray; font-size: 0.9em;">
            استخدم الشرائح التالية لتحديد درجات المشروع في المحاور المختلفة (0-100)
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**💰 الجدوى الاقتصادية**")
        economic_score = st.slider(
            "الدرجة الاقتصادية",
            0, 100, 75,
            help="تقييم الجدوى المالية والعائد الاقتصادي"
        )
        st.progress(economic_score / 100)
    
    with col2:
        st.markdown("**👥 الأثر الاجتماعي**")
        social_score = st.slider(
            "الدرجة الاجتماعية",
            0, 100, 65,
            help="تقييم الأثر على المجتمع وفرص العمل والخدمات"
        )
        st.progress(social_score / 100)
    
    with col3:
        st.markdown("**🌱 الاستدامة البيئية**")
        environmental_score = st.slider(
            "الدرجة البيئية",
            0, 100, 55,
            help="تقييم الأثر البيئي والاستدامة"
        )
        st.progress(environmental_score / 100)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**⚠️ درجة المخاطر**")
        risk_score = st.slider(
            "نسبة المخاطر (%)",
            0, 100, 45,
            help="تقييم شامل للمخاطر (فني، مالي، تشغيلي)"
        )
        
        # لون ديناميكي بناءً على المخاطر
        risk_color = config.COLORS['success'] if risk_score < 40 else (
            config.COLORS['warning'] if risk_score < 60 else config.COLORS['danger']
        )
        st.markdown(f"""
            <div style="background: {risk_color}; color: white; padding: 10px; 
                        border-radius: 5px; text-align: center; font-weight: bold;">
                {risk_score}% - {'منخفض' if risk_score < 40 else ('متوسط' if risk_score < 60 else 'مرتفع')}
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**🌿 درجة الاستدامة الشاملة**")
        sustainability_score = st.slider(
            "نسبة الاستدامة (%)",
            0, 100, 60,
            help="SIM Score - تقييم شامل للاستدامة"
        )
        
        # لون ديناميكي بناءً على الاستدامة
sust_color = config.COLORS['danger'] if sustainability_score < 40 else (
config.COLORS['warning'] if sustainability_score < 70 else config.COLORS['success']
)
st.markdown(f"""
<div style="background: {sust_color}; color: white; padding: 10px; 
                     border-radius: 5px; text-align: center; font-weight: bold;">
{sustainability_score}% - {'ضعيف' if sustainability_score < 40 else ('مقبول' if sustainability_score < 70 else 'ممتاز')}
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# حساب SFM Score
sfm_score = calculate_sfm_score(economic_score, social_score, environmental_score)

# عرض الدرجة المركبة
st.subheader("📈 درجة الجدوى الشاملة (SFM Score)")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Gauge chart لعرض SFM Score
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=sfm_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "الدرجة المركبة", 'font': {'size': 20}},
        delta={'reference': 60, 'increasing': {'color': config.COLORS['success']}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': config.COLORS['dark']},
            'bar': {'color': config.COLORS['primary']},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': config.COLORS['dark']},
            'steps': [
                {'range': [0, 40], 'color': config.COLORS['danger']},
                {'range': [40, 60], 'color': config.COLORS['warning']},
                {'range': [60, 100], 'color': config.COLORS['success']}
            ],
            'threshold': {
                'line': {'color': config.COLORS['secondary'], 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        font={'family': 'Tajawal', 'color': config.COLORS['dark'], 'size': 14}
    )
    
    st.plotly_chart(fig, use_container_width=True)

# عرض توزيع الدرجات
st.subheader("📊 توزيع الجدوى الثلاثي")

df_sfm = pd.DataFrame({
    'المحور': ['اقتصادي', 'اجتماعي', 'بيئي'],
    'الدرجة': [economic_score, social_score, environmental_score],
    'الوزن': [
        config.SFM_WEIGHTS['economic'] * 100,
        config.SFM_WEIGHTS['social'] * 100,
        config.SFM_WEIGHTS['environmental'] * 100
    ]
})

fig = px.bar(
    df_sfm,
    x='المحور',
    y='الدرجة',
    color='المحور',
    text='الدرجة',
    color_discrete_sequence=[config.COLORS['primary'], config.COLORS['info'], config.COLORS['success']]
)

fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(
    height=400,
    xaxis_title="",
    yaxis_title="الدرجة (0-100)",
    showlegend=False,
    font={'family': 'Tajawal', 'size': 14}
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# زر التحليل
if st.button("🔍 تحليل البوابة الثانية (SFM)", type="primary", use_container_width=True):
    
    if not project_name:
        st.error("⚠️ الرجاء إدخال اسم المشروع")
        return
    
    # عرض رسالة التحميل
    with st.spinner("🔄 جاري تحليل البيانات وفحص شروط البوابة..."):
        show_loading_animation()
    
    # فحص شروط البوابة
    passed, reason, violations = check_gate_2_conditions(
        risk_score,
        sustainability_score,
        npv,
        sfm_score
    )
    
    # إعداد البيانات للإرسال إلى n8n
    project_data = {
        'project_name': project_name,
        'project_cost': project_cost,
        'project_location': project_location,
        'project_sector': project_sector,
        'project_duration': project_duration,
        'npv': npv,
        'economic_score': economic_score,
        'social_score': social_score,
        'environmental_score': environmental_score,
        'sfm_score': sfm_score,
        'risk_score': risk_score,
        'sustainability_score': sustainability_score,
        'gate_2_passed': passed,
        'timestamp': datetime.now().isoformat()
    }
    
    # إرسال إلى n8n (إذا كان مفعلاً)
    with st.spinner("📡 جاري الاتصال بمحرك القرارات..."):
        n8n_response = send_to_n8n_webhook(project_data)
    
    # عرض النتيجة
    st.markdown("---")
    st.subheader("📋 نتيجة التحليل")
    
    if passed:
        st.markdown(f"""
            <div class="success-message">
                ✅ تم اجتياز البوابة الثانية بنجاح!
            </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        
        st.success(reason)
        
        # عرض التفاصيل
        with st.expander("📊 تفاصيل التقييم"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("درجة SFM", f"{sfm_score}/100", "جيد جداً ✓")
                st.metric("صافي القيمة الحالية", f"{npv} مليون", "موجب ✓")
            
            with col2:
                st.metric("درجة المخاطر", f"{risk_score}%", "مقبول ✓")
                st.metric("درجة الاستدامة", f"{sustainability_score}%", "مقبول ✓")
        
        # الخطوات التالية
        st.info("""
            **📌 الخطوات التالية:**
            1. الانتقال إلى البوابة الثالثة (التصميم المعتمد)
            2. إعداد نموذج BIM بمستوى LOD 300
            3. تحليل GIS المتقدم للموقع
            4. إعداد وثائق المناقصة
        """)
        
    else:
        st.markdown(f"""
            <div class="danger-message">
                ❌ فشل المشروع في اجتياز البوابة الثانية
            </div>
        """, unsafe_allow_html=True)
        
        st.error(reason)
        
        # عرض الانتهاكات
        with st.expander("⚠️ تفاصيل الانتهاكات"):
            for violation in violations:
                st.warning(violation)
        
        # التوصيات
        st.info("""
            **💡 التوصيات:**
            - مراجعة دراسة الجدوى وتحسين المحاور الضعيفة
            - إعادة تصميم المشروع لتقليل المخاطر
            - تحسين معايير الاستدامة
            - التشاور مع لجنة الاستثناءات في حالات الضرورة القصوى
        """)
    
    # عرض استجابة n8n
    if n8n_response['success']:
        with st.expander("🔗 استجابة محرك القرارات (n8n)"):
            st.json(n8n_response['data'])
    else:
        with st.expander("⚠️ ملاحظة: محرك القرارات غير متصل"):
            st.warning(f"لم يتم الاتصال بـ n8n: {n8n_response['message']}")
            st.info("💡 لتفعيل الاتصال، يُرجى إعداد Webhook في n8n وتحديث الرابط في ملف config.py")---

 (`decision_center.py`, `live_report.py`, `app.py`) + دليل إعداد n8n Webhook...