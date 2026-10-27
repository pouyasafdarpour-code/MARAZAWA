"""Build browsable, citation-only public library from the collected metadata."""
from pathlib import Path
import json, re, hashlib
from collect import TOPICS, ROOT

d=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))
records=d['sources']; audit=json.loads((ROOT/'audit.json').read_text(encoding='utf-8'))
for folder in ['topics','data']: (ROOT/folder).mkdir(exist_ok=True)
seeds=[
 ('UN 2030 Agenda','United Nations','https://sdgs.un.org/2030agenda','چارچوب هدف‌های توسعه و پیوند ابعاد اجتماعی، اقتصادی و محیطی.','چارچوب سیاستی است؛ جایگزین شناخت نیاز محلی یا مقررات ایران نیست.'),
 ('AR6 WGIII — Chapter 9: Buildings','IPCC','https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-9/','نقطهٔ شروع مرور ادبیات کاهش انتشار در ساختمان و ارجاع به پژوهش‌های پایه.','صفحه در نتایج رسمی بازیابی شد؛ بازکردن مستقیم این نوبت با 403 مواجه شد. متن کامل در این کار خوانده نشده است.'),
 ('Global Status Report for Buildings and Construction 2025–2026','UNEP / GlobalABC','https://wedocs.unep.org/entities/publication/dd0a1d99-dba3-46da-93ab-ef2a26fc3c14','نمای کلی وضعیت جهانی بخش ساختمان، سیاست و مسیر کاهش انتشار.','مجوز درج‌شده CC BY-NC-ND 3.0 IGO است؛ متن یا تصاویر گزارش وارد محصول تجاری نشده‌اند.'),
 ('International Guidelines on Urban and Territorial Planning','UN-Habitat','https://unhabitat.org/international-guidelines-on-urban-and-territorial-planning','مرجع برنامه‌ریزی فضایی و توجه به دسترسی، شمول و ارتباط سکونتگاه‌ها؛ صفحه، نسخهٔ فارسی را نیز فهرست می‌کند.','راهنمای بین‌المللی است؛ استعلام و طرح مصوب محلی همچنان لازم‌اند.'),
 ('Urban-rural Linkages: Guiding Principles','UN-Habitat','https://unhabitat.org/urban-rural-linkages-guiding-principles','بررسی پیوند خدمات، اقتصاد و حکمرانی شهر و روستا.','به‌جای نگاه جزیره‌ای به یک بنا، روابط منطقه‌ای بررسی شوند؛ دادهٔ واقعی باید محلی تهیه شود.'),
 ('Level(s): A quick introduction','European Commission','https://green-forum.ec.europa.eu/green-business/levels/quick-introduction-levels_en','نقشهٔ شاخص‌های چرخهٔ عمر: کربن، منابع، آب، سلامت، تاب‌آوری و هزینه.','چارچوب اروپایی است؛ به معنی گواهی ساختمان یا انطباق با ضوابط ایران نیست.'),
 ('Energy Efficiency 2025 — Buildings','IEA','https://www.iea.org/reports/energy-efficiency-2025/buildings','مرور سیاست‌ها و موضوعات بهره‌وری انرژی ساختمان و بهسازی موجودی بنا.','آمار جهانی جای قبض، اقلیم و اندازه‌گیری پروژه را نمی‌گیرد؛ متن صفحه مجوز CC BY 4.0 ذکر می‌کند.'),
 ('Breakthrough Agenda Report 2025 — Building','IEA','https://www.iea.org/reports/breakthrough-agenda-report-2025/building','بررسی جهت‌گیری گذار بخش ساختمان و موانع هزینه و اجرا.','روند سیاستی است؛ قیمت یا توجیه مالی پروژهٔ روستایی ایران از آن استخراج نشده است.'),
 ('RuralInvest','FAO Investment Centre','https://www.fao.org/investment-centre/solutions/capacity-development-CD4I/ruralinvest/en','روش مشارکتی برای تهیه و بررسی طرح سرمایه‌گذاری روستایی.','روش، نرم‌افزار و دوره باید مطابق شرایط استفادهٔ خود منبع به کار روند؛ هیچ قرارداد یا تأمین مالی ادعا نمی‌شود.'),
 ('Building Criteria: Passive House, EnerPHit, PHI Low Energy Building','Passive House Institute','https://passivehouse.com/en/home/building-certification/','مرجع رسمی معیارهای ساختمان کم‌مصرف و بهسازی انرژی.','فقط نسخهٔ رسمی و جاری مبناست؛ ارجاع، گواهی یا مجوز استفاده از نشان ایجاد نمی‌کند.'),
 ('Recommendation on the Historic Urban Landscape','UNESCO','https://www.unesco.org/en/legal-affairs/recommendation-historic-urban-landscape-including-glossary-definitions','شناخت لایه‌های فرهنگی و اجتماعی پیش از مداخله در محیط تاریخی.','سند سیاستی است؛ وضعیت میراث و مجوز هر محل باید جدا بررسی شود.'),
 ('IUCN Global Standard for Nature-based Solutions','IUCN','https://iucn.org/our-work/topic/iucn-global-standard-nature-based-solutions','مرجع طراحی، ارزیابی و پایش راهکارهای مبتنی بر طبیعت.','ملاک‌ها و نسخهٔ جاری منبع باید در زمان کاربرد دوباره بررسی شوند؛ برچسب سبز کافی نیست.'),
]
seedrows=[]; seedmd=['# منابع پایه و مسیر مطالعه\n','این ۱۲ مرجع رسمی جدا از شمار مقاله‌های DOIدار هستند. بررسی این نوبت در سطح صفحهٔ معرفی/نمایه بوده است، نه خواندن کامل تمام گزارش‌ها. یادداشت‌های فارسی تألیفی‌اند.\n']
for i,(title,pub,url,use,limit) in enumerate(seeds,1):
 seedrows.append(dict(id=f'FOUND-{i:02d}',title=title,publisher=pub,url=url,use_fa=use,limits_fa=limit,checked='2026-10-27',full_text_archived=False))
 seedmd.append(f'## FOUND-{i:02d} · {title}\n\n[{pub}]({url})\n\n{use}\n\n**حد کاربرد:** {limit}\n')
