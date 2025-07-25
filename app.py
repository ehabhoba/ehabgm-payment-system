from flask import Flask, request, jsonify
import requests
import json
import uuid
from datetime import datetime
import os

app = Flask(__name__)

# =================== بيانات الحساب ===================
# استبدل البيانات دي بالبيانات الخاصة بحسابك على Green API
INSTANCE_ID = "7103121490"
API_TOKEN = "5302bc690deb405c9bd36048a27167e4c0baaa81616449da9d"
VODAFONE_CASH_LINK = "http://vf.eg/vfcash?id=mt&qrId=rMAVF3" # ضع رابط فودافون كاش الخاص بك
YOUR_VODAFONE_NUMBER = "01022679250" # ضع رقم فودافون كاش الخاص بك
# ======================================================

# تخزين الطلبات في ملف (في الإنتاج استخدم قاعدة بيانات)
orders_file = 'orders.json'

def load_orders():
    if os.path.exists(orders_file):
        with open(orders_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_orders(orders):
    with open(orders_file, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def generate_order_id():
    return f"EGM-{uuid.uuid4().hex[:6].upper()}"

def format_phone_number(phone):
    return ''.join(filter(str.isdigit, phone))

def send_whatsapp_payment(customer_phone, customer_name, order_id, amount, description=""):
    """إرسال رابط الدفع عبر واتساب"""
    customer_phone = format_phone_number(customer_phone)
    chat_id = f"{customer_phone}@c.us"
    message = (
        f"🌟 مرحباً بك في *EhabGM Online Services*\n"
        f"عزيزي/عزيزتي: *{customer_name}*\n"
        f"طلبك رقم: *{order_id}*\n"
        f"المبلغ المطلوب: *{amount} جنيه مصري*\n"
        f"{'وصف الطلب: ' + description if description else ''}\n"
        f"📲 *اضغط على الرابط التالي لإتمام الدفع عبر فودافون كاش:*\n"
        f"🔗 {VODAFONE_CASH_LINK}\n"
        f"📸 *مهم جدًا:* بعد إتمام الدفع، أرسل صورة لشاشة التأكيد (سكرين شوت) في هذه المحادثة.\n"
        f"⏳ سيتم تجهيز طلبك فور التأكيد من استلام المبلغ.\n"
        f"شكراً لثقتكم بنا! 🙏"
    )
    url = f"https://api.green-api.com/waInstance{INSTANCE_ID}/sendMessage/{API_TOKEN}"
    payload = {"chatId": chat_id, "message": message}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"📤 WhatsApp API Response Status: {response.status_code}")
        print(f"📤 WhatsApp API Response Text: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ خطأ في إرسال الرسالة: {e}")
        return False

# =================== المسارات (Routes) ===================

@app.route('/')
def index():
    """الصفحة الرئيسية - تعرض واجهة إدخال الطلبات"""
    return '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EhabGM Online Services - نظام الدفع</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .card {
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .btn-custom {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            padding: 12px 25px;
        }
        .header-bg {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-bg text-center text-white mb-4">
            <h1><i class="fas fa-shopping-cart"></i> EhabGM Online Services</h1>
            <p class="lead">نظام الدفع الإلكتروني الآلي</p>
        </div>
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h4 class="mb-0"><i class="fas fa-plus-circle"></i> إضافة طلب جديد</h4>
                    </div>
                    <div class="card-body">
                        <form id="orderForm">
                            <div class="mb-3">
                                <label for="customerName" class="form-label">اسم العميل</label>
                                <input type="text" class="form-control" id="customerName" required>
                            </div>
                            <div class="mb-3">
                                <label for="customerPhone" class="form-label">رقم هاتف العميل</label>
                                <input type="tel" class="form-control" id="customerPhone" placeholder="201098765432" required>
                                <div class="form-text">أدخل الرقم مع كود الدولة بدون +</div>
                            </div>
                            <div class="mb-3">
                                <label for="orderAmount" class="form-label">المبلغ المطلوب (جنيه مصري)</label>
                                <input type="number" class="form-control" id="orderAmount" step="0.01" min="1" required>
                            </div>
                            <div class="mb-3">
                                <label for="orderDescription" class="form-label">وصف الطلب (اختياري)</label>
                                <textarea class="form-control" id="orderDescription" rows="2"></textarea>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-custom text-white">
                                    <i class="fas fa-paper-plane"></i> إرسال رابط الدفع
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="card mt-4">
                    <div class="card-header bg-success text-white">
                        <h4 class="mb-0"><i class="fas fa-history"></i> الطلبات الأخيرة</h4>
                    </div>
                    <div class="card-body">
                        <div id="ordersList">
                            <p class="text-center text-muted">جارٍ التحميل...</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Modal للتأكيد -->
    <div class="modal fade" id="successModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header bg-success text-white">
                    <h5 class="modal-title"><i class="fas fa-check-circle"></i> تم الإرسال بنجاح</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p id="successMessage"></p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إغلاق</button>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('orderForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const submitBtn = document.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> جاري الإرسال...';
            submitBtn.disabled = true;

            const formData = {
                customer_name: document.getElementById('customerName').value,
                customer_phone: document.getElementById('customerPhone').value,
                amount: document.getElementById('orderAmount').value,
                description: document.getElementById('orderDescription').value
            };
            try {
                const response = await fetch('/api/create_order', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                const result = await response.json();
                if (result.success) {
                    document.getElementById('successMessage').innerHTML = `
                        ✅ تم إرسال رابط الدفع بنجاح!<br>
                        <strong>رقم الطلب:</strong> ${result.order_id}<br>
                        <strong>العميل:</strong> ${formData.customer_name}
                    `;
                    new bootstrap.Modal(document.getElementById('successModal')).show();
                    document.getElementById('orderForm').reset();
                    loadOrders(); // تحديث قائمة الطلبات
                } else {
                    alert('حدث خطأ: ' + result.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('حدث خطأ في الاتصال بالخادم');
            } finally {
                 submitBtn.innerHTML = originalText;
                 submitBtn.disabled = false;
            }
        });

        async function loadOrders() {
            try {
                const response = await fetch('/api/orders');
                const orders = await response.json();
                let ordersHtml = '';
                if (Object.keys(orders).length === 0) {
                    ordersHtml = '<p class="text-center text-muted">لا توجد طلبات بعد</p>';
                } else {
                    // عرض آخر 10 طلبات فقط
                    const entries = Object.entries(orders);
                    const recentOrders = entries.slice(-10); // Get last 10 entries
                    recentOrders.reverse().forEach(([orderId, order]) => {
                        ordersHtml += `
                            <div class="border rounded p-3 mb-2">
                                <div class="d-flex justify-content-between">
                                    <strong>${orderId}</strong>
                                    <span class="badge bg-${order.status === 'paid' ? 'success' : 'warning'}">
                                        ${order.status === 'paid' ? 'مدفوع' : 'معلق'}
                                    </span>
                                </div>
                                <div class="mt-2">
                                    <small class="text-muted">${order.customer_name}</small><br>
                                    <strong>${order.amount} جنيه</strong>
                                </div>
                            </div>
                        `;
                    });
                }
                document.getElementById('ordersList').innerHTML = ordersHtml;
            } catch (error) {
                console.error('Error loading orders:', error);
                document.getElementById('ordersList').innerHTML = '<p class="text-center text-danger">خطأ في تحميل الطلبات</p>';
            }
        }

        // تحميل الطلبات عند فتح الصفحة
        document.addEventListener('DOMContentLoaded', (event) => {
            loadOrders();
            // تحديث الطلبات كل 15 ثانية
            setInterval(loadOrders, 15000);
        });
    </script>
</body>
</html>
'''

@app.route('/api/create_order', methods=['POST'])
def create_order():
    """إنشاء طلب جديد وإرسال رابط الدفع"""
    try:
        data = request.get_json()
        customer_name = data.get('customer_name', '')
        customer_phone = data.get('customer_phone', '')
        amount = data.get('amount', '')
        description = data.get('description', '')

        if not all([customer_name, customer_phone, amount]):
            return jsonify({'success': False, 'message': 'جميع الحقول مطلوبة'})

        # إنشاء رقم طلب فريد
        order_id = generate_order_id()

        # حفظ الطلب
        orders = load_orders()
        orders[order_id] = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'amount': float(amount),
            'description': description,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        save_orders(orders)

        # إرسال رابط الدفع
        success = send_whatsapp_payment(customer_phone, customer_name, order_id, amount, description)
        if success:
            return jsonify({
                'success': True,
                'message': 'تم إرسال رابط الدفع بنجاح',
                'order_id': order_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'حدث خطأ في إرسال رابط الدفع'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'حدث خطأ: {str(e)}'
        })

@app.route('/api/orders')
def get_orders():
    """الحصول على جميع الطلبات"""
    return jsonify(load_orders())

@app.route('/api/webhook/vodafone', methods=['POST'])
def vodafone_webhook():
    """Webhook لمعالجة رسائل فودافون كاش"""
    # هذا سيتم تنفيذه لاحقًا مع MicroDroid
    print("🔔 Webhook received!")
    print(request.get_json())
    return jsonify({'status': 'received'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
