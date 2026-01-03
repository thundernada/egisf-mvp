"""
صفحة محاكي القرار السيادي
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import config
from utils import display_metric_card

def show():
    """عرض صفحة محاكي القرار السيادي"""
    
    st.title("🏛️ مركز قرارات السيادة")
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, {config.COLORS['primary']} 0%, {config.COLORS['dark']} 100%); 
                    color: white; padding: 25px; border-radius: 15px; 
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3); margin: 20px 0;">
            <h3 style="color: white; margin: 0 0 15px 0; border: none;">👑 مجلس القرارات الاستراتيجية</h3>
            <p style="font-size: 1.1em; line-height: 1.8; margin: 0;">
                هذه الغرفة الافتراضية تحاكي <strong>مركز القيادة الاستراتيجي</strong> حيث يتخذ 
                صناع القرار الوطني القرارات المصيرية بشأن المشاريع الاستثمارية الكبرى.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # محاكاة مشاريع قيد المراجعة
    projects_pending = [
        {
            'id': 'PRJ-2025-00234',
            'name': 'مطار إقليمي - المنطقة الشرقية',
            'cost': 450,
            'status': 'critical',
            'sfm_score': 58,
            'risk': 72,
            'issue': 'تأخير 6 أشهر + تجاوز ميزانية 12%'
        },
        {
            'id': 'PRJ-2025-00156',
            'name': 'محطة طاقة شمسية - 500 ميجاواط',
            'cost': 380,
            'status': 'warning',
            'sfm_score': 82,
            'risk': 48,
            'issue': 'نزاع قانوني مع مقاول فرعي'
        },
        {
            'id': 'PRJ-2025-00089',
            'name': 'طريق سريع - 250 كم',
            'cost': 520,
            'status': 'pending',
            'sfm_score': 75,
            'risk': 35,
            'issue': 'انتظار موافقة M17_ESG_Approval'
        }
    ]
    
    # المقاييس الإجمالية
    st.subheader("📊 ملخص الحالة الوطنية")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        display_metric_card(
            "المشاريع النشطة",
            "487",
            "قيمة: 28.5 مليار",
            "📁"
        )
    
    with col2:
        display_metric_card(
            "المشاريع الحرجة",
            "20",
            "4% من الإجمالي",
            "🔴"
        )
    
    with col3:
        display_metric_card(
            "قرارات معلقة",
            "3",
            "تحتاج موافقة عاجلة",
            "⏳"
        )
    
    with col4:
        display_metric_card(
            "معدل النجاح",
            "87%",
            "+32% عن السابق",
            "✅"
        )
    
    st.markdown("---")
    
    # قائمة المشاريع المعلقة
    st.subheader("📋 المشاريع المعلقة للقرار")
    
    for project in projects_pending:
        status_colors = {
            'critical': config.COLORS['danger'],
            'warning': config.COLORS['warning'],
            'pending': config.COLORS['info']
        }
        
        status_labels = {
            'critical': '🔴 حرج',
            'warning': '🟡 يحتاج متابعة',
            'pending': '🔵 قيد المراجعة'
        }
        
        with st.expander(f"**{project['name']}** - {status_labels[project['status']]}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                    **📌 معرف المشروع:** `{project['id']}`  
                    **💰 القيمة:** {project['cost']} مليون دولار  
                    **⚠️ المشكلة:** {project['issue']}
                """)
                
                # SFM Score progress
                st.markdown("**درجة الجدوى الشاملة:**")
                st.progress(project['sfm_score'] / 100)
                st.caption(f"{project['sfm_score']}/100")
                
                # Risk Score
                st.markdown("**درجة المخاطر:**")
                risk_color = 'normal' if project['risk'] < 60 else 'inverse'
                st.progress(project['risk'] / 100)
                st.caption(f"{project['risk']}% - {'مرتفع' if project['risk'] > 60 else 'متوسط'}")
            
            with col2:
                st.markdown("**القرارات المتاحة:**")
                
                if st.button("✅ اعتماد", key=f"approve_{project['id']}", use_container_width=True):
                    st.success(f"تم اعتماد المشروع {project['id']}")
                    st.balloons()
                
                if st.button("⏸️ تجميد", key=f"hold_{project['id']}", use_container_width=True):
                    st.warning(f"تم تجميد المشروع {project['id']}")
                
                if st.button("❌ رفض", key=f"reject_{project['id']}", use_container_width=True):
                    st.error(f"تم رفض المشروع {project['id']}")
    
    st.markdown("---")
    
    # Gantt Chart للجدول الزمني
    st.subheader("📅 الجدول الزمني للمشاريع الحرجة")
    
    # بيانات وهمية لـ Gantt
    df_gantt = pd.DataFrame([
        dict(Task="مطار إقليمي", Start='2024-03-01', Finish='2026-12-31', Resource='حرج'),
        dict(Task="محطة طاقة شمسية", Start='2024-06-01', Finish='2026-08-31', Resource='تحذير'),
        dict(Task="طريق سريع", Start='2024-09-01', Finish='2027-03-31', Resource='مراجعة'),
    ])
    
    df_gantt['Start'] = pd.to_datetime(df_gantt['Start'])
    df_gantt['Finish'] = pd.to_datetime(df_gantt['Finish'])
    
    fig = go.Figure()
    
    colors = {'حرج': config.COLORS['danger'], 
              'تحذير': config.COLORS['warning'], 
              'مراجعة': config.COLORS['info']}
    
    for i, row in df_gantt.iterrows():
        fig.add_trace(go.Bar(
            x=[row['Finish'] - row['Start']],
            y=[row['Task']],
            base=row['Start'],
            orientation='h',
            marker=dict(color=colors[row['Resource']]),
            name=row['Resource'],
            showlegend=i == 0,
            text=row['Resource'],
            textposition='inside'
        ))
    
    fig.update_layout(
        title="الجدول الزمني المتوقع",
        xaxis_title="التاريخ",
        yaxis_title="",
        height=400,
        font={'family': 'Tajawal', 'size': 14}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # محاكي قرار سريع
    st.subheader("⚡ محاكي القرار السريع")
    
    st.markdown("""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-right: 4px solid #3498db;">
            💡 <strong>سيناريو افتراضي:</strong> مشروع جديد يحتاج قرار عاجل خلال 24 ساعة
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("quick_decision_form"):
        scenario = st.selectbox(
            "اختر السيناريو",
            [
                "مشروع طارئ بعد كارثة طبيعية",
                "فرصة استثمارية محدودة الوقت",
                "مشروع استراتيجي أمن قومي",
                "مشروع تنموي في منطقة محرومة"
            ]
        )
        
        urgency = st.slider("مستوى الأولوية", 1, 10, 7)
        
        decision_note = st.text_area(
            "ملاحظات القرار",
            placeholder="أدخل المبررات والملاحظات..."
        )
        
        submitted = st.form_submit_button("📝 تسجيل القرار", use_container_width=True)
        
        if submitted:
            st.success(f"✅ تم تسجيل القرار بخصوص: {scenario}")
            st.info(f"📌 مستوى الأولوية: {urgency}/10")
            
            if urgency >= 8:
                st.warning("⚠️ هذا المشروع يتطلب متابعة يومية")