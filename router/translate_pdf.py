from fastapi import APIRouter, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse, StreamingResponse
from starlette.templating import Jinja2Templates

from api.translate_text_pdf import detect_and_transl_text_pdf, create_pdf
from api.s3_client import download_from_s3, upload_to_s3, delete_from_s3
from fastapi.staticfiles import StaticFiles

router_translate_PDF = APIRouter(prefix='/translate_PDF',
                                 tags=["Перевод файлов PDF"])

router_translate_PDF.mount("/translate_PDF/static", StaticFiles(directory="static/css"), name="static")
templates = Jinja2Templates(directory="templages")


@router_translate_PDF.get("/", response_class=HTMLResponse, tags=["Html-страница перевода"])
async def read_root_main(request: Request):
    return templates.TemplateResponse("translate_pdf.html", {"request": request})


@router_translate_PDF.post("/upload", tags=['Загрузка файла'])
async def translate_pdf_file(file: UploadFile = File(...)):
    try:
        await upload_to_s3(file, file.filename)
        translate_text = await detect_and_transl_text_pdf(file.filename)
        translate_pdf_filename = await create_pdf(translate_text, file.filename)
        await delete_from_s3(file.filename)
        return {'filename': translate_pdf_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_translate_PDF.get("/download/{filename}", tags=['Скачивание файла'])
async def download_translate_pdf(filename: str):
    try:
        file_stream = await download_from_s3(filename)
        if file_stream is None:
            raise HTTPException(status_code=404, detail="File not found")

        return StreamingResponse(
            file_stream,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
