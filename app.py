import streamlit as st
import pandas as pd
st.set_page_config(page_title='슈퍼마켓 매출 대시보드', layout='wide')
st.title('슈퍼마켓 매출 데이터 대시보드')
st.write('Sales.xlsx 데이터를 활용한 가장 기초적인 Streamlit 대시보드 예제입니다.')
@st.cache_data
def load_data():
 df = pd.read_excel('Sales.xlsx', sheet_name='supermarket_sales_test')
 df = df.dropna()
 return df
df = load_data()

st.sidebar.header('필터')
branch_option = st.sidebar.selectbox(
 '지점을 선택하세요',
 options=['전체'] + sorted(df['Branch'].unique().tolist())
)
if branch_option == '전체':
 filtered_df = df
else:
 filtered_df = df[df['Branch'] == branch_option]

col1, col2, col3 = st.columns(3)
col1.metric('총매출 합계', f"{filtered_df['Total'].sum():,.0f}")
col2.metric('평균 매출', f"{filtered_df['Total'].mean():,.2f}")
col3.metric('평균 만족도(Rating)', f"{filtered_df['Rating'].mean():.2f}")

st.subheader('데이터 미리보기')
st.dataframe(filtered_df.head(10))
st.subheader('상품 카테고리(Product line)별 평균 매출')
product_mean = filtered_df.groupby('Product line')['Total'].mean().sort_values(ascending=False)
st.bar_chart(product_mean)
st.subheader('시간대(Time_cat)별 거래 건수')
time_count = filtered_df['Time_cat'].value_counts()
st.bar_chart(time_count)
