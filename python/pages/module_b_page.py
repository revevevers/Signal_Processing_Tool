import streamlit as st
import numpy as np
import pandas as pd
import os
import sys
from io import StringIO

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from modules.module_b.processor import BScanProcessor
from modules.module_b.visualizer import BScanVisualizer

def module_b_page():
    """
    模块B页面：B扫描信号处理
    """
    st.title("📊 B扫描信号处理")
    st.markdown("---")
    
    # 初始化session state
    if 'processor_b' not in st.session_state:
        st.session_state.processor_b = BScanProcessor()
    
    if 'visualizer_b' not in st.session_state:
        st.session_state.visualizer_b = BScanVisualizer()
    
    processor = st.session_state.processor_b
    visualizer = st.session_state.visualizer_b
    
    # 侧边栏 - 文件加载和基本信息
    with st.sidebar:
        st.header("📁 数据加载")
        
        # 文件夹选择
        folder_path = st.text_input(
            "输入数据文件夹路径",
            value="/Users/zyt/Documents/Signal_Processing_Tool/python/data/bscan/txt_files",
            help="包含TXT信号文件的文件夹路径"
        )
        
        file_pattern = st.text_input(
            "文件名模式（可选）",
            value="signal_*.txt",
            help="例如：signal_*.txt 或 *.txt"
        )
        
        if st.button("📂 加载文件夹数据", use_container_width=True):
            if os.path.exists(folder_path):
                if processor.load_from_folder(folder_path, file_pattern):
                    st.success(f"✅ 成功加载 {len(processor.signals)} 个信号文件")
                    
                    # 显示文件夹信息
                    st.subheader("📋 文件夹信息")
                    st.write(f"**文件夹：** {folder_path}")
                    st.write(f"**信号数量：** {len(processor.signals)} 个")
                    st.write(f"**采样率：** {processor.sampling_rate:.0f} Hz")
                    st.write(f"**位置范围：** {min(processor.positions):.1f} - {max(processor.positions):.1f}")
                else:
                    st.error("❌ 文件夹数据加载失败")
            else:
                st.error("❌ 文件夹路径不存在")
        
        # MAT文件加载
        st.markdown("---")
        uploaded_mat = st.file_uploader(
            "或上传MAT文件",
            type=['mat'],
            help="包含B扫描数据的MAT文件"
        )
        
        if uploaded_mat is not None:
            temp_path = f"/tmp/{uploaded_mat.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_mat.getbuffer())
            
            if processor.load_from_mat(temp_path):
                st.success(f"✅ MAT文件加载成功：{uploaded_mat.name}")
                st.write(f"**数据形状：** {processor.bscan_data.shape}")
            else:
                st.error("❌ MAT文件加载失败")
        
        # 示例数据按钮
        st.markdown("---")
        if st.button("📁 加载示例数据", use_container_width=True):
            example_path = "/Users/zyt/Documents/Signal_Processing_Tool/python/data/bscan/bscan_data.mat"
            if os.path.exists(example_path):
                if processor.load_from_mat(example_path):
                    st.success("✅ 示例数据加载成功")
                else:
                    st.error("❌ 示例数据加载失败")
            else:
                st.error("❌ 示例数据文件不存在")
    
    # 主内容区域
    if processor.signals:
        
        # 滤波器控制面板
        st.header("🔧 信号处理控制")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("带通滤波器")
            enable_bandpass = st.checkbox("启用带通滤波", key="bandpass_enable")
            if enable_bandpass:
                low_freq = st.number_input(
                    "低截止频率 (Hz)", 
                    min_value=100.0, 
                    max_value=1000000.0, 
                    value=100000.0,
                    step=1000.0,
                    key="bandpass_low"
                )
                high_freq = st.number_input(
                    "高截止频率 (Hz)", 
                    min_value=100.0, 
                    max_value=1000000.0, 
                    value=500000.0,
                    step=1000.0,
                    key="bandpass_high"
                )
                bandpass_order = st.selectbox(
                    "滤波器阶数", 
                    [2, 4, 6, 8], 
                    index=1,
                    key="bandpass_order"
                )
        
        with col2:
            st.subheader("低通滤波器")
            enable_lowpass = st.checkbox("启用低通滤波", key="lowpass_enable")
            if enable_lowpass:
                lowpass_freq = st.number_input(
                    "截止频率 (Hz)", 
                    min_value=100.0, 
                    max_value=1000000.0, 
                    value=300000.0,
                    step=1000.0,
                    key="lowpass_freq"
                )
                lowpass_order = st.selectbox(
                    "滤波器阶数", 
                    [2, 4, 6, 8], 
                    index=1,
                    key="lowpass_order"
                )
        
        with col3:
            st.subheader("高通滤波器")
            enable_highpass = st.checkbox("启用高通滤波", key="highpass_enable")
            if enable_highpass:
                highpass_freq = st.number_input(
                    "截止频率 (Hz)", 
                    min_value=100.0, 
                    max_value=1000000.0, 
                    value=50000.0,
                    step=1000.0,
                    key="highpass_freq"
                )
                highpass_order = st.selectbox(
                    "滤波器阶数", 
                    [2, 4, 6, 8], 
                    index=1,
                    key="highpass_order"
                )
        
        # 其他滤波器
        st.markdown("---")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.subheader("中值滤波器")
            enable_median = st.checkbox("启用中值滤波", key="median_enable")
            if enable_median:
                median_kernel = st.selectbox(
                    "核大小", 
                    [3, 5, 7, 9, 11], 
                    index=1,
                    key="median_kernel"
                )
        
        with col5:
            st.subheader("Savitzky-Golay滤波器")
            enable_savgol = st.checkbox("启用SG滤波", key="savgol_enable")
            if enable_savgol:
                savgol_window = st.selectbox(
                    "窗口长度", 
                    [11, 21, 31, 41, 51], 
                    index=0,
                    key="savgol_window"
                )
                savgol_order = st.selectbox(
                    "多项式阶数", 
                    [2, 3, 4, 5], 
                    index=1,
                    key="savgol_order"
                )
        
        with col6:
            st.subheader("信号处理")
            enable_normalize = st.checkbox("归一化信号", key="normalize_enable")
        
        # 应用滤波器按钮
        st.markdown("---")
        col_apply, col_reset = st.columns([1, 1])
        
        with col_apply:
            if st.button("🔄 应用滤波器", type="primary", use_container_width=True):
                # 重置处理
                processor.reset_processing()
                
                # 应用滤波器
                try:
                    if enable_bandpass and low_freq < high_freq:
                        processor.apply_bandpass_filter(low_freq, high_freq, bandpass_order)
                    
                    if enable_lowpass:
                        processor.apply_lowpass_filter(lowpass_freq, lowpass_order)
                    
                    if enable_highpass:
                        processor.apply_highpass_filter(highpass_freq, highpass_order)
                    
                    if enable_median:
                        processor.apply_median_filter(median_kernel)
                    
                    if enable_savgol:
                        processor.apply_savgol_filter(savgol_window, savgol_order)
                    
                    if enable_normalize:
                        processor.normalize_signals()
                    
                    st.success("✅ 滤波器应用成功")
                    
                except Exception as e:
                    st.error(f"❌ 滤波器应用失败：{str(e)}")
        
        with col_reset:
            if st.button("🔄 重置处理", use_container_width=True):
                processor.reset_processing()
                st.success("✅ 信号已重置为原始状态")
        
        # B扫描创建选项
        st.markdown("---")
        st.header("🖼️ B扫描创建")
        
        col_bscan1, col_bscan2 = st.columns(2)
        
        with col_bscan1:
            bscan_normalize = st.checkbox("归一化B扫描", value=True, key="bscan_normalize")
            bscan_envelope = st.checkbox("计算包络", value=False, key="bscan_envelope")
        
        with col_bscan2:
            if bscan_envelope:
                envelope_method = st.selectbox("包络计算方法", ["hilbert", "peak"], index=0, key="envelope_method")
        
        if st.button("📊 创建B扫描", type="primary", use_container_width=True):
            try:
                bscan_data = processor.create_bscan(bscan_normalize, bscan_envelope, envelope_method if bscan_envelope else 'hilbert')
                if bscan_data is not None:
                    st.success(f"✅ B扫描创建成功，形状：{bscan_data.shape}")
                else:
                    st.error("❌ B扫描创建失败")
            except Exception as e:
                st.error(f"❌ B扫描创建失败：{str(e)}")
        
        # 可视化部分
        if processor.bscan_data is not None:
            st.markdown("---")
            st.header("📈 B扫描可视化")
            
            # 创建标签页
            tab1, tab2, tab3, tab4 = st.tabs(["B扫描图像", "3D B扫描", "瀑布图", "信号切片"])
            
            with tab1:
                st.subheader("B扫描图像")
                try:
                    fig_bscan = visualizer.plot_bscan_interactive(
                        processor.bscan_data,
                        processor.time_axis,
                        processor.positions,
                        title="B扫描图像"
                    )
                    st.plotly_chart(fig_bscan, use_container_width=True)
                except Exception as e:
                    st.error(f"绘制B扫描图像时出错：{str(e)}")
            
            with tab2:
                st.subheader("3D B扫描")
                try:
                    fig_3d = visualizer.plot_bscan_3d_interactive(
                        processor.bscan_data,
                        processor.time_axis,
                        processor.positions,
                        title="3D B扫描图像"
                    )
                    st.plotly_chart(fig_3d, use_container_width=True)
                except Exception as e:
                    st.error(f"绘制3D B扫描时出错：{str(e)}")
            
            with tab3:
                st.subheader("瀑布图")
                try:
                    fig_waterfall = visualizer.plot_waterfall_interactive(
                        processor.bscan_data,
                        processor.time_axis,
                        processor.positions,
                        title="瀑布图"
                    )
                    st.plotly_chart(fig_waterfall, use_container_width=True)
                except Exception as e:
                    st.error(f"绘制瀑布图时出错：{str(e)}")
            
            with tab4:
                st.subheader("信号切片分析")
                
                col_slice1, col_slice2 = st.columns(2)
                
                with col_slice1:
                    # 位置切片
                    position_idx = st.slider(
                        "选择位置索引", 
                        0, len(processor.positions)-1, 
                        len(processor.positions)//2,
                        key="position_slice"
                    )
                    position = processor.positions[position_idx]
                    
                    if st.button("📈 查看位置切片", use_container_width=True):
                        time_axis, signal = processor.get_signal_at_position(position_idx)
                        if time_axis is not None and signal is not None:
                            fig_position = visualizer.plot_signal_at_position_interactive(
                                time_axis, signal, position,
                                title=f"位置 {position} 处的信号"
                            )
                            st.plotly_chart(fig_position, use_container_width=True)
                        else:
                            st.warning("无法获取位置切片数据")
                
                with col_slice2:
                    # 时间切片
                    if processor.time_axis is not None:
                        time_idx = st.slider(
                            "选择时间索引", 
                            0, len(processor.time_axis)-1, 
                            len(processor.time_axis)//2,
                            key="time_slice"
                        )
                        time_val = processor.time_axis[time_idx]
                        
                        if st.button("📈 查看时间切片", use_container_width=True):
                            positions, signal = processor.get_signal_at_time(time_idx)
                            if positions is not None and signal is not None:
                                fig_time = visualizer.plot_signal_at_time_interactive(
                                    positions, signal, time_val,
                                    title=f"时间 {time_val:.6f} s 处的位置切片"
                                )
                                st.plotly_chart(fig_time, use_container_width=True)
                            else:
                                st.warning("无法获取时间切片数据")
        
        # 数据导出
        st.markdown("---")
        st.header("💾 数据导出")
        
        if st.button("📄 导出B扫描数据为MAT文件", use_container_width=True):
            output_path = "/tmp/bscan_data.mat"
            if processor.save_to_mat(output_path):
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 下载MAT文件",
                        data=file.read(),
                        file_name="bscan_data.mat",
                        mime="application/octet-stream",
                        use_container_width=True
                    )
            else:
                st.error("❌ MAT文件导出失败")
    
    else:
        # 如果没有加载数据，显示欢迎信息
        st.info("👋 欢迎使用B扫描信号处理模块！请在左侧加载数据文件夹或上传MAT文件开始使用。")
        
        # 显示支持的功能
        st.subheader("🌟 支持的功能")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **数据处理：**
            - 批量加载TXT信号文件
            - 从MAT文件加载B扫描数据
            - 多种滤波器批量应用
            - 信号归一化处理
            """)
        
        with col2:
            st.markdown("""
            **可视化功能：**
            - B扫描图像显示
            - 3D B扫描可视化
            - 瀑布图展示
            - 位置/时间切片分析
            - 数据导出功能
            """)

if __name__ == "__main__":
    module_b_page()