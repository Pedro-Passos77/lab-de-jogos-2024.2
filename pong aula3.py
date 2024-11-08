from PPlay.gameimage import *
from PPlay.window import *
from PPlay.collision import *
from PPlay.sprite import *

# Criar janela e objetos do jogo
janela = Window(1280, 720)
janela.set_title("PONG")

controle = janela.get_keyboard()

# Placar dos jogadores
placar_jogador1 = 0
placar_jogador2 = 0

cenario = GameImage("C:/Users/pedro/OneDrive/Documentos/Projeto Pong/codigo/Background.png")
bola = GameImage("C:/Users/pedro/OneDrive/Documentos/Projeto Pong/codigo/Ball.png")
pad1 = GameImage("C:/Users/pedro/OneDrive/Documentos/Projeto Pong/codigo/Paddle_1.png")
pad2 = GameImage("C:/Users/pedro/OneDrive/Documentos/Projeto Pong/codigo/Paddle_2.png")

# Tamanho da bola
bola.height = 30
bola.width = 30

# Parâmetro de velocidade dos pads
VelPad = 200
# Velocidade da bola
velBallY = 100
velBallX = 100

# Posição inicial dos pads e da bola
pad1.y = janela.height / 2 - pad1.height / 2
pad2.y = janela.height / 2 - pad2.height / 2
pad1.x = 0
pad2.x = janela.width - pad2.width
bola.x = janela.width / 2 - bola.width / 2
bola.y = janela.height / 2 - bola.height / 2

# Iniciar movimento da bola
movendo = False

# Armazenar o delta_time do quadro anterior
delta_time_anterior = 0

while True:
    # Salva o delta_time atual para o cálculo do movimento
    delta_time_atual = janela.delta_time()

    # Desenha os objetos
    cenario.draw()
    pad1.draw()
    pad2.draw()
    bola.draw()

    # Detecta o início do movimento ao pressionar "Espaço"
    if controle.key_pressed("SPACE"):
        movendo = True  # Inicia o movimento da bola

    if movendo:
        # Atualiza a posição da bola com base no delta_time anterior
        bola.x += velBallX * delta_time_anterior
        bola.y += velBallY * delta_time_anterior
    else:
        # Reinicia a posição da bola quando não estiver em movimento
        bola.x = janela.width / 2 - bola.width / 2
        bola.y = janela.height / 2 - bola.height / 2

    # Controle do pad esquerdo
    if controle.key_pressed("w"):
        pad1.y -= VelPad * janela.delta_time()
    elif controle.key_pressed("s"):
        pad1.y += VelPad * janela.delta_time()

    # Movimento da IA para o pad direito
    if bola.x > janela.width / 2:
        if bola.y > pad2.y + pad2.height / 2:
            pad2.y += VelPad * janela.delta_time()
        elif bola.y < pad2.y + pad2.height / 2:
            pad2.y -= VelPad * janela.delta_time()

    # Verifica quando a bola ultrapassa a tela
    if bola.x <= 0:  # A bola ultrapassou o lado esquerdo
        placar_jogador2 += 1
        movendo = False  # Para a partida
        velBallX = 100   # Redefinir velocidade para o padrão
        velBallY = 100   # Redefinir velocidade para o padrão
        bola.x = janela.width / 2 - bola.width / 2  # Coloca a bola no centro novamente
        bola.y = janela.height / 2 - bola.height / 2  # Coloca a bola no centro novamente
    elif bola.x >= janela.width:  # A bola ultrapassou o lado direito
        placar_jogador1 += 1
        movendo = False  # Para a partida
        velBallX = 100   # Redefinir velocidade para o padrão
        velBallY = 100   # Redefinir velocidade para o padrão
        bola.x = janela.width / 2 - bola.width / 2  # Coloca a bola no centro novamente
        bola.y = janela.height / 2 - bola.height / 2  # Coloca a bola no centro novamente

    # Colisão com os pads
    if bola.collided(pad1):
        velBallX *= -1
        velBallY *= -1
        if velBallY < 0:
            velBallY -=  20  # acelera com a colisão
        else: velBallY += 20
        if velBallX < 0:
            velBallX -=  20  # acelera com a colisão
        else: velBallX += 20

    if bola.collided(pad2):
        velBallX *= -1
        velBallY *= -1
        if velBallY < 0:
            velBallY -=  20  # acelera com a colisão
        else: velBallY += 20
        if velBallX < 0:
            velBallX -=  20  # acelera com a colisão
        else: velBallX += 20

    # Colisão com a parede superior (y = 0)
    if bola.y <= 0:
        velBallY *= -1  # Inverte a direção vertical da bola
        if velBallY < 0:
            velBallY -=  20  # acelera com a colisão
        else: velBallY += 20

    # Colisão com a parede inferior (janela.height - bola.height)
    if bola.y >= janela.height - bola.height:
        velBallY *= -1  # Inverte a direção vertical da bola
        if velBallY < 0:
            velBallY -=  20  # acelera com a colisão
        else: velBallY += 20

    # Limita os pads dentro da janela
    if pad1.y < 0:
        pad1.y = 0
    elif pad1.y + pad1.height > janela.height:
        pad1.y = janela.height - pad1.height

    if pad2.y < 0:
        pad2.y = 0
    elif pad2.y + pad2.height > janela.height:
        pad2.y = janela.height - pad2.height

    # Exibição do placar
    janela.draw_text(f"|Player|: {velBallY}", 50, 50, size=30, color=(255, 255, 255))
    janela.draw_text(f"|PC|: {velBallX}", janela.width - 150, 50, size=30, color=(255, 255, 255))

    # Atualização da janela
    janela.update()

    # Atualiza o delta_time anterior
    delta_time_anterior = delta_time_atual
