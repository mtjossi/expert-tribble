import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import certifi
from utils import hsx_needed, hnx_needed, hsx_dic
import json

requests.packages.urllib3.util.ssl_.DEFAULT_CA_BUNDLE = certifi.where()

disable_warnings(InsecureRequestWarning)



st.title("Testing3")
#############################################
start_butt = st.button("Start:")
if start_butt:
    # HSX
    hsx_df = pd.DataFrame(columns=['Ticker', 'Outstanding Shares'])
    tickers = []
    outs = []
    for k, v in hsx_dic.items():
        URL = f"https://api.hsx.vn/l/api/v1/2/securities/{v}"
        r = requests.get(URL)
        data = json.loads(r.text)
        tickers.append(k)
        outs.append(data['data']['outStanding'])

    hsx_df['Ticker'] = tickers
    hsx_df['Outstanding Shares'] = outs
    
    # HNX
    hnx_needed_dict = {}
    hnx_ticker_list = []
    hnx_os_list = []

    for t in hnx_needed:
        hnx_url = f"https://hnx.vn/en-gb/cophieu-etfs/chi-tiet-chung-khoan-ny-{t}.html?_des_tab=1"
        r4 = requests.get(hnx_url, verify=False)
        
        soup = BeautifulSoup(r4.text, features = 'html.parser')
        div_class = "dktimkiem_cell_content"
        all_data = soup.find_all("div", class_=div_class)
        all_data_list = []
        for i in all_data:
            all_data_list.append(i.get_text().split())

        out_shares = int(all_data_list[-2][0].replace(',', ''))
        hnx_ticker_list.append(t)
        hnx_os_list.append(out_shares)

    hnx_needed_dict['Ticker'] = hnx_ticker_list
    hnx_needed_dict['Outstanding Shares'] = hnx_os_list

    df_hnx = pd.DataFrame.from_dict(hnx_needed_dict)
    ##########################
    df_combo = pd.concat([hsx_df, df_hnx])
    # df_combo = df_hnx.copy()
    df_combo = df_combo.sort_values(by='Ticker').reset_index(drop=True)
    df_combo['Ticker'] = [f"{n} VN" for n in df_combo['Ticker']]

    st.dataframe(df_combo)

    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df_combo)

    st.download_button(
        "Click to Download",
        csv,
        'file.csv',
        "text/csv",
        key='download-csv'
    )
