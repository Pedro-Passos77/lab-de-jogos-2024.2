from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.mouse import *
from PPlay.keyboard import *
from PPlay.sound import *
import random


# Definições básicas
janela = Window(1792, 1024)
janela.set_title("Space Invaders")
controle = janela.get_keyboard()
mouse = Mouse()
teclado = Keyboard()

# Recursos do jogo
fundo_menu = GameImage("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/bgmenu.png")
fundo_jogo = GameImage("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/fundojogo.png")
player = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/naverigby1.png", 1)
musica = Sound("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/garyvsdavid.mp3")
somtiro = Sound("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/tiro.mp3")
mordecai3 = GameImage("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/mordecai3.png")
mordecai2 =  GameImage("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/mordecai2.png")
mordecai1 = GameImage("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/mordecai1.png")
rigby3 = GameImage("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/rigby3.png")
rigby2 = GameImage("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/rigby2.png")
rigby1 = GameImage("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/rigby1.png")
fundoperdeu = GameImage("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/gameover.png")

# variaveis
player.set_position(janela.width / 2 - player.width / 2, janela.height - 200)
XLR8_nave = 1500
tiros = []
velocidade_tiro = 3000
cooldown_tiro = 1
tempo_ultimo_tiro = 0
STR = 1
tempo_clique = 0
vidas = 3
mordecai3.x = 400
mordecai3.y = 830
rigby3.x = 500
rigby3.y = 830
mordecai2.x = 400
mordecai2.y = 830
rigby2.x = 500
rigby2.y = 830
mordecai1.x = 400
mordecai1.y = 830
rigby1.x = 500
rigby1.y = 830
rodadas = 1
ultimo_check = 0  # Armazena o tempo do último check
transparencia_atual = 255  # Transparência inicial do sprite (totalmente opaco)
transparencia_minima = 50  # Transparência mínima para o efeito de invisibilidade
cooldown_colisao = 2 # Cooldown de 2 segundo

# Configurações dos inimigos
inimigos = []
XLR8_inimigos = 500
i = random.randint(3, 3)
j = random.randint(5, 5)
fr_frames = 0
fr_timer = 0
fr_fps = 0
velocidade_tiro_inimigo = 500
# Estado do jogo
estado = 0  # 0 = Menu, 1 = Jogo, 2 = Tela de dificuldade
dificuldade = 1
score = 0
PatoMode = False

# Botões do menu
botoes = [
    Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/start.png"),
    Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/diff.png"),
    Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/ranking.png"),
    Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/exit.png"),
]

# Botões de dificuldade
botao_dificuldade_1 = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/easy.png")
botao_dificuldade_2 = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/normal.png")
botao_dificuldade_3 = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/hard.png")
botao_voltar = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/exit.png")

# Configuração dos botões
for idx, botao in enumerate(botoes):
    botao.x = janela.width / 2 - botao.width / 2 + 25
    botao.y = janela.height - (450 - idx * 100)

# Configuração dos botões de dificuldade
botao_dificuldade_1.x = janela.width / 2 - botao_dificuldade_1.width / 2 + 25
botao_dificuldade_1.y = janela.height - 450 - 30

botao_dificuldade_2.x = janela.width / 2 - botao_dificuldade_2.width / 2 + 25
botao_dificuldade_2.y = janela.height - 350 - 30

botao_dificuldade_3.x = janela.width / 2 - botao_dificuldade_3.width / 2 + 25
botao_dificuldade_3.y = janela.height - 250 - 30

botao_voltar.x = janela.width / 2 - botao_voltar.width / 2  + 25
botao_voltar.y = janela.height - 150 - 30

# Funções auxiliares
def colisao_tiros():
    global tiros_inimigos, tiros, score, rodadas  # Variáveis globais que armazenam os tiros
    for tiro_inimigo in tiros_inimigos[:]:  # Itera sobre uma cópia da lista de tiros inimigos
        for tiro_jogador in tiros[:]:  # Itera sobre uma cópia da lista de tiros do jogador
            if tiro_inimigo.collided(tiro_jogador):  # Verifica a colisão entre o tiro inimigo e do jogador
                tiros_inimigos.remove(tiro_inimigo)  # Remove o tiro inimigo em caso de colisão
                tiros.remove(tiro_jogador)  # Remove o tiro do jogador também
                score = score + random.randint(1, 10) * rodadas

# Lista de tiros dos inimigos
tiros_inimigos = []

