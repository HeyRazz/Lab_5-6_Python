import csv
import json
import os

CSV_FILENAME = "ukraine_life_expectancy_1991_2019.csv"
JSON_FILENAME = "life_expectancy_data.json"
FILTERED_JSON_FILENAME = "filtered_life_expectancy.json"


def convert_csv_to_json(csv_file, json_file):
  data_list = []
  try:
    if not os.path.exists(csv_file):
      print(f"Попередження: Файл '{csv_file}' не знайдено.")
      return False

    with open(csv_file, "r", encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
        data_list.append(row)

    with open(json_file, "w", encoding="utf-8") as f:
      json.dump(data_list, f, ensure_ascii=False, indent=4)

    print(
        f"Дані успішно перетворено з CSV у JSON-файл: '{json_file}' (записів:"
        f" {len(data_list)})"
    )
    return True
  except Exception as e:
    print(f"Помилка конвертації: {e}")
    return False


def load_json_data(filename):
  """Зчитує дані з JSON-файлу з обробкою винятків."""
  try:
    if not os.path.exists(filename):
      print(f"Файл '{filename}' не знайдено.")
      return []
    with open(filename, "r", encoding="utf-8") as file:
      return json.load(file)
  except json.JSONDecodeError:
    print("Помилка: файл містить некоректні JSON-дані.")
    return []
  except Exception as e:
    print(f"Помилка читання файлу: {e}")
    return []


def main():
  convert_csv_to_json(CSV_FILENAME, JSON_FILENAME)

  while True:
    print("\n")
    print("Оберіть опцію меню:")
    print(" 1 - Переглянути всі дані з JSON-файлу")
    print(" 2 - Додати новий запис (рік та показник)")
    print(
        " 3 - Здійснити пошук (наприклад, знайти роки, де показник вищий за"
        " задане значення) і зберегти у новий JSON"
    )
    print(" 4 - Вихід")

    try:
      x = int(input("Оберіть опцію (ведіть номер): "))
    except ValueError:
      print("Помилка: потрібно ввести число від 1 до 4.")
      continue

    if x == 1:
      data = load_json_data(JSON_FILENAME)
      if data:
        print(
            "\nЗміст JSON-файлу (показано перші 10 записів)"
        )
        for item in data[:10]:
          print(
              f"Країна: {item.get('Country Name')}, Рік:"
              f" {item.get('Year')}, Значення:"
              f" {item.get('Life expectancy at birth, total (years)')}"
          )
        if len(data) > 10:
          print(f"... всього записів у файлі: {len(data)}")

    elif x == 2:
      print("\nДодавання нового запису")
      country = input("Введіть назву країни (наприклад, Ukraine): ")
      year = input("Введіть рік (наприклад, 2020): ")
      value = input("Введіть значення показника тривалості життя: ")

      current_data = load_json_data(JSON_FILENAME)
      new_record = {
          "Country Name": country,
          "Year": year,
          "Life expectancy at birth, total (years)": value,
      }
      current_data.append(new_record)

      try:
        with open(JSON_FILENAME, "w", encoding="utf-8") as file:
          json.dump(current_data, file, ensure_ascii=False, indent=4)
        print("Запис успішно додано до JSON-файлу!")
      except Exception as e:
        print(f"Помилка запису: {e}")

    elif x == 3:
      data = load_json_data(JSON_FILENAME)
      if not data:
        print("Файл даних порожній.")
        continue

      try:
        threshold = float(
            input(
                "Введіть порогове значення тривалості життя (наприклад, 70.0): "
            )
        )
      except ValueError:
        print("Помилка: введіть числове значення.")
        continue

      filtered_result = []
      for row in data:
        val_str = row.get("Life expectancy at birth, total (years)")
        try:
          if val_str and float(val_str) > threshold:
            filtered_result.append(row)
        except ValueError:
          continue

      if filtered_result:
        print(f"\nЗнайдено записів із показником > {threshold}:")
        for res in filtered_result:
          print(
              f"Рік: {res.get('Year')} — Значення:"
              f" {res.get('Life expectancy at birth, total (years)')}"
          )

        try:
          with open(FILTERED_JSON_FILENAME, "w", encoding="utf-8") as f_out:
            json.dump(filtered_result, f_out, ensure_ascii=False, indent=4)
          print(
              f"Результати пошуку успішно збережено у новий файл:"
              f" '{FILTERED_JSON_FILENAME}'."
          )
        except Exception as e:
          print(f"Помилка збереження файлу результатів: {e}")
      else:
        print("За заданим критерієм даних не знайдено.")

    elif x == 4:
      print("Вихід з програми. До побачення!")
      break
    else:
      print("Невірний вибір. Будь ласка, оберіть від 1 до 4.")


if __name__ == "__main__":
  main()