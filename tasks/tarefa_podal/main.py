import pygame
import random
import time
import cv2
import threading
import os
import pandas as pd
from constants import N_TRIALS, INTERSTIMULUS, INTERSTIMULUS_6, SUJ, PROB_6, CAMERA  

data = []  # Lista para armazenar os dados da planilha

# Função para carregar os sons com verificação de existência
def carregar_sons(pasta_audios):
    sounds = {}
    for i in range(1, 10):
        caminho_arquivo = os.path.join(pasta_audios, f"{i}.wav")
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {caminho_arquivo}")
        sounds[str(i)] = pygame.mixer.Sound(caminho_arquivo)
    
    # Carregar os sons do apito
    for nome in ["apito", "apito_final"]:
        caminho_arquivo = os.path.join(pasta_audios, f"{nome}.mp3")
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {caminho_arquivo}")
        sounds[nome] = pygame.mixer.Sound(caminho_arquivo)
    
    return sounds

# Função para gravar vídeo garantindo sincronização
def gravar_video(cap, out, gravando, fps):
    tempo_entre_frames = 1 / fps  # Tempo esperado entre cada frame
    while gravando.is_set():
        start = time.time()
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        elapsed = time.time() - start
        time.sleep(max(0, tempo_entre_frames - elapsed))  # Ajusta para manter o FPS

# Inicializar pygame
pygame.mixer.init()
pygame.display.quit()

# Inicializar câmera
cap = cv2.VideoCapture(CAMERA)
ret, _ = cap.read()
if not ret:
    raise RuntimeError("Erro ao acessar a câmera.")

# Obter FPS real da câmera
fps_camera = cap.get(cv2.CAP_PROP_FPS)
if fps_camera == 0:
    fps_camera = 30  # Define um padrão caso não consiga obter

print(f"FPS da câmera detectado: {fps_camera}")

# Configurações de gravação de vídeo
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(f"{SUJ}_gravacao.avi", fourcc, fps_camera, (640, 480))

# Carregar sons
try:
    sounds = carregar_sons("audios")
except FileNotFoundError as e:
    print(e)
    cap.release()
    out.release()
    pygame.quit()
    exit()

# Criar sequência garantindo que o número 6 apareça 15% das vezes
num_trials = N_TRIALS  
prob_6 = PROB_6    
num_6 = int(num_trials * prob_6)
num_outros = num_trials - num_6
numeros = [1, 2, 3, 4, 5, 7, 8, 9]  
sequencia = [6] * num_6 + random.choices(numeros, k=num_outros)
random.shuffle(sequencia)  

# Contagem regressiva antes de iniciar a gravação usando áudios
for i in range(5, 0, -1):
    sounds[str(i)].play()
    time.sleep(sounds[str(i)].get_length())  # Espera o tempo do áudio real

# Tocar o som do apito antes de iniciar a gravação
sounds["apito"].play()
time.sleep(sounds["apito"].get_length())  

# Variável para controlar a gravação
gravando = threading.Event()
gravando.set()

# Iniciar a gravação em uma thread separada
thread_gravacao = threading.Thread(target=gravar_video, args=(cap, out, gravando, fps_camera))
thread_gravacao.start()

# Loop para tocar os sons e armazenar os tempos
start_time = time.time()

try:
    for num in sequencia:
        data.append([num, time.time() - start_time])
        sounds[str(num)].play()  # Toca o som correspondente
        if num == 6:
            time.sleep(INTERSTIMULUS_6 / 1000.0)  # Converte de ms para s
        else:   
            time.sleep(INTERSTIMULUS / 1000.0)  # Converte de ms para s
except Exception as e:
    print(f"Erro durante a reprodução dos sons: {e}")

# Finalizar gravação
gravando.clear()  
thread_gravacao.join()

# Tocar som final
sounds["apito_final"].play()
time.sleep(sounds["apito_final"].get_length())  

# Liberar recursos
cap.release()
out.release()
pygame.quit()

# Salvar resultados em Excel
df = pd.DataFrame(data, columns=["Número Apresentado", "Tempo"])
excel_file = f"{SUJ}_resultados.xlsx"
df.to_excel(excel_file, index=False, engine="openpyxl")

print("Recursos liberados. Programa finalizado.")
