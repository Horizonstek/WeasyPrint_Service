
## دليل الاستخدام بالعربية

### آلية إنشاء التقارير

1. اختيار القالب: كل تقرير مرتبط بملف داخل `templates/`. حدد `template_name` المناسب (مثل `salary.html` أو `classic_report.html`).
2. تجهيز البيانات: اكتب حمولة JSON تطابق الحقول المستخدمة داخل القالب (جداول، بطاقات، ملاحظات...). لا حاجة لإرسال أرقام الصفحات لأن الرأس/التذييل يحسبان تلقائياً.
3. الاستدعاء: أرسل طلب `POST` إلى المسار `/WeasyPrint/report` مع ترويسة `X-API-Key` وقيمة `PDF_SERVICE_API_KEY` المخزّنة في `.env`.
4. الاستلام والتخزين: استلم استجابة PDF (بايتات) واحفظها كملف أو أرجعها للعميل. يمكن تكرار الخطوات لكل قالب أو جدولة الاستدعاء آلياً.

### الربط مع Oracle APEX

يوفّر Oracle APEX طبقة REST وPL/SQL يمكنها جمع البيانات وتحويلها إلى JSON قبل إرسالها لخدمة الطباعة.

#### 1. تجهيز مصادر البيانات
- أنشئ REST Data Source أو View يجمع البيانات المطلوبة للتقرير (موظفين، فواتير...).
- استخدم Dynamic Actions أو Job مجدول لتجميع الحقول بنفس البنية المتوقعة في حمولة JSON الخاصة بالقالب.

#### 2. تنفيذ الاستدعاء من APEX
استخدم حزمة `APEX_WEB_SERVICE` لإرسال الطلب واستلام PDF. مثال مبسّط:

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
  apex_web_service.set_request_headers(
    p_name  => 'Content-Type',
    p_value => 'application/json'
  );
  apex_web_service.set_request_headers(
    p_name  => 'X-API-Key',
    p_value => :PDF_SERVICE_API_KEY -- خزّن القيمة في متغير تطبيق
  );

  l_response := apex_web_service.make_rest_request_b(
    p_url         => 'https://your-domain/WeasyPrint/report',
    p_http_method => 'POST',
    p_body        => l_payload
  );

  -- احفظ المخرجات في جدول أو أعدها كملف للمستخدم
  insert into pdf_store(id, file_name, pdf_blob)
  values(pdf_seq.nextval, 'billing.pdf', l_response);
  commit;
end;
/
```

#### 3. توزيع التقرير داخل APEX
- استخدم `APEX_APPLICATION_TEMP_FILES` أو جداولك الخاصة لخزن الـ BLOB ثم اعرضه عبر `apex_util.get_blob_file_src`.
- يمكن ربط الاستدعاء بزر "توليد PDF"، أو تشغيله ليلاً باستخدام `DBMS_SCHEDULER` وتوزيع الملفات بالبريد.

#### 4. أفضل الممارسات
- صمّم طبقة تحويل (PL/SQL أو APEX Automation) لتطابق بنية JSON مع كل قالب.
- فعّل التحقق من مفتاح الـ API داخل FastAPI (موجود بالفعل) وقيّد عناوين IP المطلوبة.
- راقب زمن التنفيذ داخل APEX، وإذا زادت الحمولات استخدم قوائم انتظار وجدولة لتفادي حظر الجلسات.
