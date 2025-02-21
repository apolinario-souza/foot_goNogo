import pygame
import random
import time
import cv2
import threading
import os
import pandas as pd



data = []  # Lista para armazenar os dados da planilha


# Função para carregar os sons com verificação de existência
def carregar_sons(pasta_audios):
    sounds = {}
    for i in range(1, 10):
        caminho_arquivo = os.path.join(pasta_audios, f"{i}.wav")
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {caminho_arquivo}")
        sounds[str(i)] = pygame.mixer.Sound(caminho_arquivo)
    
    # Carregar o som do apito
    apito_arquivo = os.path.join(pasta_audios, "apito.mp3")
    if not os.path.exists(apito_arquivo):
        raise FileNotFoundError(f"Arquivo de áudio não encontrado: {apito_arquivo}")
    sounds["apito"] = pygame.mixer.Sound(apito_arquivo)
    
    # Carregar o som do apito
    apito_arquivo = os.path.join(pasta_audios, "apito_final.mp3")
    if not os.path.exists(apito_arquivo):
        raise FileNotFoundError(f"Arquivo de áudio não encontrado: {apito_arquivo}")
    sounds["apito_final"] = pygame.mixer.Sound(apito_arquivo)
    
    return sounds

# Função para gravar vídeo
def gravar_video(cap, out, gravando):
    while gravando.is_set():
        ret, frame = cap.read()
        if ret:
            out.write(frame)

# Inicializar pygame
pygame.mixer.init()
pygame.init()

# Inicializar câmera
cap = cv2.VideoCapture(0)  # Abre a câmera padrão
ret, _ = cap.read()
if not ret:
    raise RuntimeError("Erro ao acessar a câmera.")

# Configurações de gravação de vídeo
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec para gravação
out = cv2.VideoWriter('gravacao.avi', fourcc, 20.0, (640, 480))  # Arquivo de saída

# Carregar sons
try:
    sounds = carregar_sons("audios")
except FileNotFoundError as e:
    print(e)
    cap.release()
    out.release()
    pygame.quit()
    exit()

# Configurações
num_trials = 30  # Número total de tentativas
prob_6 = 0.15    # Probabilidade do número 6 (~15%)

# Criar sequência garantindo que o número 6 apareça 15% das vezes
num_6 = int(num_trials * prob_6)
num_outros = num_trials - num_6
numeros = [1, 2, 3, 4, 5, 7, 8, 9]  # Todos os números exceto 6

sequencia = [6] * num_6 + random.choices(numeros, k=num_outros)
random.shuffle(sequencia)  # Embaralha a sequência



# Contagem regressiva antes de iniciar a gravação usando áudios
for i in range(5, 0, -1):
    sounds[str(i)].play()
    time.sleep(sounds[str(i)].get_length())  # Espera o tempo do áudio real

# Tocar o som do apito antes de iniciar a gravação
sounds["apito"].play()
time.sleep(sounds["apito"].get_length())  # Espera o tempo do apito

# Variável para controlar a gravação
gravando = threading.Event()
gravando.set()

# Criar um evento para sincronizar a gravação após o apito
gravar_video_evento = threading.Event()

# Iniciar a gravação em uma thread separada, mas sem começar até o apito
thread_gravacao = threading.Thread(target=gravar_video, args=(cap, out, gravando))
thread_gravacao.start()

# Sinaliza o início da gravação, agora que o apito terminou
gravar_video_evento.set()

# Loop para tocar os sons

clock = pygame.time.Clock()  # Para controle de tempo
start_time = time.time()

try:
    for num in sequencia:
        
        data.append([num,time.time() - start_time])
        sounds[str(num)].play()  # Toca o som correspondente
        if num == 6:
            pygame.time.wait(2000)  
        else:   
            pygame.time.wait(800)  # Espera 1.5 segundos corretamente
except Exception as e:
    print(f"Erro durante a reprodução dos sons: {e}")

# Finalizar gravação

gravando.clear()  # Para a gravação

# Aguardar a finalização da thread de gravação
thread_gravacao.join()

sounds["apito_final"].play()
time.sleep(sounds["apito_final"].get_length())  # Espera o tempo do apito

# Liberar recursos
cap.release()
out.release()
pygame.quit()
print("Recursos liberados. Programa finalizado.")
df = pd.DataFrame(data, columns=["Número Apresentado", "Tempo"])
# Salvar em um arquivo Excel
excel_file = "resultados.xlsx"
df.to_excel(excel_file, index=False, engine="openpyxl")