# Função para gerar tiros dos inimigos
def disparar_inimigos():
    global rodadas
    global tiros_inimigos
    for linha in inimigos:
        for inimigo in linha:
            # Cada inimigo dispara aleatoriamente com um tempo entre os disparos
            if random.random() < 0.001:  # Chance de disparo por frame
                if rodadas == 1:
                    tiro_inimigo = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/tiroloiro.png", 1)
                    tiro_inimigo.x = inimigo.x + inimigo.width / 2 - tiro_inimigo.width / 2
                    tiro_inimigo.y = inimigo.y + inimigo.height
                    tiros_inimigos.append(tiro_inimigo)
                    tiroloiro = Sound("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/tiroloiro.mp3")
                    tiroloiro.play()
                elif rodadas <= 3:
                    Qprojetil = random.randint(1,3)
                    if Qprojetil == 1:
                        tiro_inimigo = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/garçomcolher.png", 1)
                        tiro_inimigo.x = inimigo.x + inimigo.width / 2 - tiro_inimigo.width / 2
                        tiro_inimigo.y = inimigo.y + inimigo.height
                        tiros_inimigos.append(tiro_inimigo)
                        tirogarçom = Sound("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/garçomsom.mp3")
                        tirogarçom.play()
                    elif Qprojetil == 2:
                        tiro_inimigo = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/garçomgarfo.png", 1)
                        tiro_inimigo.x = inimigo.x + inimigo.width / 2 - tiro_inimigo.width / 2
                        tiro_inimigo.y = inimigo.y + inimigo.height
                        tiros_inimigos.append(tiro_inimigo)
                        tirogarçom = Sound("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/garçomsom.mp3")
                        tirogarçom.play()
                    elif Qprojetil == 3:
                        tiro_inimigo = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/garçomfaca.png", 1)
                        tiro_inimigo.x = inimigo.x + inimigo.width / 2 - tiro_inimigo.width / 2
                        tiro_inimigo.y = inimigo.y + inimigo.height
                        tiros_inimigos.append(tiro_inimigo)
                        tirogarçom = Sound("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/garçomsom.mp3")
                        tirogarçom.play()
                elif rodadas <= 5:
                        Qprojetil = random.randint(1,2)
                        if Qprojetil == 1:
                            tiro_inimigo = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/tiropa.png", 1)
                            tiro_inimigo.x = inimigo.x + inimigo.width / 2 - tiro_inimigo.width / 2
                            tiro_inimigo.y = inimigo.y + inimigo.height
                            tiros_inimigos.append(tiro_inimigo)
                            tirodigchamp = Sound("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/gbo.mp3")
                            tirodigchamp.play()
                        elif Qprojetil == 2:
                            tiro_inimigo = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/tiropica.png", 1)
                            tiro_inimigo.x = inimigo.x + inimigo.width / 2 - tiro_inimigo.width / 2
                            tiro_inimigo.y = inimigo.y + inimigo.height
                            tiros_inimigos.append(tiro_inimigo)
                            tirodigchamp = Sound("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/gbo.mp3")
                            tirodigchamp.play()
                elif rodadas <= 7:
                    tiro_inimigo = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/tirogbo.png", 1)
                    tiro_inimigo.x = inimigo.x + inimigo.width / 2 - tiro_inimigo.width / 2
                    tiro_inimigo.y = inimigo.y + inimigo.height
                    tiros_inimigos.append(tiro_inimigo)
                    tirogbo = Sound("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/gbo.mp3")
                    tirogbo.play()
                       
                elif rodadas <= 10:
                    tiro_inimigo = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/gansotiro.png", 1)
                    tiro_inimigo.x = inimigo.x + inimigo.width / 2 - tiro_inimigo.width / 2
                    tiro_inimigo.y = inimigo.y + inimigo.height
                    tiros_inimigos.append(tiro_inimigo)
                    tiroganso = Sound("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/gbo.mp3")
                    tiroganso.play()
                elif  rodadas > 10:    
                    if random.random() < 0.5:  # Chance de o inimigo atirar
                    
                        tiro_inimigo = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/tirogbo.png", 1)
                        tiro_inimigo.x = inimigo.x + inimigo.width / 2 - tiro_inimigo.width / 2  # Posiciona o tiro no centro do inimigo
                        tiro_inimigo.y = inimigo.y + inimigo.height  # Posiciona o tiro abaixo do inimigo
                        tiros_inimigos.append(tiro_inimigo)  # Adiciona o tiro à lista de tiros dos inimigos
                        tirogbo = Sound("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/gbo.mp3")
                        tirogbo.play()  # Toca o som do tiro

                     

