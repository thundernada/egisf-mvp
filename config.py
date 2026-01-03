"""
ملف الإعدادات الرئيسي لتطبيق EGISF
يحتوي على الثوابت والإعدادات المشتركة
"""

# إعدادات الاتصال بـ n8n
N8N_WEBHOOK_URL = "https://your-n8n-instance.com/webhook/egisf-gate-check"
# يمكن تعديل الرابط بعد إنشاء Webhook في n8n

# الألوان السيادية
COLORS = {
    'primary': '#1e3a5f',      # كحلي داكن
    'secondary': '#d4af37',     # ذهبي
    'success': '#2ecc71',       # أخضر
    'danger': '#e74c3c',        # أحمر
    'warning': '#f39c12',       # برتقالي
    'info': '#3498db',          # أزرق فاتح
    'dark': '#2c3e50',          # رمادي داكن
    'light': '#ecf0f1'          # رمادي فاتح
}

# حدود القبول في البوابات
GATE_THRESHOLDS = {
    'gate_2': {
        'max_risk': 60,        # الحد الأقصى للمخاطر (%)
        'min_sustainability': 40,  # الحد الأدنى للاستدامة (%)
        'min_npv': 0,          # الحد الأدنى لـ NPV (يجب أن يكون موجباً)
        'min_sfm_score': 60    # الحد الأدنى لدرجة SFM
    }
}

# أوزان الجدوى الشاملة (SFM)
SFM_WEIGHTS = {
    'economic': 0.40,
    'social': 0.30,
    'environmental': 0.30
}

# معلومات التطبيق
APP_INFO = {
    'title': 'EGISF',
    'subtitle': 'الإطار الذكي المتكامل للحوكمة الاستثمارية',
    'version': 'v1.0.0 MVP',
    'organization': 'مكتب الحوكمة الذكية'
}