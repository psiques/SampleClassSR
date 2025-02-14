import os
import shutil
from PIL import Image, ImageTk, ImageEnhance
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
janela_thumbnail = None  # Janela flutuante para o thumbnail
thumbnail_label = None  # Label para o thumbnail

# Configuração inicial
pasta_amostras = "C:/SCCON/AMOSTRAS_CLASSIFIC/v1_c04_3850/w_mask_w_poly"  # Pasta das imagens com máscara
pasta_originais = "C:/SCCON/AMOSTRAS_CLASSIFIC/v1_c04_3850/wo_mask_w_poly"  # Pasta das imagens originais
amostras = [os.path.join(pasta_amostras, f) for f in sorted(os.listdir(pasta_amostras)) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]

# Solicitar o número da imagem inicial
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

    # Abrir a imagem com máscara
    imagem_original = Image.open(amostras[amostra_atual])
    scale = 1.0
    x_offset = 0
    y_offset = 0
    atualizar_imagem()

    # Atualizar o título da janela
    root.title(f"Classificador de amostras ({amostra_atual + 1}/{len(amostras)}) - {amostras[amostra_atual]}")

    # Atualizar o thumbnail da imagem original
    atualizar_thumbnail()

# Função para carregar a imagem original
def carregar_imagem_original():
    global pasta_originais, amostras, amostra_atual

    # Obter o nome do arquivo da amostra atual
    nome_arquivo = os.path.basename(amostras[amostra_atual])
    caminho_original = os.path.join(pasta_originais, nome_arquivo)

    if not os.path.exists(caminho_original):
        messagebox.showerror("Erro", f"Imagem original não encontrada: {caminho_original}")
        return None

    return Image.open(caminho_original)

# Função para criar ou atualizar a janela flutuante do thumbnail
def atualizar_thumbnail():
    global janela_thumbnail, thumbnail_label

    # Carregar a imagem original
    imagem_original = carregar_imagem_original()
    if imagem_original is None:
        return

    # Redimensionar a imagem para o thumbnail
    thumbnail_size = (100, 100)  # Tamanho do thumbnail
    thumbnail_image = imagem_original.copy()
    thumbnail_image.thumbnail(thumbnail_size)
    thumbnail_tk = ImageTk.PhotoImage(thumbnail_image)

    # Se a janela do thumbnail não existir, criá-la
    if janela_thumbnail is None or not janela_thumbnail.winfo_exists():
        janela_thumbnail = tk.Toplevel(root)
        janela_thumbnail.overrideredirect(True)  # Remove bordas e botões da janela
        janela_thumbnail.attributes("-topmost", True)  # Mantém a janela no topo
        janela_thumbnail.geometry(f"+{root.winfo_x() + 10}+{root.winfo_y() + 10}")  # Posiciona ao lado da janela principal

        # Adicionar funcionalidade de arrastar
        def iniciar_arrastar_thumbnail(event):
            janela_thumbnail._offset_x = event.x
            janela_thumbnail._offset_y = event.y

        def arrastar_thumbnail(event):
            x = janela_thumbnail.winfo_x() - janela_thumbnail._offset_x + event.x
            y = janela_thumbnail.winfo_y() - janela_thumbnail._offset_y + event.y
            janela_thumbnail.geometry(f"+{x}+{y}")

        janela_thumbnail.bind("<ButtonPress-1>", iniciar_arrastar_thumbnail)
        janela_thumbnail.bind("<B1-Motion>", arrastar_thumbnail)

        # Criar o Label para o thumbnail
        thumbnail_label = tk.Label(janela_thumbnail)
        thumbnail_label.pack()

        # Adicionar evento de duplo clique para exibir a imagem original
        thumbnail_label.bind("<Double-Button-1>", lambda event: exibir_imagem_original())

    # Atualizar o Label do thumbnail
    thumbnail_label.config(image=thumbnail_tk)
    thumbnail_label.image = thumbnail_tk  # Manter uma referência para evitar garbage collection

