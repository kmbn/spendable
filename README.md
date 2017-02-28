# Spendable
A web-based personal budget/expense-tracking app with a streamlined design focused on consistently tracking expenditures.

## Setup
1. `cd path/to/spendable`
2. Optional: set up a virtual environment using virtualenv.
3. Install the required packages: `pip install -r requirements.txt`
4. Set the secret key for session encryption: `export SECRET_KEY=<your_secret_key_here>` (if you're just testing, the length of the string doesn't matter).
5. Enable `export DEBUG=1` or disable `export DEBUG=0` debug mode for the built-in server (enabling debugging is recommended for testing; if you plan to run the app on a production server, though, debugging should be disabled).
6. Optional: in order to enable password reset emails, you'll need to export the following: `export MAIL_SERVER=<your.email.server>`, `export MAIL_USERNAME=<your@email.username>` and `export MAIL_PASSWORD=<your_password>`. If you don't do this, the app will crash if you try to reset your password.
7. `python run.py`.

## Usage
After completing the setup steps, open a browser and navigate to `http://localhost:5000/`. The first time you run the app you'l need to register; the current version of the app is intended to be single-user, so it is only possible to create one account.

By default, transactions are assumed to be expenses, so you don't need to type a `-` before the value. To record income or other positive cash flow, type a `-` before the value.