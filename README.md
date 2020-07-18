# wm2020
Código para o artigo WM 2020

## Atividades
1. Treinar uma rede para fazer segmentação humana (usar o dataset supervise.ly)
    1. [OK] Baixar o dataset supervise.ly human segmentation 
    1. [OK] Baixar um modelo de rede de segmentação 
    1. [OK] Testar e ajustar a rede até que funcione corretamente
    1. Adaptar a rede para usar o dataset supervis.ly
    1. Treinar a rede com o novo dataset 
2. Usar a nova rede para gerar novas silhuetas a partir das imagens no dataset CASIA-B
    1. baixar os vídeos do CASIAB - Enviar o release agreement preenchido
3. Preparar um modelo de reconhecimento de GEI
    1.  Treinar e avaliar o modelo utilizando as silhuetas originais do CASIA-B
        1.  [OK] Baixar as silhuetas originais do CASIA-B
    2.  Treinar e avaliar o modelo utilizando as novas silhuetas segmentadas do CASIA-B
4. Comparar os resultados
5. Ligar as redes de segmentação e de reconhecimento de GEI (deixar que o bacKpropagation determine qual é a melhor representação)
6. Comparar os resultados