# Função para exibir a imagem original em tamanho maior
def exibir_imagem_original():
    # Carregar a imagem original
    imagem_original = carregar_imagem_original()
    if imagem_original is None:
        return

    # Criar uma nova janela para exibir a imagem original
    janela_original = tk.Toplevel(root)
    janela_original.title("Imagem Original")

    # Canvas para exibir a imagem original
    canvas_original = tk.Canvas(janela_original, width=imagem_original.width, height=imagem_original.height)
    canvas_original.pack()

    # Variáveis de zoom e offset para a janela da imagem original
    scale_original = 1.0
    x_offset_original = 0
    y_offset_original = 0

    # Função para atualizar a imagem no canvas da janela original
    def atualizar_imagem_original():
        nonlocal scale_original, x_offset_original, y_offset_original

        # Redimensionar a imagem conforme o zoom
        largura = int(imagem_original.width * scale_original)
        altura = int(imagem_original.height * scale_original)
        imagem_redimensionada = imagem_original.resize((largura, altura), Image.Resampling.LANCZOS)
        imagem_tk_original = ImageTk.PhotoImage(imagem_redimensionada)

        # Atualizar o canvas
        canvas_original.delete("all")
        canvas_original.create_image(x_offset_original, y_offset_original, anchor=tk.NW, image=imagem_tk_original)
        canvas_original.config(scrollregion=canvas_original.bbox(tk.ALL))
        canvas_original.image = imagem_tk_original  # Manter uma referência para evitar garbage collection

    # Função para dar zoom na janela da imagem original
    def zoom_original(event):
        nonlocal scale_original
        if event.delta > 0:
            scale_original *= 1.1  # Aumentar zoom
        else:
            scale_original /= 1.1  # Diminuir zoom
        atualizar_imagem_original()

    # Adicionar evento de zoom com a roda do mouse
    canvas_original.bind("<MouseWheel>", zoom_original)

    # Exibir a imagem original inicialmente
    atualizar_imagem_original()

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

# Função para ajustar o contraste
def ajustar_contraste(fator):
    global imagem_original
    if imagem_original is None:
        return
    enhancer = ImageEnhance.Contrast(imagem_original)
    imagem_original = enhancer.enhance(fator)
    atualizar_imagem()

# Função para ajustar o brilho
def ajustar_brilho(fator):
    global imagem_original
    if imagem_original is None:
        return
    enhancer = ImageEnhance.Brightness(imagem_original)
    imagem_original = enhancer.enhance(fator)
    atualizar_imagem()

# Interface gráfica
root = tk.Tk()
root.withdraw()  # Oculta a janela inicial enquanto pede o número inicial
escolher_inicio()
root.deiconify()  # Exibe a janela depois da entrada do número

root.title("Classificador de amostras")

# Canvas para exibir a imagem
canvas = tk.Canvas(root, width=1900, height=950)
canvas.pack()

# Botões de classificação
btn_aprovada = tk.Button(root, text="Aprovada (A)", command=lambda: classificar_amostra("Aprovada"))
btn_aprovada.pack(side=tk.LEFT, padx=10, pady=10)

btn_Dúvida = tk.Button(root, text="Dúvida (D)", command=lambda: classificar_amostra("Dúvida"))
btn_Dúvida.pack(side=tk.LEFT, padx=10, pady=10)

btn_reprovada = tk.Button(root, text="Reprovada (R)", command=lambda: classificar_amostra("Reprovada"))
btn_reprovada.pack(side=tk.LEFT, padx=10, pady=10)

# Botões para ajustar contraste e brilho
btn_contraste_mais = tk.Button(root, text="Contraste +", command=lambda: ajustar_contraste(1.2))
btn_contraste_mais.pack(side=tk.LEFT, padx=10, pady=10)

btn_contraste_menos = tk.Button(root, text="Contraste -", command=lambda: ajustar_contraste(0.8))
btn_contraste_menos.pack(side=tk.LEFT, padx=10, pady=10)

btn_brilho_mais = tk.Button(root, text="Brilho +", command=lambda: ajustar_brilho(1.2))
btn_brilho_mais.pack(side=tk.LEFT, padx=10, pady=10)

btn_brilho_menos = tk.Button(root, text="Brilho -", command=lambda: ajustar_brilho(0.8))
btn_brilho_menos.pack(side=tk.LEFT, padx=10, pady=10)

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
