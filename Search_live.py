import csv
import os

INPUT_CSV = "ukraine_life_expectancy_1991_2019.csv"
OUTPUT_CSV = "min_max_life_expectancy_results.csv"


def find_extreme_values(input_filename, output_filename):
  print(f" Відкриття та аналіз файлу '{input_filename}'...")

  rows_data = []

  try:
    with open(input_filename, "r", encoding="utf-8") as csvfile:
      reader = csv.DictReader(csvfile)

      for row in reader:
        if "Year" in row and "Life expectancy at birth, total (years)" in row:
          year = row["Year"]
          country = row["Country Name"]
          try:
            value = float(
                row["Life expectancy at birth, total (years)"]
            )
            rows_data.append({"Country": country, "Year": year, "Value": value})
          except ValueError:
            continue

    if not rows_data:
      print(f" Попередження: Файл '{input_filename}' не містить дійсних даних.")
      return

  except FileNotFoundError:
    print(f" Помилка: Файл '{input_filename}' не знайдено!")
    return
  except IOError as io_err:
    print(f" Помилка введення-виведення при читанні файлу: {io_err}")
    return
  except Exception as e:
    print(f" Непередбачена помилка під час читання: {e}")
    return

  try:
    min_record = min(rows_data, key=lambda x: x["Value"])
    max_record = max(rows_data, key=lambda x: x["Value"])

    print("\n")
    print(" Результати пошуку:")
    print(
        f" Найнижча тривалість життя: {min_record['Value']} років"
        f" (рік: {min_record['Year']})"
    )
    print(
        f" Найвища тривалість життя: {max_record['Value']} років"
        f" (рік: {max_record['Year']})"
    )
    print("-" * 50)

  except Exception as e:
    print(f" Помилка під час обчислення значень: {e}")
    return

  try:
    with open(output_filename, "w", newline="", encoding="utf-8") as csvfile2:
      writer = csv.writer(csvfile2, delimiter=";")

      writer.writerow(
          ["Indicator Type", "Country Name", "Year", "Life Expectancy (Years)"]
      )

      writer.writerow([
          "Lowest Value",
          min_record["Country"],
          min_record["Year"],
          min_record["Value"],
      ])
      writer.writerow([
          "Highest Value",
          max_record["Country"],
          max_record["Year"],
          max_record["Value"],
      ])

    print(f" Результати успішно збережено у новий файл: '{output_filename}'")

  except IOError as io_err:
    print(f" Помилка введення-виведення при записі у файл '{output_filename}': {io_err}")
  except Exception as e:
    print(f" Помилка збереження результатів: {e}")


if __name__ == "__main__":
  find_extreme_values(INPUT_CSV, OUTPUT_CSV)