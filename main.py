
import argparse
import csv
import sys
from tabulate import tabulate


def parse_condition(condition):
    """ Парсим строку с условием """
    operators = ['>=', '<=', '>', '<', '=']

    for op in operators:
        if op in condition:
            parts = condition.split(op, 1)
            if len(parts) == 2:
                column, value = parts
                return column.strip(), op, value.strip()

    raise ValueError(f"Invalid condition format: {condition}")


def apply_filter(rows, headers, condition):
    """ Фильтр данных по условию """
    column, operator, value = parse_condition(condition)

    if column not in headers:
        raise ValueError(f"Column '{column}' not found in CSV")

    col_index = headers.index(column)
    filtered_rows = []

    for row in rows:
        cell_value = row[col_index]

        try:
            cell_num = float(cell_value)
            value_num = float(value)

            if operator == '>' and cell_num > value_num:
                filtered_rows.append(row)
            elif operator == '<' and cell_num < value_num:
                filtered_rows.append(row)
            elif operator == '>=' and cell_num >= value_num:
                filtered_rows.append(row)
            elif operator == '<=' and cell_num <= value_num:
                filtered_rows.append(row)
            elif operator == '=' and cell_num == value_num:
                filtered_rows.append(row)

        except ValueError:

            if operator == '=' and cell_value == value:
                filtered_rows.append(row)
            elif operator != '=':
                continue

    return filtered_rows


def apply_aggregation(rows, headers, condition):
    """ Аггрегация данных по условию """
    parts = condition.split('=', 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid aggregation format: {condition}")

    column, func = parts[0].strip(), parts[1].strip()

    if column not in headers:
        raise ValueError(f"Column '{column}' not found in CSV")

    col_index = headers.index(column)
    values = []

    for row in rows:
        try:
            values.append(float(row[col_index]))
        except ValueError:
            raise ValueError(f"Column '{column}' contains non-numeric values")

    if not values:
        return []

    if func == 'avg':
        result = sum(values) / len(values)
    elif func == 'min':
        result = min(values)
    elif func == 'max':
        result = max(values)
    else:
        raise ValueError(f"Unknown aggregation function: {func}")

    return [[column, func, result]]


def main():
    parser = argparse.ArgumentParser(description='Process CSV files with filtering and aggregation')
    parser.add_argument('--file', help='Path to CSV file')
    parser.add_argument('--where', help='Filter condition (e.g., "price>500")')
    parser.add_argument('--aggregate', help='Aggregation condition (e.g., "price=avg")')

    args = parser.parse_args()

    try:

        with open(args.file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            rows = list(reader)

        if args.where:
            rows = apply_filter(rows, headers, args.where)

        if args.aggregate:
            result_rows = apply_aggregation(rows, headers, args.aggregate)
            result_headers = ['Column', 'Function', 'Result']
            print(tabulate(result_rows, headers=result_headers, tablefmt='psql'))
        else:
            print(tabulate(rows, headers=headers, tablefmt='psql'))

    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
