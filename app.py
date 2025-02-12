import os
import shutil
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import simpledialog, messagebox

# Variáveis globais
imagem_original = None
imagem_tk = None
canvas = None
scale = 1.0
x_offset = 0
y_offset = 0
start_x = 0
start_y = 0
amostra_atual = 0

# Configuração inicial
pasta_amostras = "C:/SCCON/AMOSTRAS_CLASSIFIC/v1_c04_3589/w_mask_w_poly"  # Substitua pelo caminho correto
amostras = [os.path.join(pasta_amostras, f) for f in sorted(os.listdir(pasta_amostras)) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]

# Solicitar o número da imagem iniciala
def escolher_inicio():
    global amostra_atual

    if not amostras:
        messagebox.showerror("Erro", "Nenhuma amostra encontrada na pasta!")
        root.destroy()
        return

    num_amostra = simpledialog.askinteger("Imagem Inicial", f"Digite o número da imagem inicial (1 - {len(amostras)}):", minvalue=1, maxvalue=len(amostras))
    
    if num_amostra is not None:  # Se o usuário não cancelar
        amostra_atual = num_amostra - 1  # Ajusta para índice de lista (começa em 0)

# Função para classificar a amostra
def classificar_amostra(classe):
    global amostra_atual

    if amostra_atual >= len(amostras):
        return
    
    # Criar pastas de classificação, se não existirem
    for c in ["Aprovada", "Reprovada", "Dúvida"]:
        os.makedirs(os.path.join(pasta_amostras, c), exist_ok=True)

    # Mover a amostra para a pasta correspondente
    destino = os.path.join(pasta_amostras, classe, os.path.basename(amostras[amostra_atual]))
    shutil.copy(amostras[amostra_atual], destino)
    print(f"amostra movida para: {destino}")

    proxima_amostra()

# Função para carregar a amostra atual
def carregar_amostra():
    global imagem_original, imagem_tk, scale, x_offset, y_offset

    if amostra_atual >= len(amostras):
        print("Todas as amostras foram classificadas!")
        root.destroy()
        return

    # Abrir a imagem
    imagem_original = Image.open(amostras[amostra_atual])
    scale = 1.0
    x_offset = 0
    y_offset = 0
    atualizar_imagem()

    # Atualizar o título da janela
    root.title(f"Classificador de amostras ({amostra_atual + 1}/{len(amostras)}) - {amostras[amostra_atual]}")

# Função para atualizar a imagem no canvas
def atualizar_imagem():
    global imagem_original, imagem_tk, scale, x_offset, y_offset

    if imagem_original is None:
        return

    # Redimensionar a imagem conforme o zoom
    largura = int(imagem_original.width * scale)
    altura = int(imagem_original.height * scale)
    imagem_redimensionada = imagem_original.resize((largura, altura), Image.Resampling.LANCZOS)
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)

    # Atualizar o canvas
    canvas.delete("all")
    canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=imagem_tk)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

# Função para dar zoom
def zoom(event):
    global scale
    if event.delta > 0:
        scale *= 1.1  # Aumentar zoom
    else:
        scale /= 1.1  # Diminuir zoom
    atualizar_imagem()

# Função para iniciar o arrastar
def iniciar_arrastar(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

# Função para arrastar a imagem
def arrastar(event):
    global x_offset, y_offset, start_x, start_y
    dx = event.x - start_x
    dy = event.y - start_y
    x_offset += dx
    y_offset += dy
    start_x = event.x
    start_y = event.y
    atualizar_imagem()

# Função para avançar para a próxima amostra
def proxima_amostra():
    global amostra_atual
    if amostra_atual < len(amostras) - 1:
        amostra_atual += 1
        carregar_amostra()
    else:
        print("Todas as amostras foram classificadas!")
        root.destroy()

# Função para voltar para a amostra anterior
def amostra_anterior():
    global amostra_atual
    if amostra_atual > 0:
        amostra_atual -= 1
        carregar_amostra()

# Interface gráfica
root = tk.Tk()
root.withdraw()  # Oculta a janela inicial enquanto pede o número inicial
escolher_inicio()
root.deiconify()  # Exibe a janela depois da entrada do número

root.title("Classificador de amostras")

# Canvas para exibir a imagem, recomendação: width=1900, height=750 - Tela nativa (notebook), root, width=1900, height=950 segunda tela (maior)
canvas = tk.Canvas(root, width=1900, height=950)
canvas.pack()

# Botões de classificação
btn_aprovada = tk.Button(root, text="Aprovada (A)", command=lambda: classificar_amostra("Aprovada"))
btn_aprovada.pack(side=tk.LEFT, padx=10, pady=10)

btn_reprovada = tk.Button(root, text="Reprovada (R)", command=lambda: classificar_amostra("Reprovada"))
btn_reprovada.pack(side=tk.LEFT, padx=10, pady=10)

btn_Dúvida = tk.Button(root, text="Dúvida (D)", command=lambda: classificar_amostra("Dúvida"))
btn_Dúvida.pack(side=tk.LEFT, padx=10, pady=10)

# Atalhos de teclado para classificação
root.bind("a", lambda event: classificar_amostra("Aprovada"))
root.bind("r", lambda event: classificar_amostra("Reprovada"))
root.bind("d", lambda event: classificar_amostra("Dúvida"))

# Atalhos de teclado para navegação
root.bind("<Right>", lambda event: proxima_amostra())  # Próxima imagem
root.bind("<Left>", lambda event: amostra_anterior())  # Imagem anterior

# Eventos de zoom e arrastar
canvas.bind("<MouseWheel>", zoom)  # Zoom com a roda do mouse
canvas.bind("<ButtonPress-1>", iniciar_arrastar)  # Iniciar arrastar
canvas.bind("<B1-Motion>", arrastar)  # Arrastar a imagem

# Carrega a primeira amostra (a partir do número escolhido)
if amostras:
    carregar_amostra()
else:
    print("Nenhuma amostra encontrada na pasta!")
    root.destroy()

# Inicia a interface
root.mainloop()
