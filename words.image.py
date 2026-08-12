import sys
from pathlib import Path
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk

def choose_image() -> Path or None:
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(filetypes=[("PNG Image", ".png *.jpg")])
    root.destroy()
    return Path(filename)

def make_ascii_art(image: Image.Image, width: int) -> str:
    characters = "@#8&o:*. "

    image = image.convert("L")

    height = max(
        1,
        int(width * image.height / image.width * 0.5)
    )

    image = image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    result = []

    for y in range(image.height):
        line = ""

        for x in range(image.width):
            brightness = image.getpixel((x, y))

            index = int(
                brightness / 255 * (len(characters) - 1)
            )

            line += characters[index]

        result.append(line)

    return "\n".join(result)

def ask_number(question: str, default: int) -> int:
    answer = input(f"{question} [{default}]: ").strip()
    return int(answer) if answer else default


def main() -> None:
    # Путь можно передать аргументом или выбрать в окне.
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else choose_image()
    if source is None:
        print("Изображение не выбрано.")
        return
    if not source.is_file():
        print(f"Файл не найден: {source}")
        return

    try:
        pixel_width = ask_number("Ширина в пикселях", 64)
        colors = ask_number("Количество цветов", 16)

        with Image.open(source) as image:
            pixel_art = makepixelart(image, pixel_width, colors)

        # Увеличиваем результат для просмотра, сохраняя резкие границы.
        scale = max(1, 800 // pixel_art.width)
        preview = pixel_art.resize(
            (pixel_art.width * scale, pixel_art.height * scale),
            Image.Resampling.NEAREST,
        )

        output = source.with_name(f"{source.stem}_pixel_art.png")
        preview.save(output)
        preview.show()
        print(f"Готово! Результат сохранён здесь:\n{output}")
    except (ValueError, OSError) as error:
        print(f"Ошибка: {error}")



main()