(ROOT/'FOUNDATIONS.md').write_text('\n'.join(seedmd),encoding='utf-8')
(ROOT/'foundations.json').write_text(json.dumps(seedrows,ensure_ascii=False,indent=2),encoding='utf-8')

def esc(s):return str(s).replace('|',' / ').replace('[','(').replace(']',')').replace('\n',' ')
table=[]; manifest=[]; bib=[]
for slug,fa,*_ in TOPICS:
 linked=[r for r in records if slug in r['topics']]
 primary=[r for r in records if r['topics'][0]==slug]
 # Each record is stored exactly once; topic pages may cross-reference it.
 compact=[{k:r[k] for k in ['id','doi','title','authors','year','journal','publisher','url','topics','citation_count_crossref','license_urls_deposited','retrieved_at']} for r in primary]
 (ROOT/'data'/f'{slug}.json').write_text(json.dumps(compact,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
 lines=[f'# {fa}\n',f'{len(linked)} ارجاع موضوعی؛ یک مقاله ممکن است در چند شاخه دیده شود. شمار کل کتابخانه بر مبنای DOI و عنوان یکتا است.\n','وضعیت: فرادادهٔ ثبت‌شده از سوی ناشر؛ پالایش خودکار عنوان؛ متن کامل خوانده نشده. DOI، داوری و صحت نتیجه را تضمین نمی‌کند.\n','| شناسه | عنوان و لینک اصلی | سال | مجله | استناد Crossref در زمان برداشت |','|---|---|---|---|---|']
 for r in sorted(linked,key=lambda r:-r['citation_count_crossref']):lines.append(f"| {r['id']} | [{esc(r['title'])}]({r['url']}) | {r['year'] or 'نامشخص'} | {esc(r['journal'])} | {r['citation_count_crossref']} |")
 (ROOT/'topics'/f'{slug}.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 table.append(f'| [{fa}](topics/{slug}.md) | {len(linked)} | [JSON](data/{slug}.json) · {len(primary)} رکورد اصلی |')
 manifest.append({'topic':slug,'label_fa':fa,'topic_references':len(linked),'primary_records':len(primary),'path':f'data/{slug}.json'})
(ROOT/'manifest.json').write_text(json.dumps({'unique_articles':len(records),'foundations':len(seeds),'retrieved_at':d['generated_at'],'parts':manifest},ensure_ascii=False,indent=2),encoding='utf-8')
readme=f'''# کتابخانهٔ توسعهٔ پایدار و معماری پایدار مارازاوا

نسخهٔ ۲۷ اکتبر ۲۰۲۶ · **{len(records):,} مقالهٔ DOIدار یکتا در ۳۶ شاخه + ۱۲ مرجع رسمی پایه**.

این پوشه، یک کتابخانهٔ کتاب‌شناختی برای کشف و انتخاب مطالعه است. ثبت در Crossref یا تعداد استناد، تضمین داوری، اعتبار یا کیفیت مقاله نیست. عنوان‌ها با قواعد قابل بازتولید پالایش شده‌اند؛ ادعای خواندن یا ارزیابی متن کامل {len(records):,} مقاله نداریم. «بزرگ‌ترین» یا «بهترین کتابخانهٔ جهان» نیز ادعا نمی‌شود.

## از کجا شروع کنیم؟

1. [۱۲ منبع پایه](FOUNDATIONS.md) برای چارچوب کلی و مسیر مطالعه.
2. در جدول پایین، مسئلهٔ پروژه را انتخاب کن؛ به‌جای خواندن تصادفی هزاران عنوان.
3. [روش استفاده و تبدیل منبع به دانش قابل اتکا](METHOD.md): خواندن متن، ثبت شواهد، بررسی محدودیت و تناسب با ایران.
4. [فهرست ماشینی](manifest.json) و فایل‌های JSON هر شاخه برای جست‌وجو و توسعهٔ ابزارهای پژوهشی.

## شاخه‌ها

ستون دوم شامل ارجاع متقاطع است؛ جمع آن شمار منابع یکتا نیست. هر مقاله در فایل‌های داده دقیقاً یک‌بار ذخیره می‌شود؛ جمع رکوردهای اصلی **{len(records):,}** است.

| موضوع | ارجاع موضوعی | دادهٔ قابل دریافت |
|---|---|---|
'''+ '\n'.join(table)+'''

## چه چیزی واقعاً ذخیره شده؟

عنوان اصلی، نویسندگان علمی، سال، مجله، ناشر، DOI، موضوع‌ها، زمان برداشت، شمار استناد ثبت‌شده و URL مجوزی که ناشر در فراداده گذاشته است. متن کامل، چکیده، تصاویر، کتاب‌های دارای حق نشر و محتوای کاربران مارازاوا در این پوشه نیست.

وجود URL مجوز، تأیید مستقل اجازهٔ بازنشر یا ورود متن به سرویس تجاری نیست. برای هر استفاده، نسخه و شرایط اصلی باید بررسی شود. این کتابخانه به‌تنهایی موتور روستایی را به منابع متصل نمی‌کند و به معنی آموزش مدل با این مقاله‌ها نیست.

## روش گردآوری و ممیزی

- منبع فراداده: [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)، با دادهٔ ثبت‌شدهٔ ناشران.
- ۳۶ جست‌وجوی موضوعی؛ تا ۲۵۰ نتیجه برای هر جست‌وجو؛ فقط نوع journal-article و تاریخ انتشار تا ۲۷ اکتبر ۲۰۲۶.
- پالایش عبارت عنوان و زمینهٔ موضوعی؛ حذف برخی نتایج نامرتبط و اصلاحیه/پس‌گرفتن‌های علامت‌خورده در فرادادهٔ برگشتی.
- ترکیبی از رتبهٔ مرتبط، پرارجاع و تازه؛ این انتخاب مرور نظام‌مند یا پوشش جامع همهٔ زبان‌ها و پایگاه‌ها نیست.
- حذف DOI تکراری و عنوان‌های یکسان پس از نرمال‌سازی؛ ممکن است دو اثر متفاوت عنوان یکسان داشته باشند، بنابراین این قاعده در استفادهٔ پژوهشی باید بازبینی شود.
- [گزارش ممیزی و نشانی دقیق جست‌وجوها](audit.json) · [کد گردآوری](collect.py) · [ساخت فهرست‌ها](build_library.py).
- تمام DOIها در پاسخ API مشاهده شده‌اند؛ بازشدن تک‌تک صفحات ناشران، اصلاحیه‌ها یا دسترسی متن کامل جداگانه آزموده نشده است.

## توسعهٔ بعدی

اولویت بعدی، افزایش تعداد صرف نیست: مرور متن منابع کلیدی، پژوهش فارسی و ایران، ارزیابی میدانی، و تبدیل یافته‌های تأییدشده به برگه‌های شواهد با ارجاع دقیق. مقررات، ایمنی، سازه، اقلیم، هزینه و وضعیت مالکیت هر پروژه نیازمند بررسی متخصص و دادهٔ همان محل‌اند.

[بازگشت به کتابخانهٔ کسب‌وکار](../BUSINESS-RESOURCE-LIBRARY-2026-10-25.md) · [مرجع مالی و امکان‌سنجی](../FINANCE-FEASIBILITY-KNOWLEDGE-2026-10-25.md)
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
(ROOT/'METHOD.md').write_text('''# از فهرست مقاله تا پشتوانهٔ قابل اتکا

## مسیر استفاده در مارازاوا

1. **سؤال روشن:** چه تصمیمی باید گرفته شود؟ تجهیز، احیا یا ساخت؟ آسایش، درآمد، آب یا دسترسی؟
2. **انتخاب مطالعه:** از منبع پایه، مرورهای مرتبط و پژوهش محلی شروع کن؛ شمار استناد، حکم کیفیت نیست.
3. **خواندن متن اصلی:** عنوان به‌تنهایی پشتوانهٔ توصیه نیست. نوع مطالعه، مکان، نمونه، روش و محدودیت ثبت شود.
4. **برگهٔ شواهد:** ادعا، DOI، شماره صفحه/جدول، واحد، اقلیم، تاریخ و عدم‌قطعیت ثبت شود.
5. **بررسی تناسب:** انتقال نتیجه از کشور یا اقلیم دیگر به ایران نیاز به توجیه دارد. مصالح بومی هم بدون ارزیابی، الزاماً ایمن یا پایدار نیستند.
6. **کنترل حقوق:** مجوز متن، شکل و داده جداگانه بررسی شود؛ در صورت ابهام، فقط ارجاع بده.
7. **تأیید تخصصی:** منابع نامزد به‌صورت خودکار دستور اجرایی، عدد مالی یا پیشنهاد ایمنی تولید نکنند.
8. **پایلوت و پایش:** مصرف آب/انرژی، استفادهٔ مردم، هزینه و رضایت واقعی ثبت و با خط مبنا مقایسه شود.

## وضعیت‌های پیشنهادی شواهد

- `discovered`: فقط فراداده موجود است؛ وضعیت فعلی مقاله‌های این کتابخانه.
- `screened`: چکیده و تناسب سؤال بررسی شده‌اند.
- `full_text_reviewed`: متن اصلی و روش خوانده شده‌اند.
- `context_checked`: تناسب با اقلیم، جامعه و مقررات پروژه ارزیابی شده است.
- `approved_for_specific_use`: یک کاربرد مشخص با محدودیت و مسئول تأیید دارد.

این وضعیت‌ها مسیر پیشنهادی‌اند؛ در وب‌اپ به‌صورت خودکار فعال نشده‌اند.

## اولویت «باوان» و نمونه‌های روستایی

صدای مردم و گروه‌های جاافتاده → امکان استفاده از فضای موجود → مالکیت و خطر → برنامهٔ خدمت و بهره‌بردار → ارزیابی آسایش و دسترسی → هزینهٔ تجهیز و نگهداری → اجرای آزمایشی → تصمیم برای احیا یا ساخت.

هیچ عدد استاندارد، ظرفیت، بودجه، بازده یا جزئیات سازه صرفاً از عنوان مقاله استنتاج نشود. اطلاعات شخصی و ایده‌های محرمانهٔ کاربران به این مخزن عمومی اضافه نشوند.
''',encoding='utf-8')
# Deterministic integrity checks before publication.
allparts=[]
for part in manifest:allparts.extend(json.loads((ROOT/part['path']).read_text(encoding='utf-8')))
assert len(allparts)==len(records)>=1000
assert len({r['doi'] for r in allparts})==len(records)
assert all(r['url']=='https://doi.org/'+r['doi'] and r['title'] for r in allparts)
assert all(not r['full_text_reviewed'] and not r['full_text_archived'] for r in records)
files=['README.md','METHOD.md','FOUNDATIONS.md','foundations.json','manifest.json','audit.json','collect.py','build_library.py']+[str(p.relative_to(ROOT)).replace('\\','/') for folder in ['topics','data'] for p in sorted((ROOT/folder).glob('*'))]
(ROOT/'publication-files.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
print(json.dumps({'unique_articles':len(records),'foundation_sources':len(seeds),'public_files':len(files),'integrity_checks':'passed'},ensure_ascii=False))
