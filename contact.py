import sqlite3
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

# 1. الـ Schema تشمل حقل رقم الهاتف المتوافق مع الفرونت إند
class ContactSchema(BaseModel):
    name: str
    phone_number: str
    email: str
    message: str

# دالة لتهيئة قاعدة البيانات وإنشاء الجدول بالاسم الصحيح والأعمدة كاملة دفعة واحدة
def init_db():
    conn = sqlite3.connect("aivare.db")
    cursor = conn.cursor()
    
    # إنشاء الجدول بكافة الأعمدة المطلوبة مباشرة لضمان عدم حدوث أي خطأ في السيرفر
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone_number TEXT,
            email TEXT,
            message TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

# تشغيل التهيئة تلقائياً عند إقلاع السيرفر لإنشاء الجدول فوراً
init_db()


# 1️⃣ دالة استقبال طلبات التعاقد وحفظها (POST)
@router.post("/api/contact", status_code=status.HTTP_201_CREATED)
def add_contact(item: ContactSchema):
    conn = sqlite3.connect("aivare.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO contact_messages (name, phone_number, email, message) VALUES (?, ?, ?, ?)",
            (item.name, item.phone_number, item.email, item.message)
        )
        conn.commit()
        return {"status": "success", "message": "تم استلام طلب التعاقد وحفظه بنجاح!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"خطأ في حفظ البيانات: {str(e)}")
    finally:
        conn.close()


# 2️⃣ دالة جلب البيانات للوحة التحكم (GET)
@router.get("/api/contact")
def get_contacts():
    conn = sqlite3.connect("aivare.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, phone_number, email, message FROM contact_messages ORDER BY id DESC")
        rows = cursor.fetchall()
        result = [
            {
                "id": row[0],
                "name": row[1],
                "phone_number": row[2],
                "email": row[3],
                "message": row[4]
            } 
            for row in rows
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في قراءة البيانات: {str(e)}")
    finally:
        conn.close()


# 3️⃣ دالة الحذف المعتمدة على الـ ID لضمان الأمان (DELETE)
@router.delete("/api/contact/{contact_id}")
def delete_message(contact_id: int):
    conn = sqlite3.connect("aivare.db")
    cursor = conn.cursor()
    rowcount = 0
    try:
        cursor.execute("DELETE FROM contact_messages WHERE id = ?", (contact_id,))
        conn.commit()
        rowcount = cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء الحذف: {str(e)}")
    finally:
        conn.close()

    if rowcount == 0:
        raise HTTPException(status_code=404, detail="الرسالة غير موجودة")
        
    return {"status": "success", "message": "تم حذف الرسالة بنجاح"}