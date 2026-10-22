import csv
import json
import os
import requests

COUNTRY = "ua"
INDICATOR = "SP.DYN.LE00.IN"
DATE_RANGE = "1991:2019"
JSON_FILENAME = "ukraine_life_expectancy_1991_2019.json"
CSV_FILENAME = "ukraine_life_expectancy_1991_2019.csv"

URL = (
    f"https://api.worldbank.org/v2/country/{COUNTRY}/"
    f"indicator/{INDICATOR}?date={DATE_RANGE}&format=json&per_page=500"
)


def get_data_from_api(api_url):
  try:
    print("надсилання запиту до API Світового банку...")
    response = requests.get(api_url, timeout=15)

    response.raise_for_status()

    data = response.json()

    if (
        not isinstance(data, list)
        or len(data) < 2
        or data[1] is None
        or len(data[1]) == 0
    ):
      raise ValueError(
          "API повернув порожню структуру даних або відповідь не містить"
          " необхідних записів."
      )

    print(" Дані успішно отримано та перевірено.")
    return data

  except requests.exceptions.HTTPError as http_err:
    print(f" Помилка HTTP: {http_err}")
  except requests.exceptions.ConnectionError:
    print(
        " Помилка підключення до мережі. Перевірте підключення до Інтернету."
    )
  except requests.exceptions.Timeout:
    print(" Час очікування запиту (Timeout) вичерпано.")
  except ValueError as val_err:
    print(f" Помилка валідації даних: {val_err}")
  except Exception as err:
    print(f" Виникла непередбачена помилка під час запиту: {err}")

  return None

def save_to_json(data, filename):

  try:
    with open(filename, "w", encoding="utf-8") as file:
      json.dump(data, file, ensure_ascii=False, indent=4)
    print(f" JSON-файл успішно створено: {filename}")
  except (IOError, OSError) as io_err:
    print(f" Помилка введення-виведення при збереженні JSON: {io_err}")
  except Exception as e:
    print(f" Помилка збереження JSON: {e}")

def process_and_save_csv(data, filename):
  try:
    if not data or len(data) < 2 or not data[1]:
      print("Неможливо сформувати CSV: відсутні дані для обробки.")
      return

    csv_rows = []
    for item in data[1]:
      country_name = item.get("country", {}).get("value", "N/A")
      year = item.get("date", "N/A")
      value = item.get("value")

      if value is not None:
        csv_rows.append([country_name, year, value])

    if not csv_rows:
      print(" Попередження: Немає дійсних числових даних для запису в CSV.")
      return

    with open(filename, "w", newline="", encoding="utf-8") as file:
      writer = csv.writer(file)
      writer.writerow(
          ["Country Name", "Year", "Life expectancy at birth, total (years)"]
      )
      writer.writerows(csv_rows)

    print(f" CSV-файл успішно створено: {filename}")

  except (IOError, OSError) as io_err:
    print(f" Помилка введення-виведення при збереженні CSV: {io_err}")
  except Exception as e:
    print(f" Помилка під час обробки даних для CSV: {e}")


def display_results(json_filename, csv_filename):
  print("\n")
  print("Перевірка та виведення змісту файлу")

  if os.path.exists(json_filename):
    if os.path.getsize(json_filename) == 0:
      print(f" Попередження: Файл '{json_filename}' є порожнім (розмір 0 байт).")
    else:
      print(
          f"\nЗміст JSON-файлу ({json_filename}) [перші 3 записи масиву даних]:"
      )
      try:
        with open(json_filename, "r", encoding="utf-8") as file:
          json_content = json.load(file)
          print(f"Метаінформація запиту: {json_content[0]}")
          for item in json_content[1][:3]:
            print(json.dumps(item, ensure_ascii=False, indent=4))
      except json.JSONDecodeError:
        print(f" Помилка: Файл '{json_filename}' містить некоректний JSON.")
      except Exception as e:
        print(f" Помилка читання JSON: {e}")
  else:
    print(f" Файл '{json_filename}' не знайдено.")

  print("\n")

  if os.path.exists(csv_filename):
    if os.path.getsize(csv_filename) == 0:
      print(f" Попередження: Файл '{csv_filename}' є порожнім (розмір 0 байт).")
    else:
      print(f"Зміст CSV-файлу ({csv_filename}):")
      try:
        with open(csv_filename, "r", encoding="utf-8") as file:
          reader = csv.reader(file)
          rows = list(reader)
          if not rows:
            print(f" Файл '{csv_filename}' не містить рядків.")
          else:
            for row in rows[:10]:
              print(", ".join(row))
            if len(rows) > 10:
              print(f"... (всього рядків у файлі: {len(rows)})")
      except Exception as e:
        print(f" Помилка читання CSV: {e}")
  else:
    print(f" Файл '{csv_filename}' не знайдено.")


def main():
  print(" Показник: Очікувана тривалість життя для України (1991–2019)\n")

  raw_data = get_data_from_api(URL)

  if raw_data:
    save_to_json(raw_data, JSON_FILENAME)

    process_and_save_csv(raw_data, CSV_FILENAME)

    display_results(JSON_FILENAME, CSV_FILENAME)
  else:
    print(" Програму завершено достроково через помилку отримання даних.")


if __name__ == "__main__":
  main()