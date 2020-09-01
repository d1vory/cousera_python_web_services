from bs4 import BeautifulSoup
from decimal import Decimal



def transform_to_rur(value, nominal, amount = 1):
    return amount * (value / nominal)

def get_currency(to_value, to_nominal, amount_in_rur):
    return (to_nominal / to_value) * amount_in_rur

def get_value_nominal(currency, parsed_data):
    try:
        valute = parsed_data.find(lambda tag: tag.name=='charcode' and tag.text == currency ).parent
        return Decimal(str(valute.value.string).replace(',', '.')), Decimal(str(valute.nominal.string).replace(',', '.'))
    except:
        return None,None


def convert(amount, cur_from, cur_to, date, requests):


    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp',params={'date_req': date})  # Использовать переданный requests


    parsed  = BeautifulSoup(response.text, 'lxml')


    from_value, from_nominal = get_value_nominal(cur_from, parsed)

    amount_in_rur =  amount if cur_from == 'RUR' else transform_to_rur(from_value, from_nominal, amount)

    if cur_to == 'RUR':
        return  amount_in_rur

    to_value, to_nominal = get_value_nominal(cur_to, parsed)

    converted = get_currency(to_value, to_nominal, amount_in_rur)
    result = converted.quantize(Decimal('.0001'), rounding= 'ROUND_UP')
    return result  # не забыть про округление до 4х знаков после запятой
