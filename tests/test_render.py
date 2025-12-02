from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main import app, settings

client = TestClient(app)

SAMPLE_PAYLOADS = [
    {
        "template_name": "salary.html",
        "data": {
            "report_title": "تقرير الرواتب",
            "report_period": "الربع الرابع 2025",
            "employee_name": "أحمد الزهراني",
            "employee_id": "EMP-1022",
            "department": "المالية",
            "basic_salary": "8,000 SAR",
            "allowances": "1,750 SAR",
            "deductions": "550 SAR",
            "net_salary": "9,200 SAR",
            "report_date": "01/12/2025",
            "salary_items": [
                {"category": "بدلات", "description": "بدل سكن - الربع الرابع", "amount": "6,000 SAR"},
                {"category": "بدلات", "description": "بدل نقل", "amount": "1,200 SAR"},
                {"category": "مكافآت", "description": "مكافأة مشاريع خاصة", "amount": "2,500 SAR"},
                {"category": "خصومات", "description": "سلفة سابقة", "amount": "300 SAR"},
                {"category": "خصومات", "description": "اشتراك تأمين صحي", "amount": "150 SAR"},
                {"category": "مزايا", "description": "دعم تعليم الأبناء", "amount": "750 SAR"},
                {"category": "مزايا", "description": "مكافأة استثنائية", "amount": "1,100 SAR"},
                {"category": "خصومات", "description": "تأخير حضور (5 أيام)", "amount": "100 SAR"},
            ],
        },
    },
    {
        "template_name": "performance_summary.html",
        "data": {
            "report_title": "ملخص الأداء التشغيلي",
            "report_period": "الربع الثالث 2025",
            "executive_summary": "سجلت الفرق نمواً مستمراً في الإيرادات مع تحسن في زمن إنجاز المشاريع بنسبة 12%.",
            "kpi_cards": [
                {"label": "نسبة الإنجاز", "value": "92%", "trend": "+4%"},
                {"label": "رضا العملاء", "value": "4.6/5", "trend": "+0.3"},
                {"label": "سرعة التسليم", "value": "6 أيام", "trend": "-2 أيام"},
                {"label": "الإيرادات المتكررة", "value": "18M SAR", "trend": "+9%"},
            ],
            "highlights": [
                "توقيع ثلاث شراكات استراتيجية جديدة",
                "رفع نسبة التحول الرقمي في مراكز الخدمة إلى 80%",
                "إطلاق نسخة تجريبية من منصة التحليلات",
                "اكتمال تدريب 250 موظفاً على أدوات الذكاء الاصطناعي",
                "تحسين مؤشر رضا الموظفين إلى 87%",
                "استقطاب 14 موهبة حرجة في الأمن السيبراني",
            ],
            "milestones": [
                {"title": "إطلاق مركز البيانات", "date": "15 سبتمبر", "status": "منجز"},
                {"title": "اعتماد ميزانية 2026", "date": "02 أكتوبر", "status": "قيد الموافقات"},
                {"title": "تدشين تجربة العملاء الجديدة", "date": "28 أكتوبر", "status": "ضمن الخطة"},
                {"title": "دمج أنظمة الفوترة", "date": "10 نوفمبر", "status": "تحت الاختبار"},
            ],
            "next_steps": [
                {"action": "توسيع قدرات الأتمتة", "owner": "فريق التحول", "deadline": "ديسمبر 2025"},
                {"action": "إغلاق العقود الدولية", "owner": "المبيعات", "deadline": "يناير 2026"},
                {"action": "إطلاق برنامج ولاء العملاء", "owner": "التسويق", "deadline": "فبراير 2026"},
                {"action": "تحسين مؤشرات الجودة", "owner": "العمليات", "deadline": "مارس 2026"},
            ],
            "footer_note": "سري - للاستخدام الداخلي فقط",
        },
    },
    {
        "template_name": "department_overview.html",
        "data": {
            "report_title": "لوحة متابعة الأقسام",
            "report_period": "أسبوع 48 - 2025",
            "departments": [
                {
                    "name": "الهندسة",
                    "headcount": 48,
                    "budget": "5.2M SAR",
                    "spend": "3.9M SAR",
                    "compliance": "75%",
                    "status_label": "ضمن الخطة",
                    "status_class": "status-success",
                },
                {
                    "name": "التحول الرقمي",
                    "headcount": 32,
                    "budget": "3.1M SAR",
                    "spend": "2.8M SAR",
                    "compliance": "88%",
                    "status_label": "مراقبة",
                    "status_class": "status-warning",
                },
                {
                    "name": "التشغيل",
                    "headcount": 60,
                    "budget": "4.4M SAR",
                    "spend": "4.2M SAR",
                    "compliance": "96%",
                    "status_label": "خطر إنفاق",
                    "status_class": "status-risk",
                },
                {
                    "name": "الأمن السيبراني",
                    "headcount": 22,
                    "budget": "2.7M SAR",
                    "spend": "1.9M SAR",
                    "compliance": "70%",
                    "status_label": "تسارع التوظيف",
                    "status_class": "status-warning",
                },
            ],
            "risks": [
                {"title": "تأخر مورد الأجهزة", "owner": "المشتريات", "impact": "متوسط"},
                {"title": "نقص خبرات سحابة", "owner": "الهندسة", "impact": "مرتفع"},
                {"title": "قيود بيانات تشريعية", "owner": "الامتثال", "impact": "مرتفع"},
                {"title": "تبدل سياسات استضافة", "owner": "البنية التحتية", "impact": "منخفض"},
            ],
            "initiatives": [
                {
                    "title": "أتمتة مركز الاتصال",
                    "description": "نشر روبوت محادثة عربي بخدمة ذاتية",
                    "owner": "العمليات",
                    "status": "قيد التنفيذ",
                },
                {
                    "title": "لوحة مراقبة السحابة",
                    "description": "تجميع مؤشرات التكلفة والأداء في واجهة واحدة",
                    "owner": "الهندسة",
                    "status": "تحت التطوير",
                },
                {
                    "title": "برنامج توطين الخبرات",
                    "description": "تعيين 20 خبيراً في الذكاء الاصطناعي",
                    "owner": "الموارد البشرية",
                    "status": "حسب الخطة",
                },
            ],
            "footer_note": "تحديث أسبوعي للقيادة التنفيذية",
        },
    },
    {
        "template_name": "billing_statement.html",
        "data": {
            "report_title": "فاتورة خدمات التحول الرقمي",
            "invoice_number": "INV-2025-044",
            "issue_date": "01/12/2025",
            "due_date": "15/12/2025",
            "bill_from": {
                "name": "شركة الأفق التقنية",
                "address": "الرياض، شارع العليا، برج 12",
                "vat": "310123456700003",
                "phone": "+966 11 555 2000",
                "email": "finance@horizonstek.com",
            },
            "bill_to": {
                "name": "مؤسسة البيان التجارية",
                "address": "جدة، حي الزهراء، مبنى 8",
                "vat": "302998877100009",
                "phone": "+966 12 223 4411",
                "email": "accounts@albayan.sa",
            },
            "line_items": [
                {
                    "description": "باقة الاستشارات الاستراتيجية",
                    "quantity": 1,
                    "unit_price": "25,000 SAR",
                    "total": "25,000 SAR",
                },
                {
                    "description": "تطوير رحلة عميل متعددة القنوات",
                    "quantity": 1,
                    "unit_price": "18,000 SAR",
                    "total": "18,000 SAR",
                },
                {
                    "description": "دمج الأنظمة الخلفية",
                    "quantity": 80,
                    "unit_price": "350 SAR",
                    "total": "28,000 SAR",
                },
                {
                    "description": "ساعات دعم ميداني إضافية",
                    "quantity": 12,
                    "unit_price": "250 SAR",
                    "total": "3,000 SAR",
                },
            ],
            "totals": {
                "subtotal": "74,000 SAR",
                "tax": "11,100 SAR",
                "discount": "-4,000 SAR",
                "total_due": "81,100 SAR",
            },
            "notes": "تم احتساب ساعات الدعم بناءً على جداول الحضور، وتشمل الأسعار تكاليف السفر.",
            "payment_terms": "الدفع خلال 15 يوماً عبر التحويل البنكي",
            "footer_message": "شكراً لتعاونكم مع فريق الأفق",
        },
    },
    {
        "template_name": "classic_report.html",
        "data": {
            "report_title": "تقرير العمليات الكلاسيكي",
            "report_period": "نوفمبر 2025",
            "prepared_for": "مجلس إدارة الأفق",
            "prepared_by": "مكتب التحول الرقمي",
            "issued_date": "02/12/2025",
            "region": "الرياض",
            "scope": "التحسين التشغيلي",
            "stat_cards": [
                {"label": "طلب مكتمل", "value": "4,820", "trend": "+8%"},
                {"label": "نسبة SLA", "value": "95%", "trend": "+2%"},
                {"label": "تكلفة الوحدة", "value": "38 SAR", "trend": "-4%"},
                {"label": "التوافر", "value": "99.2%", "trend": "+0.4%"},
            ],
            "summary_table": [
                {
                    "section": "الدعم",
                    "target": "1,200 تذكرة",
                    "actual": "1,320",
                    "variance": "+10%",
                    "status": "ممتاز",
                    "badge_class": "badge-success",
                },
                {
                    "section": "المشاريع",
                    "target": "15",
                    "actual": "12",
                    "variance": "-3",
                    "status": "مراقبة",
                    "badge_class": "badge-watch",
                },
                {
                    "section": "التوفر",
                    "target": "99%",
                    "actual": "98.2%",
                    "variance": "-0.8%",
                    "status": "خطر",
                    "badge_class": "badge-risk",
                },
            ],
            "activities": [
                {
                    "title": "إطلاق منصة الموردين",
                    "time": "الأسبوع 44",
                    "owner": "PMO",
                    "detail": "اكتمل تدريب 60 مورداً مع مؤشرات رضا 4.7/5.",
                },
                {
                    "title": "مراقبة الحوادث",
                    "time": "الأسبوع 45",
                    "owner": "الأمن السيبراني",
                    "detail": "تم احتواء حادثين خلال 28 دقيقة بمتوسط أقل من الهدف.",
                },
                {
                    "title": "تحسين رحلة العميل",
                    "time": "الأسبوع 46",
                    "owner": "التجربة",
                    "detail": "جرى تقليص خطوات التسجيل من 7 إلى 4 خطوات.",
                },
            ],
            "notes": [
                "ينبغي اعتماد نموذج التنبؤ بالطلب قبل نهاية الربع.",
                "الاستفادة من مكاتب البيانات لتقليل دورة اتخاذ القرار",
                "الاستعداد لإطلاق مركز مراقبة موحد في يناير",
            ],
            "footer_note": "سري - للاستخدام الداخلي",
        },
    },
]


@pytest.mark.parametrize("payload", SAMPLE_PAYLOADS, ids=[p["template_name"] for p in SAMPLE_PAYLOADS])
def test_templates_render_pdf(payload) -> None:
    response = client.post("/WeasyPrint/report", headers={"X-API-Key": settings.api_key}, json=payload)

    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/pdf"
    assert len(response.content) > 100
