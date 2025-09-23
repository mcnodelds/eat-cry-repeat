from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
async def root() -> HTMLResponse:
    return HTMLResponse(content="Hello, World!")
