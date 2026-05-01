import pandas as pd
import plotly.express as px


df = pd.read_csv('product_order_summary.csv')

df_tree = df.groupby(['category', 'segment'])['order_count'].sum().reset_index()

fig2 = px.treemap(
    df_tree, 
    path=[px.Constant("Toàn bộ thị trường"), 'category', 'segment'], 
    values='order_count',
    title='<b>TỶ TRỌNG ĐƠN HÀNG CHIA THEO DANH MỤC VÀ PHÂN KHÚC</b>', 
    color='order_count',
    color_continuous_scale='Blues'
)
fig2.update_traces(
    textinfo="label+value+percent parent",
    textfont=dict(size=18)  
)

fig2.update_layout(
    title={
        'y': 0.95,              
        'x': 0.5,               
        'xanchor': 'center',    
        'yanchor': 'top',
        'font': dict(
            size=24,            
            color='black'
        )
    },
    margin=dict(t=80, l=25, r=25, b=25) 
)

html_filename = "Bieu_do_2_Treemap_Tuong_Tac.html"
fig2.write_html(html_filename)
