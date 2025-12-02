
## دليل الاستخدام الشامل (العربية)

يغطي هذا الدليل كل ما تحتاجه لتشغيل خدمة **تحويل القوالب HTML إلى ملفات PDF**، إضافة قوالب جديدة، اختبار الخدمة، وربطها مع أنظمة خارجية مثل Oracle APEX.

---

### 1. المتطلبات المسبقة

- **Python 3.10+** وبيئة عمل افتراضية مفعّلة.
- مكتبات الرسم المطلوبة من WeasyPrint (Cairo / Pango / GTK). على توزيعة Debian/Ubuntu:

  ```bash
  sudo apt-get update && sudo apt-get install -y \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
  ```

- خطوط عربية مثل عائلة **Cairo** داخل `static/fonts/`.
- ملف بيئة `.env` يحتوي على `PDF_SERVICE_API_KEY` وقيم الاتصال الأخرى.

---

### 2. تثبيت المشروع وتشغيله محلياً

```bash
git clone <repo-url>
cd print_service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # أو أنشئ الملف يدوياً
uvicorn main:app --reload
```

- الواجهة التفاعلية متاحة في `http://127.0.0.1:8000/docs`.
- التوفر الصحي عبر `GET /WeasyPrint/health`.

---

### 3. بنية المشروع الأساسية

```
main.py                   تطبيق FastAPI وتهيئة WeasyPrint
templates/*               قوالب Jinja2 لكل تقرير
static/css/*.css          أنماط كل قالب على حدة
static/fonts/             الخطوط المستخدمة داخل التقارير
pdfs/                     مجلد حفظ الملفات المُولَّدة محلياً (مستثنى من git)
tests/test_render.py      تغطية اختبارية لكل قالب
arabic-doc.md             هذا الدليل
```

---

### 4. كيفية عمل الخدمة

1. الطلب يُرسل إلى `/WeasyPrint/report` مع JSON يحتوي على `template_name` و`data`.
2. الخدمة تتحقق من مفتاح واجهة البرمجة عبر الترويسة `X-API-Key`.
3. يتم تحميل القالب من `templates/` وتمرير البيانات إلى Jinja2.
4. يتم تحويل HTML الناتج إلى PDF باستخدام WeasyPrint مع إمكانية الوصول للملفات الثابتة تحت `static/`.

#### مثال طلب `curl`

```bash
curl -X POST http://127.0.0.1:8000/WeasyPrint/report \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{
        "template_name": "billing_statement.html",
        "data": {"report_title": "فاتورة خدمات", "line_items": []}
      }' \
  --output pdfs/billing.pdf
```

---

### 5. إنشاء أو تعديل القوالب

#### 5.1 خطوات سريعة لإضافة قالب جديد

1. **نسخ قالب موجود** إلى ملف جديد داخل `templates/` (مثلاً `project_overview.html`).
2. تعديل الهيكل باستخدام Jinja2 (كتل `{% for %}`، تعبيرات `{{ variable }}`، تنسيقات التواريخ...).
3. إنشاء ملف CSS مرافق داخل `static/css/` أو إعادة استخدام أحد الملفات الموجودة إذا كان التصميم مشابهاً.
4. إضافة أي صور أو خطوط مطلوبة داخل `static/` واستخدام مسارات نسبية.
5. تحديث `README.md` و/أو هذا الدليل بقسم جديد يصف البيانات المطلوبة.
6. إنشاء حمولة JSON تجريبية كبيرة لضمان أن القالب يدعم الصفحات المتعددة.
7. تشغيل الاختبارات أو أمر `curl` للتأكد من أن PDF الناتج متوافق مع التوقعات.

#### 5.2 أفضل الممارسات في القوالب

- احتفظ بالرأس والتذييل داخل القالب ليستفيد من عداد الصفحات التلقائي.
- استخدم صناديق Flex أو Grid لضمان التوافق مع اتجاه الكتابة من اليمين لليسار.
- عرّف المتغيرات الحرجة (مثل العناوين، التواريخ، القوائم) في أعلى القالب باستخدام تعليقات HTML لتوثيقها.
- استخدم فئات CSS واضحة (مثل `.status-success`, `.status-warning`) لإعادة التدوير بين القوالب.

#### 5.3 تحديث ملف CSS

- استورد الخطوط داخل CSS (`@font-face`) إذا كانت خارج النظام.
- ضع القواعد الخاصة بالقالب فقط داخل ملفه لتجنب التعارضات.
- استخدم وحدات متجاوبة (مثل `rem`, `vh`) لتقليل مشاكل القص عند التحويل إلى PDF.

---

### 6. تصميم حمولة البيانات (JSON)

- كل قالب يحتوي على مجموعة مفاتيح يجب مطابقتها في `data`.
- استخدم أسماء مفاتيح واضحة باللغة الإنجليزية للحفاظ على سهولة الصيانة (`report_title`, `line_items`, `footer_note`).
- القوائم الكبيرة (مثل العناصر أو السجلات) يجب أن تُرسل كمصفوفات من كائنات.
- يمكن تضمين نصوص عربية مباشرة؛ WeasyPrint يدعم UTF-8 بالكامل.

