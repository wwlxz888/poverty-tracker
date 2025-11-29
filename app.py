import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 设置网页标题和布局
st.set_page_config(page_title="防返贫监测数据录入系统 - 昕泽", layout="centered")

# 定义数据文件的名称
DATA_FILE = 'poverty_data.csv'

# --- 核心函数：加载数据 ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # 如果文件不存在，创建一个空的DataFrame
        return pd.DataFrame(columns=['姓名', '性别', '月收入', '风险点', '家庭人口', '录入时间'])

# --- 核心函数：保存数据 ---
def save_data(new_entry):
    df = load_data()
    # 将新数据转换为DataFrame并合并
    new_df = pd.DataFrame([new_entry])
    df = pd.concat([df, new_df], ignore_index=True)
    # 保存为CSV文件
    df.to_csv(DATA_FILE, index=False)
    return df

# --- 网页界面搭建 ---

# 1. 侧边栏（增加专业感，显得像个正式系统）
with st.sidebar:
    st.header("系统管理面板")
    st.info(f"当前管理员：**昕泽**")
    st.write(f"所属区域：**隆化镇党群服务中心**")
    st.write(f"当前日期：{datetime.now().strftime('%Y-%m-%d')}")

# 2. 主标题区
st.title("📋 防返贫监测对象信息录入台账")

# 【改动点1】在这里显著展示你的名字，截图时一眼就能看到
st.markdown("""
    <style>
    .big-font {
        font-size:18px !important;
        color: #555;
    }
    </style>
    <p class="big-font"><b>系统开发/台账负责人：昕泽</b></p>
    """, unsafe_allow_html=True)

st.write("---") # 分割线

# 【改动点2】修改为具体的村名
st.markdown("### 数字化信息采集入口（隆化村）")
st.info("说明：请输入农户的具体信息，点击提交后系统将自动汇总。")

# 3. 创建录入表单
with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("姓名", placeholder="请输入户主姓名")
        income = st.number_input("月收入 (元)", min_value=0, step=100)

    with col2:
        gender = st.selectbox("性别", ["男", "女"])
        family_count = st.number_input("家庭人口 (人)", min_value=1, step=1)

    risk_point = st.text_area("风险点 (主要致贫/返贫原因)", placeholder="例如：因病、缺少劳动力、自然灾害等")

    # 提交按钮
    submitted = st.form_submit_button("✅ 提交录入")

    if submitted:
        if not name:
            st.error("请务必填写姓名！")
        else:
            # 准备要保存的数据
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_entry = {
                '姓名': name,
                '性别': gender,
                '月收入': income,
                '风险点': risk_point,
                '家庭人口': family_count,
                '录入时间': current_time
            }

            # 保存数据
            save_data(new_entry)
            st.success(f"成功录入：{name} 的信息已保存！")

# --- 4. 数据展示与导出区 ---
st.write("---")
st.subheader("📊 实时台账预览")

# 加载最新数据
current_df = load_data()

if not current_df.empty:
    # 展示表格
    st.dataframe(current_df, use_container_width=True)

    # 导出按钮
    csv_data = current_df.to_csv(index=False).encode('utf-8-sig')  # utf-8-sig 防止中文乱码

    st.download_button(
        label="📥 导出完整台账 (CSV/Excel)",
        data=csv_data,
        file_name='防返贫监测台账_导出.csv',
        mime='text/csv',
    )
else:
    st.caption("暂无数据，请在上方录入。")
