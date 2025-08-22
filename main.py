import requests
from bs4 import BeautifulSoup
import openpyxl
import time


def get_item_prices(item_code, server="europe"):
    """
    Отримує ціни на предмет з сайту albiononlinetools.com і повертає їх у вигляді словника.
    Автоматично обробляє предмети із зачаруванням (LEVEL).
    """
    # --- НОВА ЛОГІКА ДЛЯ ФОРМУВАННЯ URL ---
    # Перевіряємо, чи це предмет з рівнем зачарування (enchantment)
    if "_LEVEL" in item_code and item_code[-1].isdigit():
        enchantment_level = item_code[-1]
        url_param = f"{item_code}@{enchantment_level}"
    else:
        # Для звичайних предметів нічого не змінюємо
        url_param = item_code

    url = f"https://albiononlinetools.com/economy/item.php?itemPrice={url_param}&server={server}"
    # --- КІНЕЦЬ НОВОЇ ЛОГІКИ ---

    price_data = {}

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"  -> Помилка при запиті для {item_code}: Статус {response.status_code}")
            return {}

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find(class_="table-responsive")

        if not table or not table.find("tbody"):
            print(f"  -> Не знайдено таблицю з цінами для {item_code}")
            return {}

        rows = table.find("tbody").find_all("tr")
        for row in rows:
            cols = [c.get_text(strip=True) for c in row.find_all("td")]
            if len(cols) > 1:
                city_name = cols[1].split(" (")[0]
                sell_price = cols[2]
                price_data[city_name] = sell_price

    except requests.RequestException as e:
        print(f"  -> Помилка мережі при обробці {item_code}: {e}")
        return {}

    return price_data


def update_excel_prices(file_path):
    """
    Основна функція для оновлення Excel-файлу.
    """
    try:
        workbook = openpyxl.load_workbook(file_path)
    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдено. Перевірте назву та шлях до файлу.")
        return

    sheet = workbook.active

    header = [cell.value for cell in sheet[1]]

    # Створюємо словник міст, ігноруючи стовпець 'Item'
    city_columns = {city_name: col_idx + 1 for col_idx, city_name in enumerate(header) if
                    city_name and city_name != 'Item'}

    for row_index in range(2, sheet.max_row + 1):
        item_code = sheet.cell(row=row_index, column=1).value

        if not item_code:
            continue

        print(f"Обробка: {item_code}...")
        prices = get_item_prices(item_code)

        for city, col_idx in city_columns.items():
            price_to_write = prices.get(city, '-')
            sheet.cell(row=row_index, column=col_idx).value = price_to_write


    try:
        workbook.save(file_path)
        print(f"\n✅ Оновлення завершено! Файл '{file_path}' збережено.")
    except PermissionError:
        print(
            f"\n❌ Помилка: Не вдалося зберегти файл '{file_path}'. Можливо, він відкритий в Excel. Закрийте його та спробуйте знову.")


# --- ГОЛОВНА ЧАСТИНА ---
if __name__ == "__main__":
    # ВАЖЛИВО: Вкажіть тут правильну назву вашого Excel-файлу
    excel_file_name = "test.xlsx"
    update_excel_prices(excel_file_name)