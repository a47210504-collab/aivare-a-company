import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# إضافة المسار الحالي للمشروع لضمان رؤية الملفات والمجلدات
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="Aivare Core API")

# تفعيل الـ CORS لحل مشاكل الحظر من المتصفح
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في البيئة الإنتاجية يفضل تحديد الدومين بدلاً من "*" للأمان
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تفعيل مسار عرض الصور والملفات الثابتة (Static Files) 
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# 1. استيراد راوتر التعاقدات (Contact Router) مباشرة من الفولدر الرئيسي
try:
    import contact
    app.include_router(contact.router)
    print("🚀 SUCCESS: Contact router loaded successfully.")
except ImportError as e:
    # محاولة بديلة لو الملف موجود داخل فولدر فرعي
    try:
        from app.routers import contact
        app.include_router(contact.router)
        print("🚀 SUCCESS: Contact router loaded from app.routers.")
    except ImportError:
        print(f"❌ CRITICAL ERROR: Could not import contact router. Check path or dependencies: {e}")
except Exception as e:
    print(f"💥 RUNTIME ERROR: An error occurred inside contact.py: {e}")


# 2. استيراد راوتر المشاريع (Projects Router) مباشرة من الفولدر الرئيسي
try:
    import projects
    app.include_router(projects.router)
    print("🚀 SUCCESS: Projects router loaded successfully.")
except ImportError as e:
    try:
        from app.routers import projects
        app.include_router(projects.router)
        print("🚀 SUCCESS: Projects router loaded from app.routers.")
    except ImportError:
        print(f"❌ CRITICAL ERROR: Could not import projects router. Check path or dependencies: {e}")
except Exception as e:
    print(f"💥 RUNTIME ERROR: An error occurred inside projects.py: {e}")


@app.get("/")
def home():
    return {"status": "success", "message": "Aivare API is running perfectly!"}


if __name__ == "__main__":
    # قراءة البورت ديناميكياً من السيرفر لضمان عمل السيرفر على Railway
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
