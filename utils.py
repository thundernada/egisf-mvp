"""
دوال مساعدة مشتركة عبر التطبيق
"""

import streamlit as st
import requests
import time
from typing import Dict, Any, Tuple
import config

def apply_custom_css():
    """
    تطبيق CSS مخصص للتطبيق
    """
    st.markdown(f"""
        <style>
        /* الخط الأساسي */
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
        }}
        
        /* الألوان الرئيسية */
        .stApp {{
            background: linear-gradient(135deg, {config.COLORS['light']} 0%, #ffffff 100%);
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {config.COLORS['primary']} 0%, {config.COLORS['dark']} 100%);
        }}
        
        [data-testid="stSidebar"] .css-1d391kg {{
            color: white;
        }}
        
        /* العناوين */
        h1 {{
            color: {config.COLORS['primary']};
            border-bottom: 3px solid {config.COLORS['secondary']};
            padding-bottom: 10px;
        }}
        
        h2 {{
            color: {config.COLORS['dark']};
        }}
        
        /* البطاقات */
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-right: 4px solid {config.COLORS['secondary']};
            margin: 10px 0;
        }}
        
        /* الأزرار */
        .stButton>button {{
            background: linear-gradient(90deg, {config.COLORS['primary']} 0%, {config.COLORS['info']} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 30px;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        }}
        
        /* شريط التقدم */
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, {config.COLORS['secondary']} 0%, {config.COLORS['primary']} 100%);
        }}
        
        /* رسائل النجاح والفشل */
        .success-message {{
            background: {config.COLORS['success']};
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.2em;
            font-weight: bold;
            animation: fadeIn 0.5s;
        }}
        
        .danger-message {{
            background: {config.COLORS['danger']};
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.2em;
            font-weight: bold;
            animation: shake 0.5s;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-10px); }}
            75% {{ transform: translateX(10px); }}
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 20px;
            color: {config.COLORS['dark']};
            border-top: 2px solid {config.COLORS['secondary']};
            margin-top: 50px;
        }}
        </style>
    """, unsafe_allow_html=True)


def calculate_sfm_score(economic: float, social: float, environmental: float) -> float:
    """
    حساب درجة الجدوى الشاملة (SFM)
    
    Args:
        economic: الدرجة الاقتصادية (0-100)
        social: الدرجة الاجتماعية (0-100)
        environmental: الدرجة البيئية (0-100)
    
    Returns:
        float: الدرجة المركبة (0-100)
    """
    sfm_score = (
        economic * config.SFM_WEIGHTS['economic'] +
        social * config.SFM_WEIGHTS['social'] +
        environmental * config.SFM_WEIGHTS['environmental']
    )
    return round(sfm_score, 2)


def check_gate_2_conditions(
    risk_score: float,
    sustainability_score: float,
    npv: float,
    sfm_score: float
) -> Tuple[bool, str, list]:
    """
    فحص شروط اجتياز البوابة الثانية
    
    Args:
        risk_score: درجة المخاطر (0-100)
        sustainability_score: درجة الاستدامة (0-100)
        npv: صافي القيمة الحالية (بالملايين)
        sfm_score: درجة الجدوى الشاملة (0-100)
    
    Returns:
        Tuple[bool, str, list]: (نجح/فشل, السبب, قائمة الانتهاكات)
    """
    thresholds = config.GATE_THRESHOLDS['gate_2']
    violations = []
    
    # فحص المخاطر
    if risk_score > thresholds['max_risk']:
        violations.append(f"⚠️ درجة المخاطر ({risk_score}%) تتجاوز الحد المسموح ({thresholds['max_risk']}%)")
    
    # فحص الاستدامة
    if sustainability_score < thresholds['min_sustainability']:
        violations.append(f"🌱 درجة الاستدامة ({sustainability_score}%) أقل من الحد الأدنى ({thresholds['min_sustainability']}%)")
    
    # فحص NPV
    if npv < thresholds['min_npv']:
        violations.append(f"💰 صافي القيمة الحالية ({npv} مليون) سالب أو صفر")
    
    # فحص SFM
    if sfm_score < thresholds['min_sfm_score']:
        violations.append(f"📊 درجة الجدوى الشاملة ({sfm_score}) أقل من الحد الأدنى ({thresholds['min_sfm_score']})")
    
    # القرار النهائي
    if violations:
        reason = "فشل المشروع في استيفاء الشروط التالية:\n" + "\n".join(violations)
        return False, reason, violations
    else:
        reason = "✅ المشروع استوفى جميع شروط البوابة الثانية بنجاح"
        return True, reason, []


def send_to_n8n_webhook(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    إرسال البيانات إلى n8n webhook
    
    Args:
        data: البيانات المراد إرسالها
    
    Returns:
        Dict: استجابة من n8n أو رسالة خطأ
    """
    try:
        response = requests.post(
            config.N8N_WEBHOOK_URL,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json(),
                'message': 'تم إرسال البيانات بنجاح'
            }
        else:
            return {
                'success': False,
                'error': f'خطأ في الاستجابة: {response.status_code}',
                'message': 'فشل الاتصال بالخادم'
            }
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'انتهت مهلة الاتصال',
            'message': 'الرجاء المحاولة مرة أخرى'
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'خطأ في الاتصال بالشبكة'
        }


def display_metric_card(title: str, value: str, delta: str = None, icon: str = "📊"):
    """
    عرض بطاقة مقياس بتصميم مخصص
    
    Args:
        title: عنوان المقياس
        value: القيمة
        delta: التغيير (اختياري)
        icon: أيقونة (اختياري)
    """
    delta_html = f"<p style='color: gray; font-size: 0.9em;'>{delta}</p>" if delta else ""
    
    st.markdown(f"""
        <div class="metric-card">
            <p style="color: gray; font-size: 0.9em; margin: 0;">{icon} {title}</p>
            <h2 style="margin: 10px 0; color: {config.COLORS['primary']};">{value}</h2>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


def show_loading_animation(message: str = "جاري المعالجة..."):
    """
    عرض رسالة تحميل مع شريط تقدم
    
    Args:
        message: رسالة التحميل
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        time.sleep(0.02)
        progress_bar.progress(i + 1)
        status_text.text(f"{message} {i+1}%")
    
    progress_bar.empty()
    status_text.empty()