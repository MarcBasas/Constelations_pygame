# Constelations (Pygame + Pygbag)

Este proyecto es un juego interactivo de constelaciones hecho con Pygame y preparado para ser ejecutado en la web usando [pygbag](https://github.com/pygame-web/pygbag).

## Requisitos

- Python 3.8+
- [pygbag](https://github.com/pygame-web/pygbag)
- pygame

Puedes instalar las dependencias con:

```bash
pip install -r requirements.txt
```

## Ejecutar localmente

```bash
python main.py
```

## Construir para la web (pygbag)

1. Asegúrate de que `main.py` esté en la raíz del proyecto.
2. Ejecuta el siguiente comando en la terminal:

```bash
pygbag .
```

Esto iniciará un servidor en `http://localhost:8000` donde podrás probar el juego en el navegador.

## Subir a tu web/portfolio

- El contenido generado estará en la carpeta `build/web` después de correr `pygbag .`.
- Sube el contenido de `build/web` a tu servidor web o portfolio.

---

¡Listo para compartir tu juego en la web! 