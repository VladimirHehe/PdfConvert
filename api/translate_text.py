import pymupdf
import io
import translators as ts
import fitz
from api.s3_client import upload_to_s3
from api.s3_client import s3_client, AWS_BUCKET_NAME


async def detect_and_transl_text(file_name):
    file_obj = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=file_name)
    file_content = file_obj['Body'].read()
    with pymupdf.open(stream=file_content) as doc:
        detected_text = chr(12).join([page.get_text() for page in doc])
    trans_text = ts.translate_text(query_text=detected_text,
                                   translator='bing',
                                   from_language='auto',
                                   to_language='en',
                                   )
    return trans_text


async def create_pdf(query_text, file_name):
    translated_pdf_filename = f"trans_{str(file_name)[:-4]}.pdf"
    pdf_buffer = io.BytesIO()
    with fitz.open() as pdf_writer:
        pdf_writer.new_page()
        pdf_writer[-1].insert_text((72, 72), query_text, fontsize=11)
        pdf_writer.save(pdf_buffer)
    pdf_buffer.seek(0)
    await upload_to_s3(pdf_buffer, translated_pdf_filename)
    return translated_pdf_filename
