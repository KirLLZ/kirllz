import os
import re
from collections import defaultdict

# Функция для получения всех музыкальных файлов в директории и вложенных папках
def get_music_files(directory):
    music_files = []
    try:
        for root, _, files in os.walk(directory):  # os.walk автоматически обходит вложенные папки
            for file in files:
                if file.lower().endswith(('.mp3', '.flac', '.wav', '.m4a')):  # можно добавить другие форматы
                    music_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"Ошибка при сканировании директории: {e}")
    return music_files

# Функция для нормализации названий файлов
def normalize_filename(filename):
    # Заменяем подчеркивания на пробелы и приводим к нижнему регистру
    filename = filename.lower()
    filename = filename.replace('_', ' ')
    
    # Убираем слово "копия" из названия, если оно есть
    filename = re.sub(r'\bкопия\b', '', filename)
    
    return filename.strip()

# Функция для подтверждения дубликата
def confirm_duplicate(files):
    print("Найдено дублирующие файлы:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")
    response = input("Действительно ли это дубль (y/n)? ").lower()
    return response == 'y'

# Функция для удаления файлов с обработкой ошибок
def delete_files(files):
    for idx, file in enumerate(files, 1):
        try:
            response = input(f"Вы хотите удалить файл {file}? (y/n): ").lower()
            if response == 'y':
                os.remove(file)
                print(f"Файл {file} удален.")
            else:
                print(f"Файл {file} не был удален.")
        except PermissionError:
            print(f"Ошибка: У вас нет прав для удаления файла {file}.")
        except FileNotFoundError:
            print(f"Ошибка: Файл {file} не найден.")
        except Exception as e:
            print(f"Ошибка при удалении файла {file}: {e}")

# Функция для выявления дублей
def find_duplicates(directory):
    music_files = get_music_files(directory)
    
    # Словарь для хранения информации о файлах по нормализованным названиям и размерам
    file_info = defaultdict(list)
    
    for file in music_files:
        filename = os.path.basename(file)
        normalized_filename = normalize_filename(filename)
        file_size = os.path.getsize(file)
        
        file_info[(normalized_filename, file_size)].append(file)
    
    # Выводим все найденные дубли
    duplicates = {key: value for key, value in file_info.items() if len(value) > 1}
    
    if duplicates:
        print("Найдено дубли:")
        for key, files in duplicates.items():
            print(f"\nНазвание: {key[0]}, Размер: {key[1]} байт")
            if confirm_duplicate(files):
                print("Это подтвержденный дубль.")
                delete_files(files)
            else:
                print("Это не дубль.")
    else:
        print("Дубли не найдены.")

# Пример использования
if __name__ == "__main__":
    directory = input("Введите путь к директории с музыкой: ")
    find_duplicates(directory)
