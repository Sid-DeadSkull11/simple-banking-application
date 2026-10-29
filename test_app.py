
import pytest
import app as banking_app


@pytest.fixture(autouse=True)
def reset_balance():
    banking_app.balance = 1000.0
    yield
    banking_app.balance = 1000.0


def test_homepage():
    client = banking_app.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Simple Banking Application" in response.data


def test_check_balance():
    client = banking_app.app.test_client()
    response = client.post(
        "/result", data={"choice": "check_balance", "amount": ""}
    )
    assert response.status_code == 200
    assert "1000.00" in response.get_data(as_text=True)


def test_deposit_success():
    client = banking_app.app.test_client()
    response = client.post(
        "/result", data={"choice": "deposit", "amount": "250"}
    )
    assert response.status_code == 200
    assert "Deposit Successful" in response.get_data(as_text=True)
    assert "1250.00" in response.get_data(as_text=True)


def test_deposit_missing_amount():
    client = banking_app.app.test_client()
    response = client.post(
        "/result", data={"choice": "deposit", "amount": ""}
    )
    assert "Please enter an amount to deposit" in response.get_data(as_text=True)


@pytest.mark.parametrize("amount", ["0", "-50"])
def test_deposit_invalid_amount(amount):
    client = banking_app.app.test_client()
    response = client.post(
        "/result", data={"choice": "deposit", "amount": amount}
    )
    assert "Deposit amount must be positive" in response.get_data(as_text=True)


def test_deposit_non_numeric():
    client = banking_app.app.test_client()
    response = client.post(
        "/result", data={"choice": "deposit", "amount": "abc"}
    )
    assert "Invalid amount entered" in response.get_data(as_text=True)


def test_withdraw_success():
    client = banking_app.app.test_client()
    response = client.post(
        "/result", data={"choice": "withdraw", "amount": "200"}
    )
    assert response.status_code == 200
    assert "Withdrawal Successful" in response.get_data(as_text=True)
    assert "800.00" in response.get_data(as_text=True)


def test_withdraw_insufficient_balance():
    client = banking_app.app.test_client()
    response = client.post(
        "/result", data={"choice": "withdraw", "amount": "1500"}
    )
    assert "Insufficient Balance" in response.get_data(as_text=True)
    assert banking_app.balance == 1000.0


def test_withdraw_missing_amount():
    client = banking_app.app.test_client()
    response = client.post(
        "/result", data={"choice": "withdraw", "amount": ""}
    )
    assert "Please enter an amount to withdraw" in response.get_data(as_text=True)


@pytest.mark.parametrize("amount", ["0", "-100"])
def test_withdraw_invalid_amount(amount):
    client = banking_app.app.test_client()
    response = client.post(
        "/result", data={"choice": "withdraw", "amount": amount}
    )
    assert "Withdrawal amount must be positive" in response.get_data(as_text=True)


def test_withdraw_non_numeric():
    client = banking_app.app.test_client()
    response = client.post(
        "/result", data={"choice": "withdraw", "amount": "abc"}
    )
    assert "Invalid amount entered" in response.get_data(as_text=True)


def test_exit():
    client = banking_app.app.test_client()
    response = client.post(
        "/result", data={"choice": "exit", "amount": ""}
    )
    assert "Thank you for using the Banking Application" in response.get_data(as_text=True)
