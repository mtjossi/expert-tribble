import streamlit as st
import requests
import pandas as pd

URL = "https://www.hsx.vn/Modules/Listed/Web/SymbolList?pageFieldName1=Code&pageFieldValue1=&pageFieldOperator1=eq&pageFieldName2=Sectors&pageFieldValue2=&pageFieldOperator2=&pageFieldName3=Sector&pageFieldValue3=00000000-0000-0000-0000-000000000000&pageFieldOperator3=&pageFieldName4=StartWith&pageFieldValue4=&pageFieldOperator4=&pageCriteriaLength=4&_search=false&nd=1667637899557&rows=1000&page=1&sidx=id&sord=desc"
r = requests.get(URL).json()

all_rows = []
for i in range(len(r['rows'])):
    row_data = [r['rows'][i]['cell'][1], r['rows'][i]['cell'][2], r['rows'][i]['cell'][6]]
    all_rows.append(row_data)

df = pd.DataFrame(columns=['Ticker', 'ISIN', 'Outstanding Volume'], data=all_rows)

st.header("Differences?")

default_list = ['BIC',
 'BSI',
 'CTD',
 'DSN',
 'DVP',
 'DXG',
 'EVE',
 'FMC',
 'FPT',
 'GDT',
 'HUB',
 'KDH',
 'LBM',
 'LPB',
 'MBB',
 'MIG',
 'MWG',
 'NSC',
 'PTB',
 'PVT',
 'REE',
 'SCS',
 'SHB',
 'SSI',
 'SZL',
 'TCT',
 'THG',
 'TLG',
 'TMS',
 'TPB',
 'TV2',
 'VND',
 'VNM']

st.sidebar.header("Which tickers do you want to compare?")
selected_tickers = st.sidebar.multiselect("Enter the Tickers you want to compare:", df['Ticker'].to_list(), default=default_list)

# st.write(selected_tickers)

final_df = df[df['Ticker'].isin(selected_tickers)]
st.dataframe(final_df)

# uploadedFile = st.file_uploader("Upload the file you want to compare", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")

# st.dataframe(pd.read_csv(uploadedFile))

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(final_df)

st.download_button(
    "Click to Download",
    csv,
    'file.csv',
    "text/csv",
    key='download-csv'
)