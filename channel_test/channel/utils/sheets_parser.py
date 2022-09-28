from datetime import date, datetime
from decimal import Decimal

import gspread
from gspread import Worksheet, Spreadsheet, Client
import requests
import xmltodict

from config import settings

SHEET_URL = settings.SHEET_URL


class SheetsParser:
    """
    Parse data from Google Sheet. Get exchange rate from CBR.
    Update parsed data with exchange rate for every record.

    Attributes

        currency: str = 'USD'
            Currency for getting exchange rate, default = 'USD'

        sheet_url: str = settings.SHEET_URL
            URL to Google Sheet, default from .env field SHEET_URL

        google_token_filename: str = 'token.json'
            Filepath to file with Google Sheet access token

    Methods
        get_data

        get_google_datalist

        get_exchange_rate
    """

    def __init__(
            self,
            currency: str = 'USD',
            sheet_url: str = '',
            google_token_filename: str = 'token.json'
    ):
        self.currency: str = currency
        self.sheet_url: str = sheet_url or SHEET_URL
        self.google_token_filename: str = google_token_filename

    def get_data(self) -> list[dict]:
        """Returns parsed data from Google Sheets with adding
        current exchange rate for every record

        :return: Updated data list[dict]
        """

        google_data: list[dict] = self.get_google_datalist()
        exchange_rate: 'Decimal' = self.get_exchange_rate()
        updated_data: list[dict] = self.__update_keys_and_add_exchanged_field(
            google_data, exchange_rate
        )

        return updated_data

    def get_google_datalist(self) -> list[dict]:
        """
        Returns parsed data from Google Sheet

        :return: Parsed data list[dict]
        """

        client: Client = gspread.service_account(filename=self.google_token_filename)

        sheets: Spreadsheet = client.open_by_url(self.sheet_url)
        worksheet: Worksheet = sheets.get_worksheet(0)
        worksheet_data: list[dict] = worksheet.get_all_records()

        return worksheet_data

    def get_exchange_rate(self, currency: str = '') -> 'Decimal':
        """
        Returns current currency value from CBR API

        :return: (Decimal) Rounded to 2-nd digit value
        """

        if not currency:
            currency = self.currency
        current_date: str = date.today().strftime("%d/%m/%Y")
        url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={current_date}'
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.RequestException(f'Request error: status code: {response.status_code}')
        answer: str = response.text
        if currency in answer:
            parsed_data: dict[str, dict] = xmltodict.parse(answer)
            currencies: tuple[dict] = tuple(parsed_data['ValCurs']['Valute'])
            for elem in currencies:
                if elem['CharCode'] == currency:
                    value: str = elem.get('Value').replace(',', '.')

                    return Decimal(value).quantize(Decimal('1.00'))

        raise ValueError("Currency not found")

    @staticmethod
    def __get_valid_date_format(transfer_date: str) -> str:
        """Returns string with date in datetime object format"""

        return str(datetime.strptime(transfer_date, '%d.%m.%Y').date())

    def __update_keys_and_add_exchanged_field(
            self,
            data: list[dict],
            exchange_rate: Decimal
    ) -> list[dict]:

        """Returns updated list of dictionaries
        with current exchange rate for every element.
        Change keys to database model fields names.
        Replace date for transfer_date field to datetime format.

        :return: Updated list[dict]
        """

        orders = data[:]
        for order in orders:
            order['serial_number'] = order.pop('№')
            order['order_number'] = order.pop('заказ №')
            order['usd_cost'] = order.pop('стоимость,$')
            order['transfer_date'] = self.__get_valid_date_format(order.pop('срок поставки'))
            usd_price: int = int(order['usd_cost'])
            rubles_price: Decimal = usd_price * exchange_rate
            order['rubles_cost'] = rubles_price.to_eng_string()

        return orders