# Função para mover os tiros dos inimigos
def mover_tiros_inimigos():
    global tiros_inimigos
    for tiro in tiros_inimigos[:]:
        tiro.y += velocidade_tiro_inimigo * janela.delta_time()  # Velocidade do tiro inimigo
        if tiro.y > janela.height:
            tiros_inimigos.remove(tiro)
        else:
            tiro.draw()

# Função para verificar colisões entre tiros inimigos e o jogador
def verificar_colisoes_inimigos(vidas):
    global tiros_inimigos, player, estado, ultimo_check, cooldown_colisao
    
    # Atualiza o tempo de cooldown usando delta_time
    ultimo_check += janela.delta_time()  # Chama delta_time como função
    
    # Verifica se já passaram os segundos definidos para o cooldown de colisão
    if ultimo_check >= cooldown_colisao:
        # Verificação de colisões
        for tiro in tiros_inimigos[:]:
            if tiro.collided(player):  # Se o tiro atingir o jogador, o jogador perde vida
                tiros_inimigos.remove(tiro)
                vidas -= 1  # Subtrai 1 vida
                player.x = janela.width / 2  # Reposiciona o jogador
                
                # Reseta o contador de cooldown
                ultimo_check = 0

                # Estado de Game Over, se o jogador perder todas as vidas
                if vidas == 0:
                    estado = 4  # Mudar para estado de game over
                    
    return vidas


       

    




# Encerrar o jogo vitoria / derrota 
def recriar_inimigos():
    global rodadas, XLR8_inimigos
    inimigos_vivos = sum(len(linha) for linha in inimigos)
    if inimigos_vivos == 0:
        rodadas = rodadas +1
        XLR8_inimigos += 50
        criar_inimigos(i, j)
        return rodadas

   
def verificar_derrota():
    global estado
    # Verifica se algum inimigo na última linha está abaixo do jogador
    for inimigo in inimigos[-1]:  # Acessa a última linha da matriz de inimigos
        if inimigo.y > player.y:  # Verifica se o inimigo está abaixo do jogador
            estado = 4  # Muda o estado para "Game Over"
            break
        elif inimigo.collided(player):
            estado = 4  # Muda o estado para "Game Over"
            break


def organiza(file):
    try:
        with open(file, 'r') as arquivo:
            pontuacao = [line.strip() for line in arquivo if line.strip()]  # Remove espaços e linhas vazias
        return pontuacao
    except FileNotFoundError:
        return []  # Retorna uma lista vazia se o arquivo não for encontrado

# Variável para garantir que o nome seja capturado apenas uma vez
nome_inserido = False

# Função chamada quando o jogo acaba (Estado 4)
def fim_de_jogo():
    global score, nome_inserido

    if not nome_inserido:  # Verifica se o nome já foi inserido
        fundoperdeu.draw()  # Exibe o fundo de fim de jogo

        # Exibe o texto da pontuação
        janela.draw_text(f"Score: {score}", janela.width / 2 - 100, janela.height / 2, 30, (255, 255, 255), "Arial")

        # Pergunta o nome do jogador e salva a pontuação
        janela.draw_text("Digite seu nome no terminal", janela.width / 2 - 150, janela.height / 2 + 50, 30, (255, 255, 255), "Arial")

        # Aguarda o jogador inserir o nome no terminal
        nome = input("Digite seu nome: ").strip()

        # Adiciona a nova pontuação ao arquivo
        try:
            with open('C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/Pontuacao.txt', 'r') as arquivo:
                conteudo = arquivo.readlines()
        except FileNotFoundError:
            conteudo = []

        # Adiciona a pontuação
        conteudo.append(f"{score} - {nome}\n")

        # Salva a pontuação no arquivo
        with open('C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/Pontuacao.txt', 'w') as arquivo:
            arquivo.writelines(conteudo)

        nome_inserido = True  # Marca que o nome foi inserido

        estado = 5  # Muda para o estado 5 (ranking)



