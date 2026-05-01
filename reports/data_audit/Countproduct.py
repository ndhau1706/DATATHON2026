import pandas as pd
import numpy as np

product_order_counts_df= pd.read_csv('ord_orditem_pro_promo.csv')

# 2. Tổng hợp dữ liệu
# Nhóm theo các thuộc tính định danh và phân loại, sau đó đếm số đơn hàng (order_id)
summary_df = product_order_counts_df.groupby(['product_id', 'product_name', 'category', 'segment','order_status']).size().reset_index(name='order_count')

# 3. Sắp xếp theo số lượng đơn hàng giảm dần
summary_df = summary_df.sort_values(by='order_count', ascending=False)
summary_df.to_csv('product_order_summary.csv', index=False)