<p align="center">
  <a href="arabic-doc.md" style="display:inline-block;padding:10px 18px;border-radius:6px;background:#1a73e8;color:#fff;text-decoration:none;font-weight:600;">
    دليل الاستخدام باللغة العربية
  </a>
</p>

# Universal PDF Rendering Service

FastAPI microservice that turns HTML templates into PDFs with Jinja2 + WeasyPrint. Ships with multiple Arabic RTL templates (salary statement, performance summary, departmental dashboard, billing statement, classic single-page briefing) plus ready-to-extend static assets.

## Requirements

- Python 3.10+
- Cairo/Pango/GTK libraries required by WeasyPrint. Debian/Ubuntu example:

```bash
sudo apt-get update && sudo apt-get install -y \
  libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
  libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

Download Cairo font files (e.g., Cairo-Regular.ttf / Cairo-Bold.ttf) into `static/fonts/`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate # or venv\Scripts\activate.bat
pip install -r requirements.txt
cp .env.example .env
```

Set `PDF_SERVICE_API_KEY=<your-secret>` inside `.env` before starting the API.

## Run locally

```bash
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive docs. Headers and footers repeat on every PDF page automatically (with true `page / pages` counters), so you no longer need to pass `page_number` or `total_pages` in the payload.

## Render a PDF

```bash
curl -X POST http://127.0.0.1:8000/WeasyPrint/report \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{
        "template_name": "billing_statement.html",
        "data": {"...": "..."}
      }' \
  --output pdfs/bill.pdf
```

## Available templates

| Template | Description |
| --- | --- |
| `salary.html` | Modern Arabic salary slip with optional extended rows for multi-page totals. |
| `performance_summary.html` | KPI-focused narrative report without tables (cards, highlights, timelines). |
| `department_overview.html` | Department health dashboard with dense tables + risk/initiative grids. |
| `billing_statement.html` | Invoice/billing design with parties, line items, and totals. |
| `classic_report.html` | Classic A4 summary packed with metrics, dense tables, and activity log on one page. |

## Sample payloads for multi-page testing

Each payload packs large arrays to force multi-page output when rendered as PDF. Replace the `X-API-Key` header with your key.

### `salary.html`

```bash
curl -X POST http://127.0.0.1:8000/WeasyPrint/report \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{
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
            {"category": "مكافآت", "description": "فوز فريق التحول", "amount": "900 SAR"},
            {"category": "مزايا", "description": "برنامج ولاء", "amount": "420 SAR"},
            {"category": "خصومات", "description": "مخالفة موارد", "amount": "80 SAR"},
            {"category": "بدلات", "description": "تنقل إقليمي", "amount": "1,350 SAR"}
          ]
        }
      }' \
  --output pdfs/salary.pdf
```

### `performance_summary.html`

```bash
curl -X POST http://127.0.0.1:8000/WeasyPrint/report \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{
        "template_name": "performance_summary.html",
        "data": {
          "report_title": "ملخص الأداء التشغيلي",
          "report_period": "الربع الثالث 2025",
          "executive_summary": "سجلت الفرق نمواً مستمراً في الإيرادات مع تحسن في زمن إنجاز المشاريع بنسبة 12%.",
          "kpi_cards": [
            {"label": "نسبة الإنجاز", "value": "92%", "trend": "+4%"},
            {"label": "رضا العملاء", "value": "4.6/5", "trend": "+0.3"},
            {"label": "سرعة التسليم", "value": "6 أيام", "trend": "-2 أيام"},
            {"label": "الإيرادات المتكررة", "value": "18M SAR", "trend": "+9%"}
          ],
          "highlights": [
            "توقيع ثلاث شراكات استراتيجية جديدة",
            "رفع نسبة التحول الرقمي إلى 80%",
            "إطلاق نسخة تجريبية من منصة التحليلات",
            "اكتمال تدريب 250 موظفاً على أدوات الذكاء الاصطناعي",
            "تحسين مؤشر رضا الموظفين إلى 87%",
            "استقطاب 14 موهبة حرجة في الأمن السيبراني",
            "نشر 40 روبوت أتمتة مكتبي",
            "تخفيض تكاليف البنية التحتية 11%"
          ],
          "milestones": [
            {"title": "إطلاق مركز البيانات", "date": "15 سبتمبر", "status": "منجز"},
            {"title": "اعتماد ميزانية 2026", "date": "02 أكتوبر", "status": "قيد الموافقات"},
            {"title": "تدشين تجربة العملاء الجديدة", "date": "28 أكتوبر", "status": "ضمن الخطة"},
            {"title": "دمج أنظمة الفوترة", "date": "10 نوفمبر", "status": "تحت الاختبار"},
            {"title": "توسيع مركز الذكاء الاصطناعي", "date": "25 نوفمبر", "status": "قيد الإطلاق"}
          ],
          "next_steps": [
            {"action": "توسيع قدرات الأتمتة", "owner": "فريق التحول", "deadline": "ديسمبر 2025"},
            {"action": "إغلاق العقود الدولية", "owner": "المبيعات", "deadline": "يناير 2026"},
            {"action": "إطلاق برنامج ولاء العملاء", "owner": "التسويق", "deadline": "فبراير 2026"},
            {"action": "تحسين مؤشرات الجودة", "owner": "العمليات", "deadline": "مارس 2026"},
            {"action": "اختبار منصة التحليلات", "owner": "الهندسة", "deadline": "أبريل 2026"}
          ],
          "footer_note": "سري - للاستخدام الداخلي فقط"
        }
      }' \
  --output pdfs/performance.pdf
