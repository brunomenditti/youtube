import streamlit as st
import requests
import yt_dlp
import os
import uuid

# Função para baixar o vídeo do YouTube para uma pasta temporária
def download_video(url):
    temp_dir = "./temp_videos"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    video_id = str(uuid.uuid4())
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(temp_dir, f'{video_id}.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Encontra o arquivo baixado
    downloaded_files = os.listdir(temp_dir)
    video_file = [f for f in downloaded_files if video_id in f][0]
    video_path = os.path.join(temp_dir, video_file)

    return video_path, video_file

# Interface da aplicação Streamlit
st.title("Interface Streamlit com Backend")

video_url = st.text_input("Insira o link do vídeo do YouTube:")

if video_url:
    if st.button("Baixar Vídeo"):
        try:
            # Enviando o pedido ao backend
            response = requests.post("http://localhost:8000/download/", json={"url": video_url})
            
            if response.status_code == 200:
                st.success("O backend processou o pedido com sucesso!")
                st.write(response.json())  # Mostra a resposta do backend
                
                # Baixa o vídeo no servidor
                video_path, video_file = download_video(video_url)
                
                # Oferece um link para o usuário baixar o vídeo
                with open(video_path, "rb") as file:
                    btn = st.download_button(
                        label="Clique aqui para baixar o vídeo",
                        data=file,
                        file_name=video_file,
                        mime="video/mp4"
                    )
                
                # Cleanup temporário (opcional)
                # os.remove(video_path)
            else:
                st.error("Houve um problema no processamento do pedido.")
        
        except Exception as e:
            st.error(f"Erro ao se comunicar com o backend: {str(e)}")
