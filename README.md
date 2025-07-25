# ehabgm-payment-system
# 🛒 نظام الدفع الإلكتروني الآلي - EhabGM Online Services

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.0.3-green)

نظام متكامل لإدارة الطلبات وإرسال روابط الدفع تلقائيًا عبر واتساب، مع تتبع الطلبات وتأكيد الدفع تلقائيًا باستخدام رسائل SMS من فودافون كاش.

## 🌟 المميزات

- ✅ **واجهة ويب احترافية** لإدخال الطلبات (بالعربية).
- ✅ **إنشاء طلب فريد** تلقائيًا لكل عميل.
- ✅ **إرسال رابط الدفع** (فودافون كاش) تلقائيًا عبر واتساب باستخدام [Green API](https://green-api.com/).
- ✅ **تتبع الطلبات** في الوقت الحقيقي على صفحة الويب (حالة "معلق" أو "مدفوع").
- ✅ **تأكيد الدفع تلقائيًا** عند استلام رسالة SMS من فودافون كاش باستخدام تطبيق [MicroDroid](https://play.google.com/store/apps/details?id=net.xdevelop.rm).
- ✅ **قابل للنشر** على منصات استضافة مجانية مثل Render.com.
- ✅ **كود مفتوح المصدر** وسهل التخصيص.

## 📁 هيكل المشروع
ehabgm-payment-system/
├── app.py # الخادم الخلفي (Backend) - Python/Flask
├── index.html # الواجهة الأمامية (Frontend) - HTML/CSS/JS
├── requirements.txt # المكتبات المطلوبة
├── render.yaml # إعدادات النشر لـ Render.com
├── orders.json # (يُنشأ تلقائيًا) تخزين الطلبات (للتطوير)
└── README.md # هذا الملف



## 🚀 كيفية التشغيل محليًا

### المتطلبات

- [Python 3.10+](https://www.python.org/downloads/)
- حساب على [Green API](https://green-api.com/) (للإرسال عبر واتساب).

### الخطوات

1. **استنساخ المشروع (أو إنشاء المجلد):**
   ```bash
   git clone https://github.com/ehabhoba/ehabgm-payment-system.git
   cd ehabgm-payment-system