# Função chamada para exibir o ranking (Estado 5)
def rank():
    # Organiza as pontuações
    pontuacao = organiza('C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/Pontuacao.txt')
    pontuacao.sort(reverse=True)

    # Exibe o fundo do jogo
    fundo_jogo.draw()

    altura = 150
    limite = 0
    for i, conteudo in enumerate(pontuacao):
        if limite < 5:  # Mostra apenas os 5 primeiros
            janela.draw_text(f"{i + 1}. {conteudo}", (janela.width / 2) - 120, altura + 200, size=36, font_name="Arial", bold=True, color=[255, 255, 255])
            altura += 45
            limite += 1

    janela.draw_text("RANKING", (janela.width / 2) - 130, 250, size=48, font_name="Arial", bold=True, color=[255, 255, 255])

    while True:
        if teclado.key_pressed("esc"):
            estado = 0  # Voltar ao menu principal               
            vidas = 3
            score = 0
            rodadas = 1
            criar_inimigos(random.randint(3, 7), random.randint(5, 7))
            break

        janela.update()
        
# Função verificar fps
def exibir_fps(janela):
    global fr_frames, fr_timer, fr_fps

    # Incrementa o contador de frames e o temporizador
    fr_frames += 1
    fr_timer += janela.delta_time()

    # Exibe o FPS no canto inferior esquerdo da tela
    janela.draw_text("FPS: {:.1f}".format(fr_fps), janela.width - 300 , 100, 30, (255, 255, 255), "Arial")
    # Atualiza o FPS a cada segundo
    if fr_timer >= 1:
        fr_fps = fr_frames  # Define o FPS
        fr_timer = 0  # Reseta o temporizador
        fr_frames = 0  # Reseta o contador de frames

def criar_inimigos(linhas, colunas):
    global inimigos, rodadas
    inimigos = []
    if rodadas == 1:
        sprite_inimigo = "C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/blondeguy.png"
    elif rodadas <= 3:
        sprite_inimigo = "C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/garçom.png"
    elif rodadas <= 5:
        sprite_inimigo = "C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/joaofortao.png"
    elif rodadas <= 7:
        sprite_inimigo = "C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/GBO.png"
    elif rodadas <= 10:
        sprite_inimigo = "C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/ganso.png"
    else:
            sprite_inimigo = "C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/dest.png"
    
    
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            inimigo = Sprite(sprite_inimigo, 1)
            inimigo.x = 100 + j * 100
            inimigo.y = 50 + i * 100
            linha.append(inimigo)
        inimigos.append(linha)
    

def desenhar_inimigos():
    for linha in inimigos:
        for inimigo in linha:
            inimigo.draw()


def mover_inimigos():
    global XLR8_inimigos
    for linha in inimigos:
        for inimigo in linha:
            inimigo.x += XLR8_inimigos * janela.delta_time()
            if inimigo.x < 55 or inimigo.x  > janela.width - 210 :
                XLR8_inimigos = -XLR8_inimigos
                for linha_descida in inimigos:
                    for inimigo_descida in linha_descida:
                        inimigo_descida.y += 30
                break
            

def verificar_colisoes():
    global tiros, inimigos, score, rodadas
    for tiro in tiros[:]:
        for linha in inimigos:
            for inimigo in linha[:]:
                if tiro.collided(inimigo):
                    tiros.remove(tiro)
                    linha.remove(inimigo)
                    score += 10 * rodadas
                    break


# Configuração inicial
criar_inimigos(i, j)


# Definição da variável referente ao estado do jogo (0 = Menu, 1 = Gameplay, 2 = Tela de dificuldade)
estado = 0
#alterar volumes
somtiro.set_volume(30)
musica.set_repeat(True)

if estado == 4:
    fim_de_jogo()
