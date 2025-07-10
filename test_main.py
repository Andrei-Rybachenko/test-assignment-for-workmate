import pytest
import csv
import os
from main import apply_filter, apply_aggregation, parse_condition


def make_rows_and_headers():
    headers = ["id", "brand", "price"]
    rows = [
        ["1", "apple", "1000"],
        ["2", "samsung", "800"],
        ["3", "apple", "600"],
        ["4", "xiaomi", "400"],
    ]
    return headers, rows


def test_parse_condition():
    assert parse_condition("price>500") == ("price", ">", "500")
    assert parse_condition("brand=apple") == ("brand", "=", "apple")
    assert parse_condition("price<=1000") == ("price", "<=", "1000")
    with pytest.raises(ValueError):
        parse_condition("invalid")


def test_apply_filter_numeric():
    headers, rows = make_rows_and_headers()
    filtered = apply_filter(rows, headers, "price>700")
    assert filtered == [["1", "apple", "1000"], ["2", "samsung", "800"]]
    filtered = apply_filter(rows, headers, "price<700")
    assert filtered == [["3", "apple", "600"], ["4", "xiaomi", "400"]]
    filtered = apply_filter(rows, headers, "price=800")
    assert filtered == [["2", "samsung", "800"]]


def test_apply_filter_string():
    headers, rows = make_rows_and_headers()
    filtered = apply_filter(rows, headers, "brand=apple")
    assert filtered == [["1", "apple", "1000"], ["3", "apple", "600"]]
    filtered = apply_filter(rows, headers, "brand=samsung")
    assert filtered == [["2", "samsung", "800"]]
    filtered = apply_filter(rows, headers, "brand=sony")
    assert filtered == []


def test_apply_aggregation_avg():
    headers, rows = make_rows_and_headers()
    result = apply_aggregation(rows, headers, "price=avg")
    assert result[0][2] == pytest.approx((1000+800+600+400)/4)


def test_apply_aggregation_min():
    headers, rows = make_rows_and_headers()
    result = apply_aggregation(rows, headers, "price=min")
    assert result[0][2] == 400


def test_apply_aggregation_max():
    headers, rows = make_rows_and_headers()
    result = apply_aggregation(rows, headers, "price=max")
    assert result[0][2] == 1000


def test_apply_aggregation_non_numeric():
    headers, rows = make_rows_and_headers()
    with pytest.raises(ValueError):
        apply_aggregation(rows, headers, "brand=avg")


def test_apply_filter_invalid_column():
    headers, rows = make_rows_and_headers()
    with pytest.raises(ValueError):
        apply_filter(rows, headers, "foo=bar")


def test_apply_aggregation_invalid_column():
    headers, rows = make_rows_and_headers()
    with pytest.raises(ValueError):
        apply_aggregation(rows, headers, "foo=avg")


def test_apply_aggregation_invalid_func():
    headers, rows = make_rows_and_headers()
    with pytest.raises(ValueError):
        apply_aggregation(rows, headers, "price=sum") 