```

### `department_overview.html`

```bash
curl -X POST http://127.0.0.1:8000/WeasyPrint/report \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{
        "template_name": "department_overview.html",
        "data": {
          "report_title": "لوحة متابعة الأقسام",
          "report_period": "أسبوع 48 - 2025",
          "departments": [
            {"name": "الهندسة", "headcount": 48, "budget": "5.2M SAR", "spend": "3.9M SAR", "compliance": "75%", "status_label": "ضمن الخطة", "status_class": "status-success"},
            {"name": "التحول الرقمي", "headcount": 32, "budget": "3.1M SAR", "spend": "2.8M SAR", "compliance": "88%", "status_label": "مراقبة", "status_class": "status-warning"},
            {"name": "التشغيل", "headcount": 60, "budget": "4.4M SAR", "spend": "4.2M SAR", "compliance": "96%", "status_label": "خطر إنفاق", "status_class": "status-risk"},
            {"name": "الأمن السيبراني", "headcount": 22, "budget": "2.7M SAR", "spend": "1.9M SAR", "compliance": "70%", "status_label": "تسارع التوظيف", "status_class": "status-warning"},
            {"name": "الموارد البشرية", "headcount": 28, "budget": "1.4M SAR", "spend": "0.9M SAR", "compliance": "65%", "status_label": "يحتاج تحسين", "status_class": "status-warning"}
          ],
          "risks": [
            {"title": "تأخر مورد الأجهزة", "owner": "المشتريات", "impact": "متوسط"},
            {"title": "نقص خبرات سحابة", "owner": "الهندسة", "impact": "مرتفع"},
            {"title": "قيود بيانات تشريعية", "owner": "الامتثال", "impact": "مرتفع"},
            {"title": "تبدل سياسات استضافة", "owner": "البنية التحتية", "impact": "منخفض"}
          ],
          "initiatives": [
            {"title": "أتمتة مركز الاتصال", "description": "نشر روبوت محادثة عربي بخدمة ذاتية", "owner": "العمليات", "status": "قيد التنفيذ"},
            {"title": "لوحة مراقبة السحابة", "description": "تجميع مؤشرات التكلفة والأداء في واجهة واحدة", "owner": "الهندسة", "status": "تحت التطوير"},
            {"title": "برنامج توطين الخبرات", "description": "تعيين 20 خبيراً في الذكاء الاصطناعي", "owner": "الموارد البشرية", "status": "حسب الخطة"},
            {"title": "ترقية منظومة الأمن", "description": "تطبيق مراقبة لحظية للثغرات", "owner": "الأمن السيبراني", "status": "قيد الشراء"}
          ],
          "footer_note": "تحديث أسبوعي للقيادة التنفيذية"
        }
      }' \
  --output pdfs/departments.pdf
```

### `billing_statement.html`

```bash
curl -X POST http://127.0.0.1:8000/WeasyPrint/report \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{
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
            "email": "finance@horizonstek.com"
          },
          "bill_to": {
            "name": "مؤسسة البيان التجارية",
            "address": "جدة، حي الزهراء، مبنى 8",
            "vat": "302998877100009",
            "phone": "+966 12 223 4411",
            "email": "accounts@albayan.sa"
          },
          "line_items": [
            {"description": "باقة الاستشارات الاستراتيجية", "quantity": 1, "unit_price": "25,000 SAR", "total": "25,000 SAR"},
            {"description": "تطوير رحلة عميل متعددة القنوات", "quantity": 1, "unit_price": "18,000 SAR", "total": "18,000 SAR"},
            {"description": "دمج الأنظمة الخلفية", "quantity": 80, "unit_price": "350 SAR", "total": "28,000 SAR"},
            {"description": "ساعات دعم ميداني إضافية", "quantity": 12, "unit_price": "250 SAR", "total": "3,000 SAR"},
            {"description": "اشتراك منصة التحليلات", "quantity": 6, "unit_price": "500 SAR", "total": "3,000 SAR"}
          ],
          "totals": {
            "subtotal": "77,000 SAR",
            "tax": "11,550 SAR",
            "discount": "-4,000 SAR",
            "total_due": "84,550 SAR"
          },
          "notes": "تم احتساب ساعات الدعم بناءً على جداول الحضور، وتشمل الأسعار تكاليف السفر.",
          "payment_terms": "الدفع خلال 15 يوماً عبر التحويل البنكي",
          "footer_message": "شكراً لتعاونكم مع فريق الأفق"
        }
      }' \
  --output pdfs/billing.pdf
