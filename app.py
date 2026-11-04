import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 레이아웃 및 제목 설정
st.set_page_config(page_title="수퍼마켓 매출 대시보드", layout="wide")

# 앱 메인 타이틀
st.title("🛒 Supermarket Sales 분석 대시보드")
st.markdown("---")

# 1. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    try:
        # Sales.xlsx의 supermarket_sales_test 시트 로드
        df = pd.read_excel('Sales.xlsx', sheet_name='supermarket_sales_test')
        # 결측치 제거
        df = df.dropna()
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

df = load_data()

if df is not None:
    # 2. 사이드바 설정
    st.sidebar.header("⚙️ 필터 옵션")
    
    # 지점(Branch) 목록 추출
    branch_list = sorted(df['Branch'].unique())
    selected_branch = st.sidebar.selectbox("분석할 지점(Branch)을 선택하세요:", branch_list)
    
    # 선택한 지점으로 데이터 필터링
    filtered_df = df[df['Branch'] == selected_branch]
    
    # 3. 메인 화면 - 선택 지점의 KPI 메트릭
    st.subheader(f"📍 {selected_branch} 지점 주요 요약 지표")
    
    # 지표 계산
    total_sales = filtered_df['Total'].sum() if 'Total' in filtered_df.columns else filtered_df['gross income'].sum()  # 열 이름 보정 대비
    avg_sales = filtered_df['Total'].mean() if 'Total' in filtered_df.columns else filtered_df['gross income'].mean()
    avg_rating = filtered_df['Rating'].mean()
    
    # 메트릭 표시 레이아웃
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="💰 총 매출", value=f"${total_sales:,.2f}")
    with col2:
        st.metric(label="📈 평균 매출", value=f"${avg_sales:,.2f}")
    with col3:
        st.metric(label="⭐ 평균 평점", value=f"{avg_rating:.2f} / 10")
        
    st.markdown("---")
    
    # 4. 상품 카테고리(Product line)별 평균 매출 시각화
    st.subheader("📦 상품 카테고리(Product line)별 평균 매출")
    
    # 그룹화 분석
    category_sales = filtered_df.groupby('Product line')['Total'].mean().reset_index() if 'Total' in filtered_df.columns else filtered_df.groupby('Product line')['gross income'].mean().reset_index()
    category_sales.columns = ['Product line', 'Average Sales']
    category_sales = category_sales.sort_values(by='Average Sales', ascending=False)
    
    # Plotly 막대 그래프 그리기
    fig = px.bar(
        category_sales,
        x='Product line',
        y='Average Sales',
        text_auto='.2s',
        labels={'Product line': '상품 카테고리', 'Average Sales': '평균 매출 ($)'},
        color='Average Sales',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        xaxis_title="상품 카테고리",
        yaxis_title="평균 매출 ($)",
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("현재 디렉토리에 'Sales.xlsx' 파일이 있는지 확인해 주세요.")
