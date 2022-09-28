### Requirements:
    Python 3.10
    PostgreSQL
    Docker-compose

### Using:
    Django 4.1


### Quick start:
    Add your variables to .env

### Run:
    docker-compose up

### What to do
    Parse data from Google Sheet.
    Get exchange rate from "http://www.cbr.ru".
    Add column with exchanged currency to parsed data.
    Update database with new data.
    Send message with expired order numbers to Telegram.
