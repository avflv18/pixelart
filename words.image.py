

import sys
from pathlib import Path
from tkinter import Tk, filedialog

from PIL import Image


ASCII_CHARS = "676767 "


def choose_image() -> Path | None:
    """Показать стандартное окно выбора изображения."""
    window = Tk()
    window.withdraw()

    filename = filedialog.askopenfilename(
        title="Выберите изображение",
        filetypes=[
            ("Изображения", "*.png *.jpg *.jpeg *.bmp *.webp"),
            ("Все файлы", "*.*"),
        ],
    )

    window.destroy()

    return Path(filename) if filename else None


def make_ascii_art(image: Image.Image, width: int) -> str:
    """Преобразовать изображение в ASCII-арт."""

    if width < 1:
        raise ValueError("Ширина должна быть больше нуля")

    # Переводим изображение в оттенки серого.
    image = image.convert("L")

    # Вычисляем высоту с сохранением пропорций.
    # 0.5 нужно потому, что символы в консоли обычно выше, чем шире.
    height = max(
        1,
        round(image.height / image.width * width * 0.5)
    )

    # Уменьшаем изображение.
    image = image.resize((width, height))

    # Получаем яркость каждого пикселя.
    pixels = list(image.getdata())

    # Заменяем каждый пиксель ASCII-символом.
    chars = []

    for pixel in pixels:
        index = pixel * (len(ASCII_CHARS) - 1) // 255
        chars.append(ASCII_CHARS[index])

    # Разбиваем символы на строки.
    lines = []

    for i in range(0, len(chars), width):
        line = "".join(chars[i:i + width])
        lines.append(line)

    return "\n".join(lines)


def ask_number(question: str, default: int) -> int:
    """Запросить число у пользователя."""
    answer = input(f"{question} [{default}]: ").strip()

    if answer:
        return int(answer)

    return default


def main() -> None:
    # Если путь к изображению передан через консоль —
    # используем его. Иначе открываем окно выбора файла.
    if len(sys.argv) > 1:
        source = Path(sys.argv[1])
    else:
        source = choose_image()

    if source is None:
        print("Изображение не выбрано.")
        return

    if not source.is_file():
        print(f"Файл не найден: {source}")
        return

    try:
        # Чем больше ширина, тем детальнее ASCII-арт.
        width = ask_number("Ширина ASCII-арта", 100)

        with Image.open(source) as image:
            ascii_art = make_ascii_art(image, width)

        # Создаём txt-файл рядом с исходным изображением.
        output = source.with_name(
            f"{source.stem}_ascii.txt"
        )

        output.write_text(
            ascii_art,
            encoding="utf-8"
        )

        # Показываем ASCII-арт прямо в консоли.
        print()
        print(ascii_art)
        print()
        print(f"Готово!")
        print(f"Результат сохранён здесь:")
        print(output)

    except ValueError as error:
        print(f"Ошибка: {error}")

    except OSError as error:
        print(f"Ошибка при работе с изображением: {error}")


if __name__ == "__main__":
    main()