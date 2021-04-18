from bs4 import BeautifulSoup
import requests
import pandas as pd
import base64


def standard_data_item(raw_data):
    fine_data = raw_data
    fine_data = fine_data.text.strip()
    return fine_data


def get_data(tr):
    date = tr.find(class_='Item_DateItem')
    if date is not None:
        date = date.text.strip()
    props = tr.find_all(class_='Item_Price10')
    adjust_price = '',
    closed_price = '',
    open_price = '',
    max_price = '',
    min_price = '',
    if len(props) > 0:
        # Giá điều chỉnh [0], Giá đóng cửa [1], Giá mở cửa [5], Giá cao nhất [5], Giá thấp nhất [7]
        adjust_price = standard_data_item(props[0])
        closed_price = standard_data_item(props[1])
        open_price = standard_data_item(props[5])
        max_price = standard_data_item(props[6])
        min_price = standard_data_item(props[7])

    return {'Date': date, 'Giá điều chỉnh': adjust_price, 'Giá đóng cửa': closed_price, 'Giá mở cửa': open_price,
            'Giá cao nhất': max_price, 'Giá thấp nhất': min_price}


def crawl_ma_chung_khoan(ma, start_date, end_date):
    base64_message = 'aHR0cHM6Ly9zLmNhZmVmLnZuL0xpY2gtc3UtZ2lhby1kaWNoLXZjYi0xLmNobg=='
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    url = message_bytes.decode('ascii')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Cookie': 'cafef.IsMobile=IsMobile=NO; _ga=GA1.2.74394777.1618760631; _gid=GA1.2.263399120.1618760631; favorite_stocks_state=1; _ga=GA1.3.74394777.1618760631; _gid=GA1.3.263399120.1618760631'}
    payload = {
        'ctl00%24ContentPlaceHolder1%24ctl03%24txtKeyword': ma,
        'ctl00%24ContentPlaceHolder1%24ctl03%24dpkTradeDate1%24txtDatePicker': start_date,
        'ctl00%24ContentPlaceHolder1%24ctl03%24dpkTradeDate2%24txtDatePicker': end_date
    }
    session = requests.Session()
    response = session.post(url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)
    return soup


soup = crawl_ma_chung_khoan('VCB', '01%2F04%2F2021', '05%2F04%2F2021')

trs = soup.find_all('tr')
print(len(trs))
data = []
indexes = []

dates = []
adjs = []
closed_prices = []
opened_prices = []
max_prices = []
min_prices = []

for tr in trs:
    trs_data = get_data(tr)
    if trs_data is not None and trs_data['Date'] is not None:
        data_list = [trs_data['Date'], trs_data['Giá điều chỉnh'], trs_data['Giá đóng cửa'], trs_data['Giá mở cửa'],
                     trs_data['Giá cao nhất'], trs_data['Giá thấp nhất']]
        dates.append(trs_data['Date'])
        adjs.append(trs_data['Giá điều chỉnh'])
        closed_prices.append(trs_data['Giá đóng cửa'])
        opened_prices.append(trs_data['Giá mở cửa'])
        max_prices.append(trs_data['Giá cao nhất'])
        min_prices.append(trs_data['Giá thấp nhất'])

data = {
    'Date': dates,
    'Giá điều chỉnh': adjs,
    'Giá đóng cửa': closed_prices,
    'Giá mở cửa': opened_prices,
    'Giá cao nhất': max_prices,
    'Giá thấp nhất': min_prices
}

frame = pd.DataFrame(data)
print(frame)
