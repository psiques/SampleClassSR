# Classificador de Amostras

Este script permite visualizar e classificar imagens em diferentes categorias, movendo-as para pastas específicas. A interface foi desenvolvida em Python usando a biblioteca Tkinter.

## Funcionalidades
- Carregamento de imagens a partir de uma pasta definida.
- Classificação das imagens como "Aprovada", "Reprovada" ou "Dúvida".
- Navegação entre as imagens.
- Zoom e movimentação da imagem.
- Atalhos de teclado para facilitar a classificação.

## Requisitos
- Python 3.x
- Bibliotecas necessárias:
  - `Pillow`
  - `tkinter`

## Estrutura do Projeto
O script procura imagens na pasta definida na variável `pasta_amostras` e exibe uma interface para classificação. As imagens são movidas para subpastas de acordo com a classificação.

## Como Usar
1. Defina a pasta de imagens na variável `pasta_amostras`.
2. Execute o script.
3. Escolha a imagem inicial.
4. Use os botões ou atalhos para classificar as imagens.
5. As imagens classificadas serão movidas para suas respectivas pastas.

## Controles
- `A`: Classifica como "Aprovada"
- `R`: Classifica como "Reprovada"
- `D`: Classifica como "Dúvida"
- `→`: Avança para a próxima imagem
- `←`: Retorna para a imagem anterior
- Scroll do mouse: Zoom in/out
- Clique e arraste: Move a imagem na tela

## Melhorias Futuras
- Adicionar suporte para desfazer a última classificação.
- Melhorar a interface gráfica com mais opções visuais.
- Armazenar um log das classificações realizadas.

---

Este projeto foi desenvolvido para facilitar a organização e revisão de imagens de amostras.
