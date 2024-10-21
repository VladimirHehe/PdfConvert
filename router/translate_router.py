import os
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from api.translate_text import detect_and_transl_text, create_pdf
from api.s3_client import download_from_s3, upload_to_s3, delete_from_s3


router_translate_file = APIRouter(prefix='/translate',
                                  tags=["Перевод файлов PDF"])


@router_translate_file.get("/main", response_class=HTMLResponse)
async def read_root():
    with open("templages/main.html", encoding="utf-8") as f:
        return f.read()


# @router_translate_file.post("/main/upload", tags=['Загрузка файла'])
# async def translate_pdf_file(file: UploadFile = File()):
#     file_location = f"temp_{file.filename}"
#     with open(file_location, "rb+") as f:
#         f.write(f.read())
#
#     translated_text = await detect_and_transl_text(file_location)
#     translate_pdf_filename = await create_pdf(translated_text, file.filename)
#     os.remove(file_location)
#     return FileResponse(translate_pdf_filename, media_type='application/pdf', filename=translate_pdf_filename)


@router_translate_file.post("/main/upload", tags=['Загрузка файла'])
async def translate_pdf_file(file: UploadFile = File(...)):
    upload_to_s3(file)
    translate_text = await detect_and_transl_text(file.filename)
    translate_pdf_filename = await create_pdf(translate_text, file)
    delete_from_s3(file.filename)
    download_from_s3(translate_pdf_filename)
    return {'translate_pdf': translate_pdf_filename}






# @router_translate_file.post("/ds/")
# def donload(file: UploadFile = File(...)):
#     upload_to_s3(file)
#     return {"message": f"File '{file.filename}' uploaded to S3 bucket "}


# @router_translate_file.get("/dsret456")
# def donloadgfhfgh(filename: str):
#     download_from_s3(filename)
#     return "ok"
