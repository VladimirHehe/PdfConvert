import pymupdf
import io
import translators as ts
import fitz
from api.s3_client import upload_to_s3
from api.s3_client import s3_client, AWS_BUCKET_NAME
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def split_text(text, max_length=1000):
    """Разделяет текст на части, не превышающие max_length."""
    words = text.split()
    current_part = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            yield ' '.join(current_part)
            current_part = [word]
            current_length = len(word)
        else:
            current_part.append(word)
            current_length += len(word) + 1

    if current_part:
        yield ' '.join(current_part)


async def detect_and_transl_text_pdf(file_name, target_language: str) -> str:
    """Определение текса, взятие из файла и перевод"""
    file_obj = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=file_name)
    file_content = file_obj['Body'].read()
    with pymupdf.open(stream=file_content) as doc:
        detected_text = chr(12).join([page.get_text() for page in doc])
    translated_parts = []
    for part in split_text(detected_text):
        trans_text = ts.translate_text(query_text=part,
                                       translator='bing',
                                       from_language='auto',
                                       to_language=target_language)
        translated_parts.append(trans_text)

    final_translated_text = '\n'.join(translated_parts)
    return final_translated_text


async def create_pdf(query_text, file_name):
    """Создание файла pdf и выгрузка в s3"""
    translated_pdf_filename = f"trans_{str(file_name)[:-4]}.pdf"
    pdf_buffer = io.BytesIO()

    # Создаем PDF-канвас
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    x = 72
    y = height - 72
    line_height = 14

    words = query_text.split()
    current_line = ""

    for word in words:

        if c.stringWidth(current_line + " " + word) > (width - 2 * x):

            c.drawString(x, y, current_line)
            y -= line_height

            if y < 72:
                c.showPage()
                y = height - 72  # Сбрасываем y-координату для новой страницы

            current_line = word  # Начинаем новую строку с текущего слова
        else:
            # Если помещается, добавляем слово к текущей строке
            current_line += " " + word if current_line else word

    if current_line:
        c.drawString(x, y, current_line)

    c.save()

    pdf_buffer.seek(0)
    await upload_to_s3(pdf_buffer, translated_pdf_filename)
    return translated_pdf_filename
