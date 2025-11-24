import csv
from tabulate import tabulate
import argparse
import pytest

# Чтение данных из CSV-файла
def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

# Обработка данных и расчёт средней эффективности
def process_data(data):
    averages = {}
    for entry in data:
        pos = entry['position']
        perf = float(entry['performance'])
        averages.setdefault(pos, {'total': 0, 'count': 0})
        averages[pos]['total'] += perf
        averages[pos]['count'] += 1
    
    # Формируем отчёт
    report = [(pos, round(stats['total'] / stats['count'], 2)) for pos, stats in averages.items()]
    report.sort(key=lambda x: x[1], reverse=True)
    return report

# Вывод отчёта в консоль или сохранение в файл
def generate_report(report, output_file=None):
    pretty_report = tabulate(report, headers=["Position", "Average Performance"], tablefmt="grid")
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write(pretty_report)
    else:
        print(pretty_report)

# Основной блок выполнения
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Performance Report Generator")
    parser.add_argument("--files", nargs="+", required=True, help="Input CSV files.")
    parser.add_argument("--report", help="Output report filename.")
    args = parser.parse_args()

    # Чтение данных из всех файлов
    data = []
    for file in args.files:
        try:
            data.extend(read_csv(file))
        except Exception as err:
            print(f"Ошибка при чтении файла '{file}': {err}. Не найден.")
    
    # Обработка данных и формирование отчёта
    processed_data = process_data(data)
    generate_report(processed_data, args.report)

# === Тесты ===

# Тест для проверки чтения CSV-файла
def test_read_csv():
    data = read_csv('employees1.csv')
    assert len(data) > 0
    assert isinstance(data, list)
    assert isinstance(data[0], dict)

# Тест для проверки обработки данных
def test_process_data():
    sample_data = [
        {'position': 'Backend Developer', 'performance': '4.8'},
        {'position': 'Frontend Developer', 'performance': '4.6'},
        {'position': 'Backend Developer', 'performance': '4.9'},
        {'position': 'Frontend Developer', 'performance': '4.5'}
    ]
    expected_result = [
        ('Backend Developer', 4.85),
        ('Frontend Developer', 4.55)
    ]
    result = process_data(sample_data)
    assert sorted(result) == sorted(expected_result)

# Тест для проверки вывода отчёта
def test_generate_report(capsys):
    sample_report = [
        ('Backend Developer', 4.85),
        ('Frontend Developer', 4.55)
    ]
    generate_report(sample_report)
    captured = capsys.readouterr()
    assert 'Backend Developer' in captured.out
    assert '4.85' in captured.out
    assert 'Frontend Developer' in captured.out
    assert '4.55' in captured.out