```

### `classic_report.html`

```bash
curl -X POST http://127.0.0.1:8000/WeasyPrint/report \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{
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
            {"label": "التوافر", "value": "99.2%", "trend": "+0.4%"}
          ],
          "summary_table": [
            {"section": "الدعم", "target": "1,200 تذكرة", "actual": "1,320", "variance": "+10%", "status": "ممتاز", "badge_class": "badge-success"},
            {"section": "المشاريع", "target": "15", "actual": "12", "variance": "-3", "status": "مراقبة", "badge_class": "badge-watch"},
            {"section": "التوفر", "target": "99%", "actual": "98.2%", "variance": "-0.8%", "status": "خطر", "badge_class": "badge-risk"}
          ],
          "activities": [
            {"title": "إطلاق منصة الموردين", "time": "الأسبوع 44", "owner": "PMO", "detail": "اكتمل تدريب 60 مورداً مع مؤشرات رضا 4.7/5."},
            {"title": "مراقبة الحوادث", "time": "الأسبوع 45", "owner": "الأمن السيبراني", "detail": "تم احتواء حادثين خلال 28 دقيقة بمتوسط أقل من الهدف."},
            {"title": "تحسين رحلة العميل", "time": "الأسبوع 46", "owner": "التجربة", "detail": "جرى تقليص خطوات التسجيل من 7 إلى 4 خطوات."}
          ],
          "notes": [
            "ينبغي اعتماد نموذج التنبؤ بالطلب قبل نهاية الربع.",
            "الاستفادة من مكاتب البيانات لتقليل دورة اتخاذ القرار",
            "الاستعداد لإطلاق مركز مراقبة موحد في يناير"
          ],
          "footer_note": "سري - للاستخدام الداخلي"
        }
      }' \
  --output pdfs/classic.pdf
```








### `model_report.html`

```bash
curl -X POST http://127.0.0.1:8000/WeasyPrint/report \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{
    "template_name": "model_report.html",
    "data": {
        "ar_company_main": "شركة مصانع الخير للخياطة",
        "ar_company_sub": "شركة مصانع الخير للخياطة",
        "ar_branch": "الرياض فرع 1",

        "en_company_main": "Default Main Company",
        "en_company_sub": "Default Sub Company",
        "en_branch": "1 Branch",

        "vat_no": "1",
        "cr_no": "2",

        "title": "الموديلات",

        "printed_by": "مدير النظام",
        "print_datetime": "01/12/2025 04:41 PM",

        "models": [
        {"id": 1, "name_ar": "سعودي", "name_en": "Saudi", "notes": ""},
        {"id": 2, "name_ar": "عماني", "name_en": "Omani", "notes": ""},
        {"id": 3, "name_ar": "بحريني", "name_en": "Bahraini", "notes": ""},
        {"id": 4, "name_ar": "اماراتي", "name_en": "Emirati", "notes": ""},
        {"id": 5, "name_ar": "فرنسي", "name_en": "", "notes": ""},
        {"id": 6, "name_ar": "توصيل", "name_en": "", "notes": ""},
        {"id": 7, "name_ar": "تغليف", "name_en": "", "notes": ""}
        ]
    }
    }' \
  --output pdfs/model_report.pdf
```






## Project layout

```
main.py                         FastAPI application entrypoint
templates/salary.html           Arabic salary slip (header/footer + optional detail table)
templates/performance_summary.html  Narrative KPI summary without tables
templates/department_overview.html  Department health dashboard with data tables
templates/billing_statement.html    Bill/invoice design with line items
templates/classic_report.html       Classic dense A4 snapshot
static/css/report.css           Styles for salary template
static/css/performance.css      Styles for performance summary
static/css/department.css       Styles for department dashboard
static/css/billing.css          Styles for billing statement
static/css/classic.css          Styles for the classic dense report
static/fonts/                   Place Cairo font files here
tests/test_render.py            FastAPI TestClient coverage for every template
```

Add more templates under `templates/` and reference them via `template_name`.

## Testing

```bash
pytest
```