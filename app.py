from flask import Flask, request

app = Flask(__name__)

# Initial account balance
balance = 1000.0


@app.route("/")
def home():
    return """
    <h2>Simple Banking Application</h2>
    <form action="/result" method="post">
        <label for="choice">Select an option:</label><br><br>
        <select name="choice" id="choice">
            <option value="check_balance">1. Check Balance</option>
            <option value="deposit">2. Deposit Money</option>
            <option value="withdraw">3. Withdraw Money</option>
            <option value="exit">4. Exit</option>
        </select><br><br>

        <label for="amount">Amount (for deposit/withdraw):</label><br>
        <input type="number" id="amount" name="amount" step="0.01" placeholder="Enter amount"><br><br>

        <button type="submit">Submit</button>
    </form>
    """


@app.route("/result", methods=["POST"])
def result():
    global balance

    choice = request.form.get("choice")
    amount_text = request.form.get("amount")

    # Check Balance
    if choice == "check_balance":
        return f"""
        <h3>Balance</h3>
        Your current balance is: ₹{balance:.2f}<br><br>
        <a href="/">Go Back</a>
        """

    # Deposit Money
    elif choice == "deposit":
        if amount_text is None or amount_text == "":
            return """
            <h3>Error</h3>
            Please enter an amount to deposit.<br><br>
            <a href="/">Go Back</a>
            """

        try:
            amount = float(amount_text)
        except ValueError:
            return """
            <h3>Error</h3>
            Invalid amount entered. Please enter a valid number.<br><br>
            <a href="/">Go Back</a>
            """

        if amount <= 0:
            return """
            <h3>Error</h3>
            Deposit amount must be positive.<br><br>
            <a href="/">Go Back</a>
            """

        balance += amount
        return f"""
        <h3>Deposit Successful</h3>
        Deposited amount: ₹{amount:.2f}<br>
        Updated balance: ₹{balance:.2f}<br><br>
        <a href="/">Go Back</a>
        """

    # Withdraw Money
    elif choice == "withdraw":
        if amount_text is None or amount_text == "":
            return """
            <h3>Error</h3>
            Please enter an amount to withdraw.<br><br>
            <a href="/">Go Back</a>
            """

        try:
            amount = float(amount_text)
        except ValueError:
            return """
            <h3>Error</h3>
            Invalid amount entered. Please enter a valid number.<br><br>
            <a href="/">Go Back</a>
            """

        if amount <= 0:
            return """
            <h3>Error</h3>
            Withdrawal amount must be positive.<br><br>
            <a href="/">Go Back</a>
            """

        if amount > balance:
            return f"""
            <h3>Insufficient Balance</h3>
            Withdrawal amount: ₹{amount:.2f}<br>
            Available balance: ₹{balance:.2f}<br><br>
            <a href="/">Go Back</a>
            """

        balance -= amount
        return f"""
        <h3>Withdrawal Successful</h3>
        Withdrawn amount: ₹{amount:.2f}<br>
        Updated balance: ₹{balance:.2f}<br><br>
        <a href="/">Go Back</a>
        """

    # Exit
    elif choice == "exit":
        return """
        <h3>Thank you for using the Banking Application.</h3>
        <a href="/">Go Back</a>
        """

    else:
        return """
        <h3>Error</h3>
        Invalid option selected.<br><br>
        <a href="/">Go Back</a>
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)