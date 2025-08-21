import streamlit as st
import os
import sys
from pathlib import Path
from pages import home_page, module_a_page, module_b_page, module_c_page

# 设置页面配置
st.set_page_config(
    page_title="信号处理工具",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 创建临时目录
os.makedirs(os.path.join(os.path.dirname(__file__), "temp"), exist_ok=True)

# 页面路由
def main():
    # 获取URL参数
    query_params = st.experimental_get_query_params()
    page = "home"
    
    if "page" in query_params:
        page_param = query_params["page"][0]
        if page_param == "module_a":
            page = "module_a"
        elif page_param == "module_b":
            page = "module_b"
        elif page_param == "module_c":
            page = "module_c"
    
    # 侧边栏导航
    with st.sidebar:
        st.title("导航")
        
        st.markdown("### 模块")
        if st.button("主页", key="sidebar_home"):
            st.experimental_set_query_params(page="home")
            page = "home"
        if st.button("模块A: 单点信号处理", key="sidebar_module_a"):
            st.experimental_set_query_params(page="module_a")
            page = "module_a"
        if st.button("模块B: B扫描信号处理", key="sidebar_module_b"):
            st.experimental_set_query_params(page="module_b")
            page = "module_b"
        if st.button("模块C: 波场数据处理", key="sidebar_module_c"):
            st.experimental_set_query_params(page="module_c")
            page = "module_c"
        
        st.markdown("---")
        
        # 关于信息
        st.markdown("### 关于")
        st.info("""
        **信号处理工具 - Python版本**
        
        这是原MATLAB信号处理工具的Python重新实现版本，使用Streamlit作为GUI框架。
        
        版本: 1.0.0
        """)
    
    # 根据选择的页面显示相应的内容
    if page == "home":
        home_page.app()
    elif page == "module_a":
        module_a_page.app()
    elif page == "module_b":
        module_b_page.app()
    elif page == "module_c":
        module_c_page.app()
    
    # 页脚
    st.markdown("""<div style='text-align: center'>
                <p>© 2023 信号处理工具 | Python版本</p>
                </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()