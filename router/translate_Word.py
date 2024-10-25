from fastapi import APIRouter, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from api.translate_text_word import create_word, detect_and_transl_text_word
from api.s3_client import download_from_s3, upload_to_s3, delete_from_s3

router_translate_Word = APIRouter(prefix='/translate_word',
                                  tags=["Перевод файлов Word"])

router_translate_Word.mount("/translate_word/static", StaticFiles(directory="static/css"), name="static")
templates = Jinja2Templates(directory="templages")


@router_translate_Word.get("/", response_class=HTMLResponse, tags=["Html-страница перевода"])
async def read_root_main(request: Request):
    return templates.TemplateResponse("translate_word.html", {"request": request})


@router_translate_Word.post("/upload", tags=['Загрузка файла'])
async def translate_word_file(file: UploadFile = File(...)):
    try:
        await upload_to_s3(file, file.filename)
        translate_text = await detect_and_transl_text_word(file.filename)
        translate_word_filename = await create_word(translate_text, file.filename)
        await delete_from_s3(file.filename)
        return {'filename': translate_word_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_translate_Word.get("/download/{filename}", tags=['Скачивание файла'])
async def download_translate_word(filename: str):
    try:
        local_path = await download_from_s3(filename)
        return FileResponse(local_path, media_type="application/pdf",
                            headers={"Content-Disposition": f"attachment; filename={filename}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
