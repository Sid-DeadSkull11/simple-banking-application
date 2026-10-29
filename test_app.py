import pytest

import app as banking_app


@pytest.fixture(autouse=True)
def reset_balance():
    banking_app.balance = 1000.0
    yield
    banking_app.balance = 1000.0


def test_homepage_loads_successfully():
    client = banking_app.app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_check_balance_displays_1000():
    client = banking_app.app.test_client()

    response = client.post("/result", data={"choice": "check_balance", "amount": ""})

    assert response.status_code == 200
    assert "₹1000.00" in response.get_data(as_text=True)


def test_deposit_positive_amount_updates_balance():
    client = banking_app.app.test_client()

    response = client.post("/result", data={"choice": "deposit", "amount": "250"})

    assert response.status_code == 200
    assert "Deposit Successful" in response.get_data(as_text=True)
    assert "₹1250.00" in response.get_data(as_text=True)


def test_missing_deposit_amount_displays_error():
    client = banking_app.app.test_client()

    response = client.post("/result", data={"choice": "deposit", "amount": ""})

    assert response.status_code == 200
    assert "Please enter an amount to deposit" in response.get_data(as_text=True)


@pytest.mark.parametrize("amount", ["0", "-50"])
def test_zero_or_negative_deposit_is_rejected(amount):
    client = banking_app.app.test_client()

    response = client.post("/result", data={"choice": "deposit", "amount": amount})

    assert response.status_code == 200
    assert "Deposit amount must be positive" in response.get_data(as_text=True)


def test_invalid_numeric_deposit_displays_error():
    client = banking_app.app.test_client()

    response = client.post("/result", data={"choice": "deposit", "amount": "abc"})

    assert response.status_code == 200
    assert "Invalid amount entered" in response.get_data(as_text=True)


def test_exit_option_displays_thank_you_message():
    client = banking_app.app.test_client()

    response = client.post("/result", data={"choice": "exit", "amount": ""})

    assert response.status_code == 200
    assert "Thank you for using the Banking Application" in response.get_data(as_text=True)