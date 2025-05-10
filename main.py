import pygame
import random
import time
import math
import asyncio  # Para compatibilidad con pygbag

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 1024
ALTO = 576
ALTO_PANEL = int(ALTO * 0.1)  # 10% del alto para el panel
ALTO_JUEGO = ALTO  # Todo el alto disponible para el juego

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Constelations")

# Colores
GRIS_OSCURO = (40, 40, 40)
GRIS_PANEL = (45, 45, 45)
BEIGE = (245, 245, 220)
TRAPECIO_COLOR = (65, 65, 65)

# Velocidad fija para todos los puntos
VELOCIDAD = 0.5
VELOCIDAD_MIN = 0.5
VELOCIDAD_MAX = 10.0

# Configuración de puntos
NUMERO_PUNTOS = 40
NUMERO_PUNTOS_MIN = 10
NUMERO_PUNTOS_MAX = 100

# Configuración de las líneas
DISTANCIA_MAXIMA = 100  # Distancia máxima para dibujar una línea
DISTANCIA_MIN = 50
DISTANCIA_MAX = 300
OPACIDAD_LINEA = 50    # Opacidad de las líneas (0-255)

# Estado del panel
panel_visible = True
# Dimensiones del trapecio
TRAPECIO_BASE_MAYOR = 40
TRAPECIO_BASE_MENOR = 20
TRAPECIO_ALTURA = 10

