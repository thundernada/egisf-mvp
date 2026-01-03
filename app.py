"""
تطبيق EGISF MVP - الإطار الذكي المتكامل للحوكمة الاستثمارية
نظام محاكاة لبوابات العبور الرقمية ومحرك القرارات السيادية

المطور: فريق الحوكمة الذكية
الإصدار: v1.0.0 MVP
"""

import streamlit as st
from streamlit_option_menu import option_menu
import config
from utils import apply_custom_css

# استيراد الصفحات
from pages import vision, gate_simulator, decision_center, live_report

# ═══════════════════════════════════════════════════════════════
# إعدادات الصفحة
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title=config.APP_INFO['title'],
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/egisf-mvp',
        'Report a bug': 'https://github.com/your-repo/egisf-mvp/issues',
        'About': f"{config.APP_INFO['subtitle']} - {config.APP_INFO['version']}"
    }
)

# تطبيق CSS مخصص
apply_custom_css()

# ═══════════════════════════════════════════════════════════════
# الشريط الجانبي (Sidebar)
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    # الشعار والعنوان
    st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: {config.COLORS['secondary']}; font-size: 2.5em; margin: 0;">
                🏛️
            </h1>
            <h2 style="color: white; margin: 10px 0; font-size: 1.5em;">
                {config.APP_INFO['title']}
            </h2>
            <p style="color: {config.COLORS['light']}; font-size: 0.9em;">
                {config.APP_INFO['subtitle']}
            </p>
            <p style="color: {config.COLORS['secondary']}; font-size: 0.8em; margin-top: 5px;">
                {config.APP_INFO['version']}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # القائمة الرئيسية
    selected = option_menu(
        menu_title="القائمة الرئيسية",
        options=[
            "الرؤية الاستراتيجية",
            "بوابات العبور الرقمية",
            "محاكي القرار السيادي",
            "تقرير الأداء الحي"
        ],
        icons=['flag', 'door-open', 'building', 'graph-up'],
        menu_icon="list",
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "icon": {"color": config.COLORS['secondary'], "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "right",
                "margin": "5px",
                "--hover-color": config.COLORS['dark']
            },
            "nav-link-selected": {"background-color": config.COLORS['secondary']},
        }
    )
    
    st.markdown("---")
    
    # معلومات سريعة
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 15px; 
                    border-radius: 10px; margin: 10px 0;">
            <p style="color: white; font-size: 0.9em; margin: 0;">
                <strong>📊 إحصائية سريعة:</strong><br>
                • المشاريع النشطة: <strong>487</strong><br>
                • القيمة الإجمالية: <strong>28.5 مليار</strong><br>
                • معدل النجاح: <strong>87%</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # روابط مفيدة
    st.markdown("### 🔗 روابط مفيدة")
    st.markdown("""
        - [📚 الوثائق الكاملة](https://docs.egisf.gov)
        - [💻 GitHub Repository](https://github.com/your-repo/egisf-mvp)
        - [📧 الدعم الفني](mailto:support@egisf.gov)
    """)

# ═══════════════════════════════════════════════════════════════
# المحتوى الرئيسي
# ═══════════════════════════════════════════════════════════════

# عرض الصفحة المختارة
if selected == "الرؤية الاستراتيجية":
    vision.show()

elif selected == "بوابات العبور الرقمية":
    gate_simulator.show()

elif selected == "محاكي القرار السيادي":
    decision_center.show()

elif selected == "تقرير الأداء الحي":
    live_report.show()

# ═══════════════════════════════════════════════════════════════
# التذييل (Footer)
# ═══════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(f"""
    <div class="footer">
        <p style="margin: 0;">
            {config.APP_INFO['organization']} © 2025 | 
            تم التطوير بواسطة فريق التحول الرقمي
        </p>
        <p style="font-size: 0.9em; color: gray; margin: 5px 0 0 0;">
            {config.APP_INFO['version']} | 
            آخر تحديث: يناير 2025
        </p>
    </div>
""", unsafe_allow_html=True)