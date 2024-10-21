from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse
from api.translate_text import detect_and_transl_text, create_pdf
from api.s3_client import download_from_s3, upload_to_s3, delete_from_s3


router_translate_file = APIRouter(prefix='/translate',
                                  tags=["Перевод файлов PDF"])


@router_translate_file.get("/main", response_class=HTMLResponse)
async def read_root():
    with open("templages/main.html", encoding="utf-8") as f:
        return f.read()


@router_translate_file.post("/main/upload", tags=['Загрузка файла'])
async def translate_pdf_file(file: UploadFile = File(...)):
    await upload_to_s3(file, file.filename)
    translate_text = await detect_and_transl_text(file.filename)
    translate_pdf_filename = await create_pdf(translate_text, file)
    await delete_from_s3(file.filename)
    await download_from_s3(translate_pdf_filename)
    await delete_from_s3(translate_pdf_filename)
    return {'translate_pdf': translate_pdf_filename}