# Configuración del slider
SLIDER_ANCHO = 150
SLIDER_ALTO = 20
SLIDER_MARGEN = 20
SLIDER_Y = ALTO - ALTO_PANEL + (ALTO_PANEL // 2) - (SLIDER_ALTO // 2)  # Centrado verticalmente en el panel

# Posiciones horizontales basadas en porcentajes del ancho
POSICION_SLIDER_1 = int(ANCHO * 0.22)  # 20% del ancho
POSICION_SLIDER_2 = int(ANCHO * 0.53)  # 50% del ancho
POSICION_SLIDER_3 = int(ANCHO * 0.86)  # 80% del ancho

class Slider:
    def __init__(self, x, y, ancho, alto, min_val, max_val, valor_inicial, texto):
        self.x = x - (ancho // 2)  # Centrar el slider en la posición x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.min_val = min_val
        self.max_val = max_val
        self.valor = valor_inicial
        self.texto = texto
        self.arrastrando = False
        self.rect = pygame.Rect(self.x, y, ancho, alto)
        self.rect_control = pygame.Rect(self.x, y, 10, alto)

    def actualizar_valor(self, pos_x):
        pos_relativa = max(0, min(pos_x - self.x, self.ancho))
        self.valor = self.min_val + (pos_relativa / self.ancho) * (self.max_val - self.min_val)
        self.rect_control.x = self.x + pos_relativa - 5

    def dibujar(self, pantalla):
        fuente = pygame.font.SysFont(None, 24)
        texto = fuente.render(self.texto, True, BEIGE)
        texto_rect = texto.get_rect()
        texto_rect.x = self.x - texto_rect.width - 10
        texto_rect.centery = self.y + self.alto//2
        pantalla.blit(texto, texto_rect)

        pygame.draw.rect(pantalla, GRIS_OSCURO, self.rect)
        pygame.draw.rect(pantalla, BEIGE, self.rect_control)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_control.collidepoint(evento.pos):
                self.arrastrando = True
        elif evento.type == pygame.MOUSEBUTTONUP:
            self.arrastrando = False
        elif evento.type == pygame.MOUSEMOTION and self.arrastrando:
            self.actualizar_valor(evento.pos[0])

class Punto:
    def __init__(self):
        self.x = random.randint(0, ANCHO)
        self.y = random.randint(0, ALTO)
        angulo = random.uniform(0, 2*math.pi)
        self.velocidad_x = VELOCIDAD * math.cos(angulo)
        self.velocidad_y = VELOCIDAD * math.sin(angulo)
        self.radio = 3
        self.tiempo_creacion = time.time()
        self.tiempo_vida = random.uniform(4, 10)
        self.tiempo_aparicion = 1.0
        self.tiempo_desaparicion = 1.0
        self.superficie = pygame.Surface((self.radio * 2, self.radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.superficie, BEIGE, (self.radio, self.radio), self.radio)

    def actualizar_velocidad(self, nueva_velocidad):
        proporcion = math.sqrt(self.velocidad_x**2 + self.velocidad_y**2) / VELOCIDAD
        self.velocidad_x = nueva_velocidad * (self.velocidad_x / (proporcion * VELOCIDAD))
        self.velocidad_y = nueva_velocidad * (self.velocidad_y / (proporcion * VELOCIDAD))

    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y

    def esta_fuera(self):
        return (self.x < -self.radio or self.x > ANCHO + self.radio or self.y < -self.radio or self.y > ALTO)

    def debe_destruir(self):
        return time.time() - self.tiempo_creacion > self.tiempo_vida

    def get_opacidad(self):
        tiempo_transcurrido = time.time() - self.tiempo_creacion
        if tiempo_transcurrido < self.tiempo_aparicion:
            return int((tiempo_transcurrido / self.tiempo_aparicion) * 255)
        tiempo_restante = self.tiempo_vida - tiempo_transcurrido
        if tiempo_restante < self.tiempo_desaparicion:
            return int((tiempo_restante / self.tiempo_desaparicion) * 255)
        return 255

    def dibujar(self, pantalla):
        superficie_actual = self.superficie.copy()
        superficie_actual.set_alpha(self.get_opacidad())
        pantalla.blit(superficie_actual, (int(self.x - self.radio), int(self.y - self.radio)))

    def distancia_a(self, otro_punto):
        return math.hypot(self.x - otro_punto.x, self.y - otro_punto.y)


def dibujar_lineas(pantalla, puntos):
    superficie_lineas = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    for i, punto1 in enumerate(puntos):
        for punto2 in puntos[i+1:]:
            distancia = punto1.distancia_a(punto2)
            if distancia < DISTANCIA_MAXIMA:
                opacidad = int(OPACIDAD_LINEA * (1 - distancia/DISTANCIA_MAXIMA))
                pygame.draw.line(superficie_lineas, (*BEIGE, opacidad), (int(punto1.x), int(punto1.y)), (int(punto2.x), int(punto2.y)), 1)
    pantalla.blit(superficie_lineas, (0, 0))


def dibujar_panel_control(pantalla):
    y_panel = ALTO - ALTO_PANEL if panel_visible else ALTO
    if panel_visible:
        pygame.draw.rect(pantalla, GRIS_PANEL, (0, y_panel, ANCHO, ALTO_PANEL))
        for slider in sliders:
            slider.dibujar(pantalla)
    x_centro = ANCHO // 2
    y_trapecio = y_panel
    puntos_trapecio = [
        (x_centro + TRAPECIO_BASE_MENOR//2, y_trapecio - TRAPECIO_ALTURA),
        (x_centro - TRAPECIO_BASE_MENOR//2, y_trapecio - TRAPECIO_ALTURA),
        (x_centro - TRAPECIO_BASE_MAYOR//2, y_trapecio),
        (x_centro + TRAPECIO_BASE_MAYOR//2, y_trapecio)
    ]
    pygame.draw.polygon(pantalla, BEIGE, puntos_trapecio)
    return pygame.Rect(x_centro - TRAPECIO_BASE_MAYOR//2, y_trapecio - TRAPECIO_ALTURA, TRAPECIO_BASE_MAYOR, TRAPECIO_ALTURA)

# Sliders
sliders = [
    Slider(POSICION_SLIDER_1, SLIDER_Y, SLIDER_ANCHO, SLIDER_ALTO, VELOCIDAD_MIN, VELOCIDAD_MAX, VELOCIDAD, "SPEED"),
    Slider(POSICION_SLIDER_2, SLIDER_Y, SLIDER_ANCHO, SLIDER_ALTO, NUMERO_PUNTOS_MIN, NUMERO_PUNTOS_MAX, NUMERO_PUNTOS, "POINTS"),
    Slider(POSICION_SLIDER_3, SLIDER_Y, SLIDER_ANCHO, SLIDER_ALTO, DISTANCIA_MIN, DISTANCIA_MAX, DISTANCIA_MAXIMA, "DISTANCE")
]

async def main():
    global VELOCIDAD, NUMERO_PUNTOS, DISTANCIA_MAXIMA, panel_visible
    puntos = []
    corriendo = True
    reloj = pygame.time.Clock()
    boton_rect = None

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect and boton_rect.collidepoint(evento.pos):
                    panel_visible = not panel_visible
                if panel_visible:
                    for slider in sliders:
                        slider.manejar_evento(evento)
            elif evento.type == pygame.MOUSEBUTTONUP:
                if panel_visible:
                    for slider in sliders:
                        slider.manejar_evento(evento)
            elif evento.type == pygame.MOUSEMOTION and panel_visible:
                for slider in sliders:
                    slider.manejar_evento(evento)

        # Actualizar parámetros
        if VELOCIDAD != sliders[0].valor:
            VELOCIDAD = sliders[0].valor
            for p in puntos:
                p.actualizar_velocidad(VELOCIDAD)
        if NUMERO_PUNTOS != int(sliders[1].valor):
            NUMERO_PUNTOS = int(sliders[1].valor)
            while len(puntos) < NUMERO_PUNTOS:
                puntos.append(Punto())
            while len(puntos) > NUMERO_PUNTOS:
                puntos.pop(0)
        if DISTANCIA_MAXIMA != sliders[2].valor:
            DISTANCIA_MAXIMA = sliders[2].valor

        # Movimiento y ciclo de vida
        eliminar = []
        for p in puntos:
            p.mover()
            if p.debe_destruir() or p.esta_fuera():
                eliminar.append(p)
        for p in eliminar:
            if p in puntos:
                puntos.remove(p)
        if len(puntos) < NUMERO_PUNTOS:
            puntos.append(Punto())

        # Dibujado
        pantalla.fill(GRIS_OSCURO)
        dibujar_lineas(pantalla, puntos)
        for p in puntos:
            p.dibujar(pantalla)
        boton_rect = dibujar_panel_control(pantalla)

        pygame.display.flip()
        reloj.tick(60)
        await asyncio.sleep(0)  # Ceder control al runtime WebAssembly

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
