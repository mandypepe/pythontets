import pygame, sys


class Text:
    def __init__(self, FontName=None, FontSize=30):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize

    def render(self, surface, text, color, pos):
        x, y = pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i, 1, color), (x, y))
            y += self.size


# definiendo colores
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
CAFE = (90, 50, 15)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


infile = open('texto', 'r')

for line in infile:
    seg = []
    punto = Point(0, 0)
    line = line.replace(" ", ",").replace("|", ",").split(",")

    i = 0
    while i < len(line):
        i = i + 2

    i = 0

    pygame.init()
    dimx = 1000
    dimy = 600
    mul = 100
    may = 0
    for cc in line:
        cc = int(cc)
        if (cc > may):
            may = cc

    mul = dimy / may

    py = int(line.pop())
    px = int(line.pop())
    punto = Point(px, py)

    dimensiones = (dimx, dimy)
    pantalla = pygame.display.set_mode(dimensiones)
    pantalla.fill(BLANCO)
    terminar = False
    reloj = pygame.time.Clock()
    text = Text()

    while not terminar:
        for Evento in pygame.event.get():
            if Evento.type == pygame.QUIT:
                terminar = True

        while i < len(line):
            seg.append(Point(int(line[i]), int(line[i + 1])))
            i = i + 2

        bb = seg[len(seg) - 1]
        tpoint = []

        ii = 0

        for aa in seg:
            if (ii < len(seg) - 1):
                pygame.draw.line(pantalla, ROJO, [seg[ii].x * mul, dimy - seg[ii].y * mul],
                                 [seg[ii + 1].x * mul, dimy - seg[ii + 1].y * mul], 3)
                text.render(pantalla, "(" + str(seg[ii].x) + "," + str(seg[ii].y) + ")", NEGRO,
                            (seg[ii].x * mul, dimy - seg[ii].y * mul))
            else:
                pygame.draw.line(pantalla, ROJO, [seg[ii].x * mul, dimy - seg[ii].y * mul],
                                 [seg[0].x * mul, dimy - seg[0].y * mul], 3)
                text.render(pantalla, "(" + str(seg[ii].x) + "," + str(seg[ii].y) + ")", NEGRO,
                            (seg[ii].x * mul, dimy - seg[ii].y * mul))
            text.render(pantalla, "(" + str(punto.x) + "," + str(punto.y) + ")", NEGRO,
                        (punto.x * mul, dimy - punto.y * mul))
            ii = ii + 1

            tama = 0
            while tama < dimx / mul:
                pygame.draw.line(pantalla, CAFE, [tama * mul, 0], [tama * mul, dimy], 1)
                pygame.draw.line(pantalla, CAFE, [0, tama * mul], [dimx, tama * mul], 1)
                tama = tama + 1

            pygame.draw.line(pantalla, AZUL, [punto.x * mul, dimy - punto.y * mul], [punto.x * mul, dimy - 0 * mul], 3)
            pygame.draw.line(pantalla, AZUL, [punto.x * mul, dimy - punto.y * mul], [0 * mul, dimy - punto.y * mul], 3)

            pygame.draw.line(pantalla, AZUL, [punto.x * mul, dimy - punto.y * mul],
                             [punto.x * mul, dimy - may * 2 * mul], 3)
            pygame.draw.line(pantalla, AZUL, [punto.x * mul, dimy - punto.y * mul], [may * mul, dimy - punto.y * mul],
                             3)
            bb = aa
        ciudadano = True
        for tp in [Point(punto.x, 0), Point(punto.x, 100), Point(0, punto.y), Point(100, punto.y)]:
            contador = 0
            for aa in seg:
                if (intersect(bb, aa, punto, tp)):
                    contador = contador + 1
                bb = aa
            print(contador)
            if contador % 2 != 0:
                ciudadano = False
        if ciudadano:
            pygame.display.set_caption("Ciudadano")

        else:
            pygame.display.set_caption("Prisionero")

        pygame.display.flip()
        reloj.tick(20)

infile.close()
