import os
import uuid
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/api/projects", tags=["Projects"])

# مجلد تخزين الصور المرفوعة
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# قاعدة بيانات وهمية مؤقتة في الذاكرة لتخزين المشاريع 
# (تقدر تربطها بقاعدة بياناتك لاحقاً بنفس أسلوب التعاقدات)
PROJECTS_DB = []
project_id_counter = 1


@router.get("")
async def get_projects():
    """جلب كافة المشاريع المضافة"""
    return PROJECTS_DB


@router.post("")
async def create_project(
    title: str = Form(...),
    link: str = Form(...),
    description: str = Form(None),
    images: List[UploadFile] = File(...)
):
    """إضافة مشروع جديد مع رفع صور متعددة"""
    global project_id_counter
    saved_images_urls = []

    for image in images:
        # التحقق من أن الملف المرفوع هو صورة بالفعل
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=f"الملف {image.filename} ليس صورة صالحة.")
        
        # توليد اسم فريد للصورة لمنع تداخل الأسماء
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # حفظ الصورة في المجلد المحلي
        try:
            with open(file_path, "wb") as f:
                content = await image.read()
                f.write(content)
            # رابط الصورة الذي سيعود للفرونت إند (يعتمد على بورت السيرفر 8000)
            saved_images_urls.append(f"http://127.0.0.1:8000/static/uploads/{unique_filename}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"فشل حفظ الصورة {image.filename}: {str(e)}")

    # إنشاء كائن المشروع الجديد وتخزينه
    new_project = {
        "id": project_id_counter,
        "title": title,
        "link": link,
        "description": description,
        "images": saved_images_urls
    }
    PROJECTS_DB.append(new_project)
    project_id_counter += 1

    return {"status": "success", "message": "Project added successfully", "project": new_project}


@router.delete("/{project_id}")
async def delete_project(project_id: int):
    """حذف مشروع معين عن طريق الـ ID"""
    global PROJECTS_DB
    project_to_delete = next((p for p in PROJECTS_DB if p["id"] == project_id), None)
    
    if not project_to_delete:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    
    # (اختياري) يمكنك هنا إضافة كود لحذف ملفات الصور الفعلية من الهارد ديسك إذا أردت
    
    PROJECTS_DB = [p for p in PROJECTS_DB if p["id"] != project_id]
    return {"status": "success", "message": "Project deleted successfully"}
