import streamlit as st
import os
import sys

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def app():
    """
    主页面
    """
    st.title("信号处理工具")
    
    st.markdown("""
    ## 欢迎使用信号处理工具
    
    这是一个功能强大的信号处理工具，可以帮助您进行各种信号处理任务。
    
    ### 主要功能
    
    本工具提供以下三个主要模块：
    
    1. **单点信号处理**：处理单个信号，支持各种滤波、频谱分析和时频分析。
    2. **B扫描信号处理**：处理多个位置的信号，生成B扫描图像，进行位置-时间分析。
    3. **波场数据处理**：处理二维空间中的波场数据，进行时空分析和可视化。
    
    ### 使用方法
    
    1. 在左侧导航栏选择您需要使用的模块
    2. 上传数据文件或指定数据文件夹
    3. 设置处理参数
    4. 点击处理按钮进行数据处理和可视化
    
    ### 支持的数据格式
    
    - **TXT文件**：每行一个数据点，第一行可以包含采样率信息
    - **MAT文件**：MATLAB数据文件，包含信号数据和相关参数
    """)
    
    # 显示模块卡片
    st.subheader("选择模块")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        ### 单点信号处理
        
        处理单个信号，支持：
        - 多种滤波器
        - 时域分析
        - 频域分析
        - 时频分析
        - 包络提取
        
        [进入模块 →](/?page=module_a)
        """)
    
    with col2:
        st.info("""
        ### B扫描信号处理
        
        处理多个位置的信号，支持：
        - B扫描图像生成
        - 位置-时间分析
        - 瀑布图
        - 3D可视化
        
        [进入模块 →](/?page=module_b)
        """)
    
    with col3:
        st.info("""
        ### 波场数据处理
        
        处理二维空间中的波场数据，支持：
        - 时间切片分析
        - 能量图
        - 最大幅值图
        - 到达时间图
        - 波场动画
        
        [进入模块 →](/?page=module_c)
        """)
    
    # 显示关于信息
    st.subheader("关于")
    st.markdown("""
    本工具是基于Python的信号处理工具，使用Streamlit构建用户界面，
    集成了NumPy、SciPy、Matplotlib和Plotly等科学计算和可视化库。
    
    原始MATLAB版本的功能已完全迁移到Python，并进行了扩展和优化。
    
    © 2023 信号处理工具团队
    """)

if __name__ == "__main__":
    app()