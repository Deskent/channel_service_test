from sheets_parser import SheetsParser


if __name__ == '__main__':
    url = 'https://docs.google.com/spreadsheets/d/153fuB1T1f-JiU_LVzU8Pc3MlxtdMqwm-cd0GcEydPRs'

    result = SheetsParser(currency='USD', sheet_url=url).get_data()
    print(result)
