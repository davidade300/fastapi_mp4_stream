"""
Returns:
    _type_: _description_

Yields:
    _type_: _description_
"""

import os

from fastapi import FastAPI, Request, status
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(debug=True, title="Video Streaming")
templates = Jinja2Templates(directory="templates")

VIDEO_FILE = "video.mp4"
# CHUNK_SIZE = 1024 * 1024
CHUNK_SIZE = 256**2


def generate_video_chunks():
    with open(VIDEO_FILE, "rb") as file_object:
        counter = 0
        while True:
            chunk = file_object.read(CHUNK_SIZE)
            if not chunk:  # quando chunk for uma string vazia (fim do arquivo)
                print("end of chunks")
                break
            counter = counter + 1
            print("Chunk counter", counter)
            yield chunk


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "title": "FastAPI Video Streaming",
        },
    )


@app.route("/example", methods=["GET", "POST"])
async def stream_video(request: Request):
    file_size = os.stat(VIDEO_FILE).st_size
    headers = {
        "content-type": "video/mp4",
        "accept-ranges": "bytes",
        "content-encoding": "identity",
        "content-lenght": str(file_size),
        "content-range": f"bytes 0-{file_size-1}/{file_size}",
    }
    return StreamingResponse(
        content=generate_video_chunks(),
        headers=headers,
        status_code=status.HTTP_206_PARTIAL_CONTENT,
    )


@app.get("/asd")
async def rota(request: Request):
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "title": "FastAPI Video Streaming",
        },
    )


# @app.route()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)
