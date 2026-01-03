"""
صفحة تقرير الأداء الحي
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import config

def show():
    """عرض صفحة تقرير الأداء الحي"""
    
    st.title("📈 تقرير الأداء الحي")
    
    # تاريخ ووقت التحديث
    st.markdown(f"""
        <div style="text-align: left; color: gray; font-size: 0.9em;">
            آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    """, unsafe_allow_html=True)
    
    # المؤشرات الرئيسية
    st.subheader("📊 المؤشرات الرئيسية")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics_data = [
        ("إجمالي المشاريع", "487", "+23", "📁"),
        ("القيمة الإجمالية", "28.5 مليار", "+2.1 مليار", "💰"),
        ("معدل الإنجاز", "68%", "+5%", "⚙️"),
        ("الوفورات", "180 مليون", "+15 مليون", "💎"),
        ("معدل النجاح", "87%", "+12%", "✅")
    ]
    
    cols = [col1, col2, col3, col4, col5]
    for col, (label, value, delta, icon) in zip(cols, metrics_data):
        with col:
            st.metric(label, value, delta)
    
    st.markdown("---")
    
    # توزيع المشاريع حسب الحالة
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📌 توزيع المشاريع حسب الحالة")
        
        status_data = pd.DataFrame({
            'الحالة': ['On Track', 'At Risk', 'Critical', 'Completed'],
            'العدد': [385, 82, 20, 350],
            'النسبة': [79, 17, 4, 100]
        })
        
        fig = px.pie(
            status_data,
            values='العدد',
            names='الحالة',
            color='الحالة',
            color_discrete_map={
                'On Track': config.COLORS['success'],
                'At Risk': config.COLORS['warning'],
                'Critical': config.COLORS['danger'],
                'Completed': config.COLORS['info']
            },
            hole=0.4
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            height=400,
            font={'family': 'Tajawal', 'size': 14},
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏗️ توزيع المشاريع حسب القطاع")
        
        sector_data = pd.DataFrame({
            'القطاع': ['الصحة', 'التعليم', 'البنية التحتية', 'الإسكان', 'الطاقة'],
            'العدد': [95, 120, 180, 65, 27],
            'الميزانية': [4.2, 3.8, 12.5, 5.3, 2.7]
        })
        
        fig = px.bar(
            sector_data,
            x='القطاع',
            y='العدد',
            text='العدد',
            color='القطاع',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            height=400,
            xaxis_title="",
            yaxis_title="عدد المشاريع",
            showlegend=False,
            font={'family': 'Tajawal', 'size': 14}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # الأداء الزمني
    st.subheader("📅 الأداء الزمني (آخر 12 شهر)")
    
    # بيانات وهمية للأداء الشهري
    dates = pd.date_range(end=datetime.now(), periods=12, freq='ME')
    
    performance_data = pd.DataFrame({
        'التاريخ': dates,
        'المشاريع الجديدة': np.random.randint(15, 45, 12),
        'المشاريع المكتملة': np.random.randint(10, 35, 12),
        'الانحرافات المكتشفة': np.random.randint(2, 15, 12)
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=performance_data['التاريخ'],
        y=performance_data['المشاريع الجديدة'],
        mode='lines+markers',
        name='مشاريع جديدة',
        line=dict(color=config.COLORS['primary'], width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=performance_data['التاريخ'],
        y=performance_data['المشاريع المكتملة'],
        mode='lines+markers',
        name='مشاريع مكتملة',
        line=dict(color=config.COLORS['success'], width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=performance_data['التاريخ'],
        y=performance_data['الانحرافات المكتشفة'],
        mode='lines+markers',
        name='انحرافات مكتشفة',
        line=dict(color=config.COLORS['danger'], width=3, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        height=450,
        xaxis_title="الشهر",
        yaxis_title="العدد",
        hovermode='x unified',
        font={'family': 'Tajawal', 'size': 14},
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # أفضل وأسوأ أداء
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 أفضل 5 مشاريع أداءً")
        
        top_projects = pd.DataFrame({
            'المشروع': [
                'مستشفى الجنوب',
                'مدرسة النور',
                'جسر الوحدة',
                'محطة تحلية',
                'مركز رياضي'
            ],
            'SFM Score': [92, 89, 87, 85, 83],
            'الإنجاز': [95, 88, 92, 78, 85]
        })
        
        st.dataframe(
            top_projects,
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.subheader("⚠️ مشاريع تحتاج تدخل")
        
        bottom_projects = pd.DataFrame({
            'المشروع': [
                'مطار الشرق',
                'طريق الساحل',
                'مجمع سكني',
                'محطة كهرباء',
                'سد مائي'
            ],
            'المشكلة': [
                'تأخير 6 أشهر',
                'تجاوز ميزانية 15%',
                'نزاع قانوني',
                'مخاطر جيولوجية',
                'نقص مواد'
            ],
            'الأولوية': ['🔴 عاجل', '🔴 عاجل', '🟡 متوسط', '🟡 متوسط', '🟢 منخفض']
        })
        
        st.dataframe(
            bottom_projects,
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("---")
    
    # تحميل التقرير
    st.subheader("📥 تصدير التقرير")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 تحميل PDF", use_container_width=True):
            st.info("🔄 جاري إنشاء التقرير...")
    
    with col2:
        if st.button("📊 تحميل Excel", use_container_width=True):
            st.info("🔄 جاري تصدير البيانات...")
    
    with col3:
        if st.button("📧 إرسال بالبريد", use_container_width=True):
            st.success("✅ تم إرسال التقرير")