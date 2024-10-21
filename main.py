from fastapi import FastAPI
import uvicorn
from router.translate_router import router_translate_PDF


app = FastAPI()
app.include_router(router_translate_PDF)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
