from fastapi import APIRouter, File, UploadFile, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse

from api.translate_text import detect_and_transl_text, create_pdf
from api.s3_client import download_from_s3, upload_to_s3, delete_from_s3
from fastapi.staticfiles import StaticFiles


router_translate_PDF = APIRouter(prefix='/translate_PDF',
                                 tags=["Перевод файлов PDF"])
router_translate_PDF.mount("/static", StaticFiles(directory="static/css"), name="static")


@router_translate_PDF.get("/main", response_class=HTMLResponse)
async def read_root():
    with open("templages/main.html", encoding="utf-8") as f:
        return f.read()


@router_translate_PDF.post("/upload", tags=['Загрузка файла'])
async def translate_pdf_file(file: UploadFile = File(...)):
    try:
        await upload_to_s3(file, file.filename)
        translate_text = await detect_and_transl_text(file.filename)
        translate_pdf_filename = await create_pdf(translate_text, file.filename)
        await delete_from_s3(file.filename)
        return {'filename': translate_pdf_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_translate_PDF.get("/download/{filename}")
async def download_translate_pdf(filename: str):
    try:
        local_path = await download_from_s3(filename)
        return FileResponse(local_path, media_type="application/pdf",
                            headers={"Content-Disposition": f"attachment; filename={filename}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
