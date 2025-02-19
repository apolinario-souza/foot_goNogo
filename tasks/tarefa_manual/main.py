import pygame
import random
import time
import pandas as pd  # Para salvar os dados no Excel

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Configurar tela
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Tela cheia
pygame.display.set_caption("Go/No-Go")
font = pygame.font.Font(None, 100)  # Fonte para exibição de texto

# Carregar sons (garanta que os arquivos '1.wav' a '9.wav' estão na pasta 'audios/')
sounds = {str(i): pygame.mixer.Sound(f"audios/{i}.wav") for i in range(1, 10)}

# Configuração inicial
num_trials = 3  # Total de tentativas
num_sixes = int(num_trials * 0.15)  # 15% das tentativas devem ser o número 6
num_other_trials = num_trials - num_sixes  # Restante das tentativas

# Criar lista com ocorrências do número 6 e distribuir os outros números aleatórios
sequence = ["6"] * num_sixes + [str(random.choice([1, 2, 3, 4, 5, 7, 8, 9])) for _ in range(num_other_trials)]
random.shuffle(sequence)  # Embaralhar a sequência

# Iniciar jogo
print("Pressione a barra de espaço quando ouvir o som do número 6!")
score = 0  # Contador de acertos
errors = 0  # Contador de erros
reaction_times = []  # Lista para armazenar tempos de reação ao número 6
data = []  # Lista para armazenar os dados da planilha

running = True  # Controle do loop principal
very_time = time.time()
for trial, num in enumerate(sequence, start=1):
    if not running:
        break

    # Limpar tela e exibir número sorteado
    screen.fill((0, 0, 0))  # Fundo preto
    text = font.render(f"{num}", True, (255, 255, 255))  # Número branco
    screen.blit(text, (screen.get_width() // 2 - 20, screen.get_height() // 2 - 50))
    pygame.display.flip()

    # Tocar som do número
    sounds[num].play()
    start_time = time.time()
    
    

    pressed = False
    reaction_time = None
    waiting_for_keypress = True  # Flag para esperar input dentro do tempo

    # Tempo limite para resposta: 1.5 segundos
    while time.time() - start_time < .750:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and waiting_for_keypress:
                pressed = True
                reaction_time = time.time() - start_time  # Calcula tempo de reação
                waiting_for_keypress = False  # Não aceita mais inputs para essa tentativa

        if not running:
            break

    # Determinar o resultado da tentativa
    screen.fill((0, 0, 0))  # Fundo preto
    if num == "6" and pressed:
        result_text = f"Acertou! Tempo: {reaction_time:.3f}s"
        score += 1
        reaction_times.append(reaction_time)
        result_type = "Acerto"
    elif num != "6" and pressed:
        result_text = "Erro!"
        errors += 1
        result_type = "Erro"
    elif num == "6" and not pressed:
        result_text = "Erro!"
        errors += 1
        result_type = "Erro!"
    else:
        result_text = ""
        result_type = "Nenhuma resposta"

    print(result_text)

    # Salvar dados da tentativa
    data.append([trial, num, "Sim" if pressed else "Não", result_type, reaction_time if reaction_time else ""])

    # Exibir resultado na tela
    result_display = font.render(result_text, True, (255, 255, 255))
    screen.blit(result_display, (screen.get_width() // 2 - 300, screen.get_height() // 2))
    pygame.display.flip()
    time.sleep(.750)  # Intervalo fixo antes da próxima tentativa


# Exibir mensagem final na tela
screen.fill((0, 0, 0))
final_text = font.render("Encerrado", True, (255, 255, 255))
screen.blit(final_text, (screen.get_width() // 2 - 200, screen.get_height() // 2 - 50))
pygame.display.flip()
time.sleep(1)  # Mostrar resultado por 3 segundos antes de fechar

pygame.quit()

# SALVAR RESULTADOS NO EXCEL
df = pd.DataFrame(data, columns=["Tentativa", "Número Apresentado", "Pressionou?", "Resultado", "Tempo de Reação"])


# Salvar em um arquivo Excel
excel_file = "resultados.xlsx"
df.to_excel(excel_file, index=False, engine="openpyxl")
print(f"\nResultados salvos em: {excel_file}")
