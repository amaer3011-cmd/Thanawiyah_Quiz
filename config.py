# -*- coding: utf-8 -*-
"""
إعدادات البوت — كل القيم تُقرأ من متغيرات البيئة (.env)
"""
import os
from dotenv import load_dotenv

load_dotenv()

# توكن بوت تليجرام (من BotFather)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# مفاتيح Gemini API — يدعم أكتر من مفتاح مفصولة بفاصلة
# مثال في .env:  GEMINI_API_KEYS=key1,key2,key3
_raw_keys = os.getenv("GEMINI_API_KEYS", "")
GEMINI_API_KEYS = [k.strip() for k in _raw_keys.split(",") if k.strip()]

# اسم موديل Gemini المستخدم لتوليد الأسئلة (نص) ولقراءة الصور
GEMINI_TEXT_MODEL = os.getenv("GEMINI_TEXT_MODEL", "gemini-2.0-flash")
GEMINI_VISION_MODEL = os.getenv("GEMINI_VISION_MODEL", "gemini-2.0-flash")

# الحد الأقصى لحجم الملفات المرفوعة (بايت) — تليجرام نفسه بيحدد بحد أقصى ~20MB للبوتات العادية
MAX_FILE_SIZE = 20 * 1024 * 1024

# مجلد مؤقت لتحميل ومعالجة الملفات
TEMP_DIR = os.getenv("TEMP_DIR", "/tmp/quizbot")

# الحد الأدنى والأقصى لعدد أسئلة الكويز
MIN_QUESTIONS = 3
MAX_QUESTIONS = 40
DEFAULT_QUESTIONS = 15

# قالب الكويز HTML
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "quiz_template.html")

# ---------------------------------------------------------------------------
# الصور التوضيحية (SVG) لبعض أسئلة الكويز
# ---------------------------------------------------------------------------
# لو True، يحاول البوت توليد رسم SVG بسيط للأسئلة اللي النموذج يقرر إنها
# تستفيد من رسم توضيحي (needs_image=True). أي فشل في توليد صورة معينة
# بيتجاهل بهدوء ومايوقفش باقي الكويز.
ENABLE_QUESTION_IMAGES = os.getenv("ENABLE_QUESTION_IMAGES", "true").strip().lower() not in ("0", "false", "no")
# حد أقصى لعدد الصور المولّدة لكل كويز (تحكم في الوقت والتكلفة)
MAX_IMAGES_PER_QUIZ = int(os.getenv("MAX_IMAGES_PER_QUIZ", "6"))

# ---------------------------------------------------------------------------
# تقسيم توليد الأسئلة لدفعات (batching)
# ---------------------------------------------------------------------------
# لو عدد الأسئلة المطلوب أكبر من هذا الحد، يتم تقسيم التوليد لدفعات أصغر
# بدل استدعاء واحد ضخم لـ Gemini، لتقليل احتمال تقطّع الـ JSON وزيادة تنوع الأسئلة.
BATCH_THRESHOLD = int(os.getenv("BATCH_THRESHOLD", "12"))
QUESTIONS_PER_BATCH = int(os.getenv("QUESTIONS_PER_BATCH", "10"))

# ---------------------------------------------------------------------------
# مدة الامتحان المؤقت
# ---------------------------------------------------------------------------
DEFAULT_DURATION_MINUTES = int(os.getenv("DEFAULT_DURATION_MINUTES", "10"))
MIN_DURATION_MINUTES = 3
MAX_DURATION_MINUTES = 180
