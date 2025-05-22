import pytest
from unittest.mock import patch
import asyncio
import os

# --- Example functions/classes to test ---

def add(a, b):
    return a + b

def is_palindrome(s):
    return s == s[::-1]

def get_user_age(user):
    return user.get("age", None)

def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

async def fetch_data():
    await asyncio.sleep(0.1)
    return {"status": "success"}

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

def external_api_call():
    import requests
    response = requests.get("https://example.com/api")
    return response.json()

# --- Test cases ---

# 1. Simple math check
def test_add():
    assert add(2, 3) == 5

# 2. String palindrome check
@pytest.mark.parametrize("word,expected", [
    ("madam", True),
    ("hello", False),
    ("", True),
])
def test_is_palindrome(word, expected):
    assert is_palindrome(word) == expected

# 3. Dictionary key access with default
def test_get_user_age():
    assert get_user_age({"name": "Alice", "age": 30}) == 30
    assert get_user_age({"name": "Bob"}) is None

# 4. File reading (using pytest tmp_path)
def test_read_file(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text("hello world")
    assert read_file(p) == "hello world"

# 5. Async function returns expected dict
@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data()
    assert result == {"status": "success"}

# 6. BankAccount deposit increases balance
def test_deposit():
    account = BankAccount()
    account.deposit(100)
    assert account.balance == 100

# 7. BankAccount withdraw decreases balance
def test_withdraw():
    account = BankAccount(200)
    account.withdraw(50)
    assert account.balance == 150

# 8. Withdraw more than balance raises error
def test_withdraw_insufficient_funds():
    account = BankAccount(50)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(100)

# 9. Mocking external API call
@patch("requests.get")
def test_external_api_call(mock_get):
    mock_get.return_value.json.return_value = {"result": "ok"}
    assert external_api_call() == {"result": "ok"}

# 10. Parametrize multiple addition scenarios
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (2.5, 2.5, 5.0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected

# 11. Test exception on invalid file read
def test_read_file_not_exist():
    with pytest.raises(FileNotFoundError):
        read_file("no_such_file.txt")

# 12. Test string uppercase method
def test_string_upper():
    assert "hello".upper() == "HELLO"

# 13. Test list append operation
def test_list_append():
    lst = [1, 2]
    lst.append(3)
    assert lst == [1, 2, 3]

# 14. Test dictionary merge
def test_dict_merge():
    d1 = {"a": 1}
    d2 = {"b": 2}
    merged = {**d1, **d2}
    assert merged == {"a": 1, "b": 2}

# 15. Test function that returns None explicitly
def test_none_return():
    def func():
        return None
    assert func() is None

# 16. Test float approximate equality
def test_float_approx():
    assert pytest.approx(0.1 + 0.2, 0.0001) == 0.3

# 17. Test empty list is falsy
def test_empty_list_falsy():
    assert not []

# 18. Test a function that raises a custom exception
class MyError(Exception):
    pass

def error_func():
    raise MyError("Custom error happened")

def test_error_func():
    with pytest.raises(MyError, match="Custom error happened"):
        error_func()

# 19. Test environment variable is set (monkeypatch example)
def test_env_var_set(monkeypatch):
    monkeypatch.setenv("MY_VAR", "VALUE")
    import os
    assert os.getenv("MY_VAR") == "VALUE"

# 20. Test code that deletes a file (using tmp_path)
def test_file_delete(tmp_path):
    f = tmp_path / "temp.txt"
    f.write_text("data")
    assert f.exists()
    f.unlink()
    assert not f.exists()
