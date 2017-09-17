import pygame, sys
from pygame.locals import *

# Aclaraciones
# Requiere "pygame" para las graficas
#
#  Se grafican las figuras para una mejor comprencion pero como son coordenadas tan pequenas no se muestran bien
# (aumentando las proporciones pude verse mejo)
# pero la orden del problema no lo permite.
#
# La solucion trate de buscarla matematicamente
#   1- para saber si es ciudadano o prisionero :
#       comprobamos si el punto esta fuera o dentro de un poligono o en uno de sus vertices
#

# definiendo colores
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
CAFE = (90, 50, 15)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)

# Abriendo Fichero
infile = open('texto.txt', 'r')
for line in infile:
    lista = line
    pygame.init()
    # Asignando dimenciones a la ventana
    dimensiones = (500, 500)
    pantalla = pygame.display.set_mode(dimensiones)

    # asignando nombre de la ventana
    pantalla.fill(BLANCO)  # rellenando ventana
    terminar = False

    reloj = pygame.time.Clock()

    while not terminar:
        for Evento in pygame.event.get():
            if Evento.type == pygame.QUIT:
                terminar = True

        # limpiando lista y declarando variables
        lista = lista.replace(" ", ",").replace("|", ",")
        lista_limpa = lista.split(",")
        lista_x = []
        lista_y = []
        longitud = len(lista_limpa)
        poligono = []
        #separando las cordenadas X,Y y conformando el Poligono
        i = 0
        while i < longitud - 2:
            cordenada_x = int(lista_limpa[i])
            if (cordenada_x >= 0 and cordenada_x <= 10):
                temp_x = int(lista_limpa[i])    # aca se puede aumentar las proporciones
                lista_x.append(temp_x)
            j = i + 1
            cordenada_y = int(lista_limpa[j])
            if (cordenada_y >= 0 and cordenada_y <= 10):
                temp_y = int(lista_limpa[j])    # aca se puede aumentar las proporciones
                lista_y.append(temp_y)

            poligono.append((temp_x, temp_y))
            i = i + 2

        #  Preparando las cordenadas para dibujar P (puntos de rectas ) D para las diagonales
        # o rectas de cierre de la figura
        i = 0
        while i < len(lista_x):
            px = int(lista_x[i])
            py = int(lista_y[i])
            pxx = int(lista_x[i + 1])
            pyy = int(lista_y[i + 1])
            if i == 0:
                dx = int(lista_x[i])
                dy = int(lista_y[i])
                dxx = int(lista_x[i + 3])
                dyy = int(lista_y[i + 3])
            if i == 2:
                dx = int(lista_x[i - 1])
                dy = int(lista_y[i - 1])
                dxx = int(lista_x[i])
                dyy = int(lista_y[i])
            #dibujando la figura
            pygame.draw.line(pantalla, ROJO, [px, py], [pxx, pyy], 2)
            pygame.draw.aaline(pantalla, ROJO, [dx, dy], [dxx, dyy], True)
            i = i + 2
            #campturando los puntos del usuario
            punto_x = int(lista_limpa[len(lista_limpa) - 2])
            punto_y = int(lista_limpa[len(lista_limpa) - 1])
            #aplicando restricciones
            if punto_y >= 3 and punto_y <= 12 and punto_x >= 3 and punto_x <= 12:
                punto_x = punto_x
                punto_y = punto_y
                pygame.draw.circle(pantalla, CAFE, [punto_x, punto_y], 1) #dibujando el .

            #metodo para definir si el punto esta dentro o fuera del poligono
            def punto_en_poligono(x, y, poligono):
                i = 0
                j = len(poligono) - 1
                salida = 0
                for i in range(len(poligono)):
                    # condicion para saber si el punto esta en uno de los vertices de la figura
                    if poligono[i][0] == x and poligono[i][1] == y:
                        salida = 2
                        break
                    if (poligono[i][1] < y and poligono[j][1] >= y) or (poligono[j][1] < y and poligono[i][1] >= y):
                        if poligono[i][0] + (y - poligono[i][1]) / (poligono[j][1] - poligono[i][1]) * (
                            poligono[j][0] - poligono[i][0]) < x:
                            salida = 1
                    j = i
                return salida

            if punto_en_poligono(punto_x, punto_y, poligono) == 2:
                pygame.display.set_caption("Prisionero Estas en unode los vertice")
            elif punto_en_poligono(punto_x, punto_y, poligono) == 1:
                pygame.display.set_caption("Prisionero")
            else:
                pygame.display.set_caption("Ciudadano")

        pygame.display.flip()
        reloj.tick(20)

# Cerramos el fichero.
infile.close()

pygame.quit()
