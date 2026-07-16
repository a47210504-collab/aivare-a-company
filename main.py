import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# إضافة المسار الحالي للمشروع لضمان رؤية المجلدات الفرعية
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
# هذا يجعل مجلد static/uploads متاحاً عبر الرابط: http://127.0.0.1:8000/static/uploads/
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# 1. استيراد راوتر التعاقدات (Contact Router)
try:
    from app.routers import contact
    app.include_router(contact.router)
    print("🚀 SUCCESS: Contact router loaded successfully.")
except ImportError as e:
    print(f"❌ CRITICAL ERROR: Could not import contact router. Check path or dependencies: {e}")
except Exception as e:
    print(f"💥 RUNTIME ERROR: An error occurred inside contact.py: {e}")


# 2. استيراد راوتر المشاريع الجديد (Projects Router)
try:
    from app.routers import projects
    app.include_router(projects.router)
    print("🚀 SUCCESS: Projects router loaded successfully.")
except ImportError as e:
    print(f"❌ CRITICAL ERROR: Could not import projects router. Check path or dependencies: {e}")
except Exception as e:
    print(f"💥 RUNTIME ERROR: An error occurred inside projects.py: {e}")


@app.get("/")
def home():
    return {"status": "success", "message": "Aivare API is running perfectly!"}


if __name__ == "__main__":
    # تشغيل السيرفر بالاسم الثابت "main:app" لضمان استقرار خاصية الـ reload وتفادي توقف uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)