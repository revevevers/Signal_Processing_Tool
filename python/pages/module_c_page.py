import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import scipy.io as sio
from typing import Tuple, List, Dict, Any, Optional, Union
import plotly.graph_objects as go
from matplotlib.animation import FuncAnimation
import io
import base64

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入模块
from modules.module_c import WaveFieldProcessor, WaveFieldVisualizer
from utils.file_utils import FileUtils

def app():
    """
    波场数据处理页面
    """
    st.title("波场数据处理")
    
    # 初始化处理器和可视化器
    processor = WaveFieldProcessor()
    visualizer = WaveFieldVisualizer()
    
    # 创建侧边栏
    with st.sidebar:
        st.header("参数设置")
        
        # 文件上传
        st.subheader("数据加载")
        uploaded_file = st.file_uploader("上传波场数据文件", type=["mat"])
        
        # 网格设置
        st.subheader("网格设置")
        auto_grid = st.checkbox("自动推断网格尺寸", True)
        if not auto_grid:
            nx = st.number_input("X方向网格点数", 10, 1000, 100, step=10)
            ny = st.number_input("Y方向网格点数", 10, 1000, 100, step=10)
            dx = st.number_input("X方向网格间距", 0.001, 1.0, 0.01, step=0.001, format="%.3f")
            dy = st.number_input("Y方向网格间距", 0.001, 1.0, 0.01, step=0.001, format="%.3f")
        
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
        
        # 数据处理选项
        st.subheader("数据处理选项")
        normalize = st.checkbox("归一化", True)
        compute_energy = st.checkbox("计算能量图", True)
        compute_max_amplitude = st.checkbox("计算最大幅值图", True)
        compute_arrival_time = st.checkbox("计算到达时间图", True)
        
        # 可视化选项
        st.subheader("可视化选项")
        plot_type = st.selectbox("图表类型", [
            "时间切片", 
            "能量图", 
            "最大幅值图", 
            "到达时间图", 
            "3D表面图", 
            "多视图分析"
        ])
        use_plotly = st.checkbox("使用交互式图表", True)
        
        if plot_type == "时间切片":
            time_index = st.slider("时间索引", 0, 1000, 500, key="time_slider")
        elif plot_type == "3D表面图":
            surface_data = st.selectbox("3D表面数据", ["能量图", "最大幅值图", "到达时间图"])
        
        # 保存选项
        st.subheader("保存选项")
        save_results = st.checkbox("保存处理结果", False)
        if save_results:
            save_path = st.text_input("保存路径", "processed_wavefield.mat")
        
        # 处理按钮
        process_button = st.button("处理波场数据")
    
    # 主内容区域
    if uploaded_file is not None:
        # 显示上传文件信息
        st.write(f"已上传文件: {uploaded_file.name}")
        
        # 保存上传的文件到临时位置
        file_path = os.path.join(os.path.dirname(__file__), "..\\temp", uploaded_file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 处理波场数据
        if process_button:
            with st.spinner("正在处理波场数据..."):
                # 加载数据
                if auto_grid:
                    processor.load_from_mat(file_path)
                else:
                    processor.load_from_mat(file_path, nx=nx, ny=ny, dx=dx, dy=dy)
                
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
                
                # 计算分析图
                if compute_energy:
                    processor.compute_energy_map()
                
                if compute_max_amplitude:
                    processor.compute_max_amplitude_map()
                
                if compute_arrival_time:
                    processor.compute_arrival_time_map()
                
                # 保存结果
                if save_results:
                    processor.save_to_mat(save_path)
                    st.success(f"处理结果已保存到 {save_path}")
                
                # 可视化结果
                st.subheader("处理结果")
                
                # 获取坐标轴
                x_axis = processor.x_axis
                y_axis = processor.y_axis
                time_axis = processor.time_axis
                
                if plot_type == "时间切片":
                    # 确保时间索引在有效范围内
                    max_time_idx = processor.wave_data.shape[2] - 1
                    time_index = min(time_index, max_time_idx)
                    
                    # 获取时间切片
                    time_slice = processor.get_time_slice(time_index)
                    
                    if use_plotly:
                        fig = visualizer.plot_time_slice_interactive(
                            time_slice, 
                            x_axis, 
                            y_axis, 
                            time_axis[time_index], 
                            title=f"时间 {time_axis[time_index]:.6f} s 的波场切片"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = visualizer.plot_time_slice(
                            time_slice, 
                            x_axis, 
                            y_axis, 
                            time_axis[time_index], 
                            title=f"时间 {time_axis[time_index]:.6f} s 的波场切片", 
                            show=False
                        )
                        st.pyplot(fig)
                
                elif plot_type == "能量图" and compute_energy:
                    if use_plotly:
                        fig = visualizer.plot_energy_map_interactive(
                            processor.energy_map, 
                            x_axis, 
                            y_axis, 
                            title="能量图"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = visualizer.plot_energy_map(
                            processor.energy_map, 
                            x_axis, 
                            y_axis, 
                            title="能量图", 
                            show=False
                        )
                        st.pyplot(fig)
                
                elif plot_type == "最大幅值图" and compute_max_amplitude:
                    if use_plotly:
                        fig = visualizer.plot_surface_3d_interactive(
                            processor.max_amplitude_map, 
                            x_axis, 
                            y_axis, 
                            title="最大幅值图", 
                            zlabel="最大幅值"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = visualizer.plot_max_amplitude_map(
                            processor.max_amplitude_map, 
                            x_axis, 
                            y_axis, 
                            title="最大幅值图", 
                            show=False
                        )
                        st.pyplot(fig)
                
                elif plot_type == "到达时间图" and compute_arrival_time:
                    if use_plotly:
                        fig = visualizer.plot_surface_3d_interactive(
                            processor.arrival_time_map, 
                            x_axis, 
                            y_axis, 
                            title="到达时间图", 
                            zlabel="到达时间 (s)"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = visualizer.plot_arrival_time_map(
                            processor.arrival_time_map, 
                            x_axis, 
                            y_axis, 
                            title="到达时间图", 
                            show=False
                        )
                        st.pyplot(fig)
                
                elif plot_type == "3D表面图":
                    if surface_data == "能量图" and compute_energy:
                        data = processor.energy_map
                        title = "能量图 (3D)"
                        zlabel = "能量"
                    elif surface_data == "最大幅值图" and compute_max_amplitude:
                        data = processor.max_amplitude_map
                        title = "最大幅值图 (3D)"
                        zlabel = "最大幅值"
                    elif surface_data == "到达时间图" and compute_arrival_time:
                        data = processor.arrival_time_map
                        title = "到达时间图 (3D)"
                        zlabel = "到达时间 (s)"
                    else:
                        st.warning(f"请先启用{surface_data}计算选项")
                        data = None
                    
                    if data is not None:
                        if use_plotly:
                            fig = visualizer.plot_surface_3d_interactive(
                                data, 
                                x_axis, 
                                y_axis, 
                                title=title, 
                                zlabel=zlabel
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            fig = visualizer.plot_surface_3d(
                                data, 
                                x_axis, 
                                y_axis, 
                                title=title, 
                                zlabel=zlabel, 
                                show=False
                            )
                            st.pyplot(fig)
                
                elif plot_type == "多视图分析":
                    # 确保所有需要的数据都已计算
                    if not compute_energy:
                        processor.compute_energy_map()
                    if not compute_max_amplitude:
                        processor.compute_max_amplitude_map()
                    
                    # 选择一个合适的时间索引
                    time_index = min(500, processor.wave_data.shape[2] - 1)
                    
                    if use_plotly:
                        fig = visualizer.plot_multi_view_interactive(
                            processor.wave_data, 
                            time_index, 
                            processor.energy_map, 
                            processor.max_amplitude_map, 
                            x_axis, 
                            y_axis, 
                            time_axis, 
                            title="多视图分析"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = visualizer.plot_multi_view(
                            processor.wave_data, 
                            time_index, 
                            processor.energy_map, 
                            processor.max_amplitude_map, 
                            x_axis, 
                            y_axis, 
                            time_axis, 
                            title="多视图分析", 
                            show=False
                        )
                        st.pyplot(fig)
                
                # 创建波场传播动画
                st.subheader("波场传播动画")
                
                # 创建动画（使用较少的帧数以提高性能）
                step = max(1, processor.wave_data.shape[2] // 50)
                ani = visualizer.create_wave_propagation_animation(
                    processor.wave_data[:, :, ::step], 
                    x_axis, 
                    y_axis, 
                    time_axis[::step], 
                    interval=100, 
                    title="波场传播动画"
                )
                
                # 将动画保存为GIF
                gif_path = os.path.join(os.path.dirname(__file__), "..\\temp", "wave_animation.gif")
                ani.save(gif_path, writer='pillow', fps=10)
                
                # 显示GIF
                with open(gif_path, "rb") as f:
                    gif_data = f.read()
                    b64 = base64.b64encode(gif_data).decode("utf-8")
                    html = f'<img src="data:image/gif;base64,{b64}" alt="波场传播动画" style="width:100%">'  
                    st.markdown(html, unsafe_allow_html=True)
                
                # 显示波场参数
                st.subheader("波场参数")
                st.write(f"采样率: {processor.fs} Hz")
                st.write(f"X方向网格点数: {processor.nx}")
                st.write(f"Y方向网格点数: {processor.ny}")
                st.write(f"X方向网格间距: {processor.dx:.6f}")
                st.write(f"Y方向网格间距: {processor.dy:.6f}")
                st.write(f"时间点数: {processor.nt}")
                st.write(f"信号持续时间: {processor.signal_duration:.6f} 秒")
                
                # 显示统计信息
                st.subheader("波场统计信息")
                stats_df = pd.DataFrame({
                    "参数": ["最大值", "最小值", "均值", "标准差"],
                    "值": [
                        f"{np.max(processor.wave_data):.6f}",
                        f"{np.min(processor.wave_data):.6f}",
                        f"{np.mean(processor.wave_data):.6f}",
                        f"{np.std(processor.wave_data):.6f}"
                    ]
                })
                st.table(stats_df)
    else:
        # 显示使用说明
        st.info("""
        ### 使用说明
        1. 在侧边栏上传MAT格式的波场数据文件
        2. 设置网格参数（或使用自动推断）
        3. 设置滤波器参数和数据处理选项
        4. 选择可视化方式
        5. 点击"处理波场数据"按钮进行处理和可视化
        
        ### 支持的数据格式
        - **MAT文件**: 包含波场数据的MATLAB数据文件，数据应为3D数组（nx × ny × nt）
        """)
        
        # 显示示例
        st.subheader("示例")
        
        # 创建示例波场数据
        nx, ny, nt = 50, 50, 100
        x = np.linspace(-1, 1, nx)
        y = np.linspace(-1, 1, ny)
        t = np.linspace(0, 0.1, nt)
        
        # 创建网格
        X, Y = np.meshgrid(x, y, indexing='ij')
        
        # 创建一个简单的波场（圆形波）
        wave_data = np.zeros((nx, ny, nt))
        source_x, source_y = 0, 0  # 波源位置
        velocity = 10  # 波速
        
        for i in range(nt):
            # 计算波前位置
            radius = velocity * t[i]
            # 创建圆形波
            distance = np.sqrt((X - source_x)**2 + (Y - source_y)**2)
            wave = np.exp(-((distance - radius) ** 2) / (2 * 0.05 ** 2)) * np.sin(20 * np.pi * distance)
            wave_data[:, :, i] = wave
        
        # 添加一些噪声
        wave_data += 0.05 * np.random.randn(*wave_data.shape)
        
        # 显示示例波场的一个时间切片
        time_idx = nt // 2
        fig, ax = plt.subplots(figsize=(8, 8))
        im = ax.pcolormesh(X, Y, wave_data[:, :, time_idx], shading='gouraud', cmap='viridis')
        plt.colorbar(im, ax=ax, label='幅值')
        ax.set_title(f"示例波场 - 时间 {t[time_idx]:.3f} s 的切片")
        ax.set_xlabel("X 位置")
        ax.set_ylabel("Y 位置")
        st.pyplot(fig)
        
        st.write("""
        上面显示的是一个示例波场数据的时间切片，展示了从中心点向外扩散的圆形波。
        请上传您自己的波场数据文件以开始处理。
        """)

if __name__ == "__main__":
    app()