import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import scipy.io as sio
from typing import Tuple, List, Dict, Any, Optional, Union
import plotly.graph_objects as go

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入模块
from modules.module_a import SinglePointProcessor, SinglePointVisualizer
from utils.file_utils import FileUtils

def app():
    """
    单点信号处理页面
    """
    st.title("单点信号处理")
    
    # 初始化处理器和可视化器
    processor = SinglePointProcessor()
    visualizer = SinglePointVisualizer()
    
    # 创建侧边栏
    with st.sidebar:
        st.header("参数设置")
        
        # 文件上传
        uploaded_file = st.file_uploader("上传信号文件", type=["txt", "mat"])
        
        # 滤波器设置
        st.subheader("滤波器设置")
        filter_type = st.selectbox("滤波器类型", ["带通滤波", "低通滤波", "高通滤波", "中值滤波", "Savitzky-Golay滤波"])
        
        if filter_type in ["带通滤波", "低通滤波", "高通滤波"]:
            order = st.slider("滤波器阶数", 1, 10, 4)
            if filter_type == "带通滤波":
                low_freq = st.number_input("低截止频率 (Hz)", 0.0, 1000000.0, 10000.0, step=1000.0)
                high_freq = st.number_input("高截止频率 (Hz)", 0.0, 1000000.0, 100000.0, step=1000.0)
            elif filter_type == "低通滤波":
                cutoff_freq = st.number_input("截止频率 (Hz)", 0.0, 1000000.0, 100000.0, step=1000.0)
            elif filter_type == "高通滤波":
                cutoff_freq = st.number_input("截止频率 (Hz)", 0.0, 1000000.0, 10000.0, step=1000.0)
        elif filter_type == "中值滤波":
            window_size = st.slider("窗口大小", 3, 51, 5, step=2)
        elif filter_type == "Savitzky-Golay滤波":
            window_size = st.slider("窗口大小", 5, 51, 11, step=2)
            poly_order = st.slider("多项式阶数", 1, 5, 3)
        
        # 其他处理选项
        st.subheader("其他处理选项")
        normalize = st.checkbox("归一化", True)
        compute_envelope = st.checkbox("计算包络", True)
        envelope_method = st.selectbox("包络计算方法", ["希尔伯特变换", "峰值检测"])
        
        # 可视化选项
        st.subheader("可视化选项")
        plot_type = st.selectbox("图表类型", ["时域波形", "频谱", "短时傅里叶变换", "信号与包络", "原始信号与处理后信号对比", "多视图分析"])
        use_plotly = st.checkbox("使用交互式图表", True)
        
        # 保存选项
        st.subheader("保存选项")
        save_results = st.checkbox("保存处理结果", False)
        if save_results:
            save_path = st.text_input("保存路径", "processed_signal.mat")
        
        # 处理按钮
        process_button = st.button("处理信号")
    
    # 主内容区域
    if uploaded_file is not None:
        # 显示上传文件信息
        st.write(f"已上传文件: {uploaded_file.name}")
        
        # 保存上传的文件到临时位置
        file_path = os.path.join(os.path.dirname(__file__), "..\\temp", uploaded_file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 处理信号
        if process_button:
            with st.spinner("正在处理信号..."):
                # 加载信号
                if uploaded_file.name.endswith(".txt"):
                    processor.load_from_txt(file_path)
                elif uploaded_file.name.endswith(".mat"):
                    processor.load_from_mat(file_path)
                
                # 应用滤波器
                if filter_type == "带通滤波":
                    processor.apply_bandpass_filter(low_freq, high_freq, order)
                elif filter_type == "低通滤波":
                    processor.apply_lowpass_filter(cutoff_freq, order)
                elif filter_type == "高通滤波":
                    processor.apply_highpass_filter(cutoff_freq, order)
                elif filter_type == "中值滤波":
                    processor.apply_median_filter(window_size)
                elif filter_type == "Savitzky-Golay滤波":
                    processor.apply_savgol_filter(window_size, poly_order)
                
                # 归一化
                if normalize:
                    processor.normalize()
                
                # 计算包络
                if compute_envelope:
                    if envelope_method == "希尔伯特变换":
                        processor.compute_envelope(method="hilbert")
                    else:
                        processor.compute_envelope(method="peak")
                
                # 计算FFT和STFT
                processor.compute_fft()
                processor.compute_stft()
                
                # 保存结果
                if save_results:
                    processor.save_to_mat(save_path)
                    st.success(f"处理结果已保存到 {save_path}")
                
                # 可视化结果
                st.subheader("处理结果")
                
                if plot_type == "时域波形":
                    if use_plotly:
                        fig = visualizer.plot_waveform_interactive(
                            processor.signal, 
                            processor.time_axis, 
                            title="信号波形"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = visualizer.plot_waveform(
                            processor.signal, 
                            processor.time_axis, 
                            title="信号波形", 
                            show=False
                        )
                        st.pyplot(fig)
                
                elif plot_type == "频谱":
                    if use_plotly:
                        fig = visualizer.plot_spectrum_interactive(
                            processor.fft_magnitude, 
                            processor.freq_axis, 
                            title="信号频谱"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = visualizer.plot_spectrum(
                            processor.fft_magnitude, 
                            processor.freq_axis, 
                            title="信号频谱", 
                            show=False
                        )
                        st.pyplot(fig)
                
                elif plot_type == "短时傅里叶变换":
                    if use_plotly:
                        fig = visualizer.plot_stft_interactive(
                            processor.stft_magnitude, 
                            processor.time_axis, 
                            processor.stft_freq_axis, 
                            title="短时傅里叶变换"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = visualizer.plot_stft(
                            processor.stft_magnitude, 
                            processor.time_axis, 
                            processor.stft_freq_axis, 
                            title="短时傅里叶变换", 
                            show=False
                        )
                        st.pyplot(fig)
                
                elif plot_type == "信号与包络":
                    if compute_envelope:
                        if use_plotly:
                            fig = visualizer.plot_signal_and_envelope_interactive(
                                processor.signal, 
                                processor.envelope, 
                                processor.time_axis, 
                                title="信号与包络"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            fig = visualizer.plot_signal_and_envelope(
                                processor.signal, 
                                processor.envelope, 
                                processor.time_axis, 
                                title="信号与包络", 
                                show=False
                            )
                            st.pyplot(fig)
                    else:
                        st.warning("请先启用包络计算选项")
                
                elif plot_type == "原始信号与处理后信号对比":
                    if use_plotly:
                        fig = visualizer.plot_original_vs_processed_interactive(
                            processor.original_signal, 
                            processor.signal, 
                            processor.time_axis, 
                            title="原始信号与处理后信号对比"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = visualizer.plot_original_vs_processed(
                            processor.original_signal, 
                            processor.signal, 
                            processor.time_axis, 
                            title="原始信号与处理后信号对比", 
                            show=False
                        )
                        st.pyplot(fig)
                
                elif plot_type == "多视图分析":
                    if use_plotly:
                        fig = visualizer.plot_multi_view_interactive(
                            processor.signal, 
                            processor.time_axis, 
                            processor.fft_magnitude, 
                            processor.freq_axis, 
                            processor.stft_magnitude, 
                            processor.stft_freq_axis, 
                            title="多视图分析"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = visualizer.plot_multi_view(
                            processor.signal, 
                            processor.time_axis, 
                            processor.fft_magnitude, 
                            processor.freq_axis, 
                            processor.stft_magnitude, 
                            processor.stft_freq_axis, 
                            title="多视图分析", 
                            show=False
                        )
                        st.pyplot(fig)
                
                # 显示信号参数
                st.subheader("信号参数")
                st.write(f"采样率: {processor.fs} Hz")
                st.write(f"信号长度: {len(processor.signal)} 点")
                st.write(f"信号持续时间: {processor.signal_duration:.6f} 秒")
                
                # 显示信号统计信息
                st.subheader("信号统计信息")
                stats_df = pd.DataFrame({
                    "参数": ["最大值", "最小值", "均值", "标准差", "RMS", "峰峰值"],
                    "原始信号": [
                        f"{np.max(processor.original_signal):.6f}",
                        f"{np.min(processor.original_signal):.6f}",
                        f"{np.mean(processor.original_signal):.6f}",
                        f"{np.std(processor.original_signal):.6f}",
                        f"{np.sqrt(np.mean(np.square(processor.original_signal))):.6f}",
                        f"{np.max(processor.original_signal) - np.min(processor.original_signal):.6f}"
                    ],
                    "处理后信号": [
                        f"{np.max(processor.signal):.6f}",
                        f"{np.min(processor.signal):.6f}",
                        f"{np.mean(processor.signal):.6f}",
                        f"{np.std(processor.signal):.6f}",
                        f"{np.sqrt(np.mean(np.square(processor.signal))):.6f}",
                        f"{np.max(processor.signal) - np.min(processor.signal):.6f}"
                    ]
                })
                st.table(stats_df)
    else:
        # 显示使用说明
        st.info("""
        ### 使用说明
        1. 在侧边栏上传TXT或MAT格式的信号文件
        2. 设置滤波器参数和其他处理选项
        3. 选择可视化方式
        4. 点击"处理信号"按钮进行处理和可视化
        
        ### 支持的文件格式
        - **TXT文件**: 每行一个数据点，第一行可以包含采样率信息
        - **MAT文件**: 包含信号数据和采样率的MATLAB数据文件
        """)
        
        # 显示示例
        st.subheader("示例")
        
        # 创建示例信号
        t = np.linspace(0, 0.1, 1000)
        f1, f2 = 50, 120
        signal = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t) + 0.2 * np.random.randn(len(t))
        
        # 显示示例信号
        fig = plt.figure(figsize=(10, 4))
        plt.plot(t, signal)
        plt.title("示例信号")
        plt.xlabel("时间 (s)")
        plt.ylabel("幅值")
        plt.grid(True)
        st.pyplot(fig)
        
        st.write("""
        上面显示的是一个示例信号，包含50Hz和120Hz的正弦波以及随机噪声。
        上传您自己的信号文件以开始处理。
        """)

if __name__ == "__main__":
    app()