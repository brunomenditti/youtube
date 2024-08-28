from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Um exemplo simples de modelo de dados
class VideoRequest(BaseModel):
    url: str

# Rota que processa o pedido de download
@app.post("/download/")
def download_video(request: VideoRequest):
    # Lógica para processar o download do vídeo
    # Por exemplo, você pode integrar o yt-dlp aqui
    return {"message": "Vídeo processado", "url": request.url}

# Para rodar o servidor, use:
# uvicorn backend:app --reload
