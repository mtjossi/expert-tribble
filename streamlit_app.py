import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

hsx_needed = ['BIC','BSI', 'CTD', 'DSN', 'DVP', 'DXG', 'EVE', 'FMC', 'FPT', 'GDT',
 'HUB', 'KDH', 'LBM', 'LPB', 'MBB', 'MIG', 'MWG', 'NSC', 'PTB', 'PVT', 'REE', 'SCS',
 'SHB', 'SSI', 'SZL', 'TCT', 'THG', 'TLG', 'TMS', 'TPB', 'TV2', 'VND', 'VNM']

hnx_needed = ['CDN', 'DAD', 'EID', 'PVI', 'ABI', 'HC3', 'HNI', 'HPP', 'LTG', 'MCH',
 'MPC', 'PHP', 'VGG', 'VTP', 'WSB']


st.title("Testing3")
#############################################
start_butt = st.button("Start:")
if start_butt:
    URL1 = "https://www.hsx.vn/Modules/Listed/Web/SymbolList?pageFieldName1=Code&pageFieldValue1=&pageFieldOperator1=eq&pageFieldName2=Sectors&pageFieldValue2=&pageFieldOperator2=&pageFieldName3=Sector&pageFieldValue3=00000000-0000-0000-0000-000000000000&pageFieldOperator3=&pageFieldName4=StartWith&pageFieldValue4=&pageFieldOperator4=&pageCriteriaLength=4&_search=false&nd=1667637899557&rows=1000&page=1&sidx=id&sord=desc"
    r = requests.get(URL1).json()

    all_rows = []
    for i in range(len(r['rows'])):
        ticker = r['rows'][i]['cell'][1]
        out_vol = r['rows'][i]['cell'][6].replace('.','').replace(',','.')
        row_data = [ticker, float(out_vol)]
        all_rows.append(row_data)
        
    df1 = pd.DataFrame(columns=['Ticker', 'Outstanding Volume'], data=all_rows)
    df1['Outstanding Volume'] = df1['Outstanding Volume']

    df_hsx = df1.copy()
    df_hsx = df_hsx[df_hsx['Ticker'].isin(hsx_needed)]
    #################################################################

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
    hnx_needed_dict['Outstanding Volume'] = hnx_os_list

    df_hnx = pd.DataFrame.from_dict(hnx_needed_dict)
    ##########################
    df_combo = pd.concat([df_hsx, df_hnx])
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
