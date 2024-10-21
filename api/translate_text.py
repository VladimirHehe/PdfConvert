import pymupdf
import asyncio
import translators as ts
import fitz
from fastapi.responses import FileResponse
from api.s3_client import upload_to_s3


async def detect_and_transl_text(file):
    with pymupdf.open(file) as doc:
        detected_text = chr(12).join([page.get_text() for page in doc])
    trans_text = ts.translate_text(query_text=detected_text,
                                   translator='bing',
                                   from_language='auto',
                                   to_language='en',
                                   )
    return trans_text


async def create_pdf(query_text, file):
    translated_pdf_filename = f"trans_{str(file.filename)[:-4]}.pdf"
    with fitz.open() as pdf_writer:
        pdf_writer.new_page()
        pdf_writer[-1].insert_text((72, 72), query_text, fontsize=11)
        pdf_writer.save(translated_pdf_filename)
        upload_to_s3(translated_pdf_filename)#    s3_client.upload_fileobj(file.file, AWS_BUCKET_NAME, file.filename)AttributeError: 'str' object has no attribute 'file'
    return translated_pdf_filename
