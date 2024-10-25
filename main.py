from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
from starlette.templating import Jinja2Templates
from router.translate_pdf import router_translate_PDF
from router.translate_Word import router_translate_Word

app = FastAPI()

templates = Jinja2Templates(directory="templages")


@app.get("/", response_class=HTMLResponse, tags=['Главная страница'])
async def read_root_main(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

app.include_router(router_translate_Word)
app.include_router(router_translate_PDF)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