جدول مصغّر للحقول الشائعة:

| القالب | أهم الحقول |
| --- | --- |
| `salary.html` | `employee_name`, `salary_items[]`, `net_salary` |
| `performance_summary.html` | `kpi_cards[]`, `highlights[]`, `next_steps[]` |
| `department_overview.html` | `departments[]`, `risks[]`, `initiatives[]` |
| `billing_statement.html` | `bill_from`, `bill_to`, `line_items[]`, `totals` |
| `classic_report.html` | `stat_cards[]`, `summary_table[]`, `activities[]` |
| `model_report.html` | `models[]`, `print_datetime`, `company metadata` |

---

### 7. الاختبارات وضمان الجودة

- استخدم `pytest` لتشغيل الاختبارات الموجودة في `tests/test_render.py`، والتي تتأكد من أن كل قالب يُحوَّل بنجاح ولا يُرجع أخطاء HTTP.
- أضف حالات اختبار جديدة إذا أنشأت قالباً إضافياً (أنشئ بيانات عينة وفعّل الاستدعاء داخل الاختبار).
- تفقد مجلد `pdfs/` بعد كل تعديل للتأكد بصرياً من النتيجة.

```bash
pytest
```

---

### 8. نصائح الأمان والإعدادات

- لا ترفع الملف `.env` إلى المستودع؛ يتم استبعاده عبر `.gitignore`.
- قم بتدوير قيمة `PDF_SERVICE_API_KEY` بانتظام، واستخدم أسرار بيئة المنصة في الإنتاج (مثل GitHub Actions أو Docker Secrets).
- حدّد قائمة القوالب المسموح بها إذا كنت لا ترغب في قبول أسماء ملفات عشوائية (يمكن إضافة تحقق إضافي داخل `main.py`).

---

### 9. التكامل مع Oracle APEX

يمكن لـ Oracle APEX تحضير البيانات واستدعاء الخدمة لإنتاج PDF، ثم تخزينه أو عرضه للمستخدم.

#### 9.1 تجهيز مصادر البيانات

- أنشئ REST Data Source أو View تُجمِّع البيانات المطلوبة.
- استخدم Dynamic Actions أو Jobs لتجهيز حمولة JSON بنفس بنية القالب.

#### 9.2 مثال PL/SQL كامل

```plsql
declare
  l_payload   clob := json_object(
                    'template_name' value 'billing_statement.html',
                    'data' value json_object(
                      'report_title' value 'فاتورة خدمات' )
                  );
  l_response  blob;
begin
  apex_web_service.g_request_headers.delete;
  apex_web_service.set_request_headers('Content-Type', 'application/json');
  apex_web_service.set_request_headers('X-API-Key', :PDF_SERVICE_API_KEY);

  l_response := apex_web_service.make_rest_request_b(
    p_url         => 'https://your-domain/WeasyPrint/report',
    p_http_method => 'POST',
    p_body        => l_payload
  );

  insert into pdf_store(id, file_name, pdf_blob)
  values(pdf_seq.nextval, 'billing.pdf', l_response);
  commit;
end;
/
```

يمكن بعد ذلك إرجاع الـ BLOB كملف للمستخدم عبر `APEX_UTIL.GET_PRINT_DOCUMENT` أو صفحة تحميل مخصصة.

---

### 10. استكشاف الأخطاء الشائعة

| المشكلة | السبب المحتمل | الحل |
| --- | --- | --- |
| `401 Unauthorized` | قيمة `X-API-Key` غير صحيحة | تأكد من قراءة القيمة من `.env` أو من إعداد المنصة |
| `TemplateNotFound` | اسم الملف غير موجود أو الامتداد خطأ | تحقق من `templates/` وأنالاسم مطابق تماماً |
| حروف عربية غير واضحة | الخط غير محمّل أو CSS لا يشير إليه | أضف الخط إلى `static/fonts/` وتأكد من تعريفه في CSS |
| عناصر تتجاوز الصفحة | جداول طويلة بدون تقسيم | استخدم `page-break-inside: avoid` أو قسّم الجدول إلى صفحات |

---

### 11. نشر الخدمة

- يمكن نشر التطبيق عبر Docker أو خدمة PaaS مثل Render / Azure / Railway.
- تأكد من تثبيت مكتبات Cairo/Pango في الصورة أو البيئة المستهدفة.
- استخدم `uvicorn main:app --host 0.0.0.0 --port 8000` داخل خدمة النظام أو ملف Dockerfile.

---

### 12. خارطة طريق مقترحة

- إضافة دعم تحميل ملفات (صور، شعارات) عبر تخزين خارجي مثل S3 بدلاً من `static/` المحلي.
- إنشاء نقطة نهاية لإرجاع قائمة القوالب المتاحة.
- دعم الترجمة الثنائية داخل القالب الواحد باستخدام كتل شرطية في Jinja2.

بهذا الدليل يمكنك تشغيل الخدمة end-to-end، إضافة قوالب جديدة بثقة، ودمجها في منظومة تقاريرك بدون الحاجة للرجوع إلى ملفات أخرى.