# Game Loop
while True:
    if  rodadas > 12 and teclado.key_pressed("p"):
        player = GameImage("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/superpato.png")
        player.y = janela.height - player.height *2
        player.x = janela.width/2
        PatoMode = True
        if teclado.key_pressed("esc"): 
            player = GameImage("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/naverigby1.png")
    
    
    

    if estado == 0:  # Menu
        fundo_menu.draw()
        STR = 1
        for botao in botoes:
            botao.draw()

        if mouse.is_over_object(botoes[0]) and mouse.is_button_pressed(1):
            estado = 1
        elif mouse.is_over_object(botoes[1]) and mouse.is_button_pressed(1):
            estado = 2
        elif mouse.is_over_object(botoes[3]) and mouse.is_button_pressed(1):
            janela.close()
        if mouse.is_over_object(botoes[2]) and mouse.is_button_pressed(1):
            estado = 5 # Quando o botão de ranking for pressionado, exibe o ranking
    if estado == 2:  # Tela de dificuldade
        fundo_menu.draw()
        botao_dificuldade_1.draw()
        botao_dificuldade_2.draw()
        botao_dificuldade_3.draw()
        botao_voltar.draw()
        if teclado.key_pressed("esc"):
            estado = 0

        tempo_clique += janela.delta_time()

        if tempo_clique >= cooldown_tiro:
            if mouse.is_over_object(botao_dificuldade_1) and mouse.is_button_pressed(1):
                dificuldade = 1
                estado = 1
                tempo_clique = 0
            elif mouse.is_over_object(botao_dificuldade_2) and mouse.is_button_pressed(1):
                dificuldade = 2
                estado = 1
                tempo_clique = 0
            elif mouse.is_over_object(botao_dificuldade_3) and mouse.is_button_pressed(1):
                dificuldade = 3
                estado = 1
                tempo_clique = 0
            elif mouse.is_over_object(botao_voltar) and mouse.is_button_pressed(1):
                estado = 0
                tempo_clique = 0
       

    
    if estado == 1:  # Jogo
        verificar_derrota()
        fundo_jogo.draw()
        player.draw()
        desenhar_inimigos()
        if vidas == 3:
            mordecai3.draw()
            rigby3.draw()
        elif vidas == 2:
            mordecai2.draw()
            rigby2.draw()
        elif vidas == 1:
            mordecai1.draw()
            rigby1.draw()
        janela.draw_text(f"Score: {score}", 150, 100, 30, (255, 255, 255), "Arial")
        janela.draw_text(f"Estado dos Pilotos:", 150, janela.height - 130, 30, (255, 255, 255), "Arial")
        exibir_fps(janela)
        if controle.key_pressed("esc"):
            estado = 0  # Voltar ao menu principal               
            vidas = 3
            score = 0
            rodadas = 1
            criar_inimigos(random.randint(3, 7), random.randint(5, 7))
        
        # Movimentação do jogador
        if controle.key_pressed("a"):
            player.x -= XLR8_nave * janela.delta_time()
        if controle.key_pressed("d"):
            player.x += XLR8_nave * janela.delta_time()
        if player.x < 0:
            player.x = 0
        if player.x + player.width > janela.width:
            player.x = janela.width - player.width

         # Dificuldades mudanças
        if STR == 1:
            if dificuldade == 2:
                XLR8_nave = 1000
                velocidade_tiro = 2000
                XLR8_inimigos = -1000
                velocidade_tiro_inimigo = 1000
                STR = 0
            elif dificuldade == 3:
                XLR8_nave = 500
                velocidade_tiro = 1000
                XLR8_inimigos = 1500
                velocidade_tiro_inimigo = 1500
                STR = 0
            elif dificuldade == 1:
                XLR8_nave = 1500
                velocidade_tiro = 3000
                XLR8_inimigos = 500
                velocidade_tiro_inimigo = 500
                STR = 0
        # Colisão paredes player
        if player.x > 1600:
            player.x = 1600

        if player.x < 130:
            player.x = 130
        
        # Tiros do jogador
        disparar_inimigos()
        vidas = verificar_colisoes_inimigos(vidas)
        colisao_tiros()
        mover_tiros_inimigos()
        tempo_ultimo_tiro += janela.delta_time()
        if controle.key_pressed("space") and tempo_ultimo_tiro >= cooldown_tiro:
            somtiro.play()
            tiro = Sprite("C:/Users/pedro/OneDrive/Documentos/SpaceInvaders/tirorigby.png", 1)
            tiro.x = player.x + player.width / 2 - tiro.width / 2
            tiro.y = player.y
            tiros.append(tiro)
            tempo_ultimo_tiro = 0
        # Atualização dos tiros
        for tiro in tiros[:]:
            tiro.y -= velocidade_tiro * janela.delta_time()
            if tiro.y < 0:
                tiros.remove(tiro)
            else:
                tiro.draw()
        # Movimentação e colisões dos inimigos
        mover_inimigos()
        verificar_colisoes()
        recriar_inimigos()
        # Interface do jogador
    if estado == 4:
        fim_de_jogo()

        # Perguntar o nome e salvar no ranking
        if teclado.key_pressed("enter"):  # Quando pressionar Enter
            estado = 5

        if teclado.key_pressed("esc"):
            estado = 0  # Voltar ao menu principal               
            vidas = 3
            score = 0
            rodadas = 1
            criar_inimigos(random.randint(3, 7), random.randint(5, 7), score)

    if estado == 5:
        fundo_jogo.draw()
        rank()

        if teclado.key_pressed("esc"):
            estado = 0  # Voltar ao menu principal               
            vidas = 3
            score = 0
            rodadas = 1
            criar_inimigos(random.randint(3, 7), random.randint(5, 7))

    janela.update()