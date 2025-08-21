import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
try:
    import streamlit as st
except ImportError:
    st = None
from typing import Tuple, List, Dict, Any, Optional, Union

class SinglePointVisualizer:
    """
    单点信号可视化器，用于创建各种信号显示图表
    """
    
    def __init__(self):
        """
        初始化可视化器
        """
        pass
    
    @staticmethod
    def plot_time_domain(time_axis: np.ndarray, signal: np.ndarray, 
                        title: str = "时域信号", 
                        xlabel: str = "时间 (s)", 
                        ylabel: str = "幅值",
                        use_plotly: bool = True) -> Any:
        """
        绘制时域信号
        
        Args:
            time_axis: 时间轴
            signal: 信号数据
            title: 图表标题
            xlabel: X轴标签
            ylabel: Y轴标签
            use_plotly: 是否使用Plotly（用于交互式图表）
            
        Returns:
            图表对象
        """
        if use_plotly:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=time_axis,
                y=signal,
                mode='lines',
                name='信号',
                line=dict(width=1)
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title=xlabel,
                yaxis_title=ylabel,
                hovermode='x unified',
                showlegend=False
            )
            
            return fig
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(time_axis, signal, linewidth=1)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.grid(True, alpha=0.3)
            return fig
    
    @staticmethod
    def plot_frequency_domain(frequencies: np.ndarray, magnitudes: np.ndarray,
                             title: str = "频域信号",
                             xlabel: str = "频率 (Hz)",
                             ylabel: str = "幅值",
                             use_plotly: bool = True) -> Any:
        """
        绘制频域信号
        
        Args:
            frequencies: 频率轴
            magnitudes: 幅值数据
            title: 图表标题
            xlabel: X轴标签
            ylabel: Y轴标签
            use_plotly: 是否使用Plotly
            
        Returns:
            图表对象
        """
        if use_plotly:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=frequencies,
                y=magnitudes,
                mode='lines',
                name='频谱',
                line=dict(width=1)
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title=xlabel,
                yaxis_title=ylabel,
                hovermode='x unified',
                showlegend=False
            )
            
            return fig
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(frequencies, magnitudes, linewidth=1)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.grid(True, alpha=0.3)
            return fig
    
    @staticmethod
    def plot_comparison(time_axis: np.ndarray, 
                       original_signal: np.ndarray, 
                       processed_signal: np.ndarray,
                       title: str = "信号对比",
                       use_plotly: bool = True) -> Any:
        """
        绘制原始信号与处理后信号的对比图
        
        Args:
            time_axis: 时间轴
            original_signal: 原始信号
            processed_signal: 处理后信号
            title: 图表标题
            use_plotly: 是否使用Plotly
            
        Returns:
            图表对象
        """
        if use_plotly:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=time_axis,
                y=original_signal,
                mode='lines',
                name='原始信号',
                line=dict(width=1, color='blue'),
                opacity=0.7
            ))
            
            fig.add_trace(go.Scatter(
                x=time_axis,
                y=processed_signal,
                mode='lines',
                name='处理后信号',
                line=dict(width=1, color='red')
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title="时间 (s)",
                yaxis_title="幅值",
                hovermode='x unified',
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            
            return fig
        else:
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(time_axis, original_signal, label='原始信号', alpha=0.7, linewidth=1)
            ax.plot(time_axis, processed_signal, label='处理后信号', linewidth=1)
            ax.set_title(title)
            ax.set_xlabel("时间 (s)")
            ax.set_ylabel("幅值")
            ax.legend()
            ax.grid(True, alpha=0.3)
            return fig
    
    @staticmethod
    def plot_stft(time_grid: np.ndarray, 
                  frequency_grid: np.ndarray, 
                  stft_magnitude: np.ndarray,
                  title: str = "短时傅里叶变换",
                  use_plotly: bool = True) -> Any:
        """
        绘制短时傅里叶变换（时频图）
        
        Args:
            time_grid: 时间网格
            frequency_grid: 频率网格
            stft_magnitude: STFT幅值
            title: 图表标题
            use_plotly: 是否使用Plotly
            
        Returns:
            图表对象
        """
        if use_plotly:
            fig = go.Figure(data=go.Heatmap(
                x=time_grid,
                y=frequency_grid,
                z=20 * np.log10(stft_magnitude + 1e-10),  # 转换为dB
                colorscale='Viridis',
                colorbar=dict(title="幅值 (dB)")
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title="时间 (s)",
                yaxis_title="频率 (Hz)"
            )
            
            return fig
        else:
            fig, ax = plt.subplots(figsize=(12, 8))
            im = ax.pcolormesh(time_grid, frequency_grid, 
                              20 * np.log10(stft_magnitude + 1e-10), 
                              shading='gouraud', cmap='viridis')
            ax.set_title(title)
            ax.set_xlabel("时间 (s)")
            ax.set_ylabel("频率 (Hz)")
            plt.colorbar(im, ax=ax, label="幅值 (dB)")
            return fig
    
    @staticmethod
    def plot_envelope(time_axis: np.ndarray, 
                     signal: np.ndarray, 
                     envelope: np.ndarray,
                     title: str = "信号包络",
                     use_plotly: bool = True) -> Any:
        """
        绘制信号及其包络
        
        Args:
            time_axis: 时间轴
            signal: 原始信号
            envelope: 信号包络
            title: 图表标题
            use_plotly: 是否使用Plotly
            
        Returns:
            图表对象
        """
        if use_plotly:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=time_axis,
                y=signal,
                mode='lines',
                name='信号',
                line=dict(width=1, color='lightblue'),
                opacity=0.6
            ))
            
            fig.add_trace(go.Scatter(
                x=time_axis,
                y=envelope,
                mode='lines',
                name='包络',
                line=dict(width=2, color='red')
            ))
            
            fig.add_trace(go.Scatter(
                x=time_axis,
                y=-envelope,
                mode='lines',
                name='负包络',
                line=dict(width=2, color='red'),
                showlegend=False
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title="时间 (s)",
                yaxis_title="幅值",
                hovermode='x unified',
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            
            return fig
        else:
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(time_axis, signal, label='信号', alpha=0.6, linewidth=1)
            ax.plot(time_axis, envelope, label='包络', linewidth=2, color='red')
            ax.plot(time_axis, -envelope, linewidth=2, color='red')
            ax.set_title(title)
            ax.set_xlabel("时间 (s)")
            ax.set_ylabel("幅值")
            ax.legend()
            ax.grid(True, alpha=0.3)
            return fig
    
    @staticmethod
    def create_dashboard(processor, use_plotly: bool = True) -> Dict[str, Any]:
        """
        创建信号处理仪表板
        
        Args:
            processor: 单点信号处理器实例
            use_plotly: 是否使用Plotly
            
        Returns:
            包含所有图表的字典
        """
        plots = {}
        
        if processor.signal_data is not None:
            # 时域信号对比
            plots['comparison'] = SinglePointVisualizer.plot_comparison(
                processor.time_axis,
                processor.signal_data,
                processor.processed_data,
                use_plotly=use_plotly
            )
            
            # 频域分析
            freqs, magnitudes = processor.compute_fft()
            if freqs is not None and magnitudes is not None:
                plots['frequency'] = SinglePointVisualizer.plot_frequency_domain(
                    freqs, magnitudes, use_plotly=use_plotly
                )
            
            # 信号包络
            envelope = processor.compute_envelope()
            if envelope is not None:
                plots['envelope'] = SinglePointVisualizer.plot_envelope(
                    processor.time_axis,
                    processor.processed_data,
                    envelope,
                    use_plotly=use_plotly
                )
            
            # 短时傅里叶变换
            f, t, Zxx = processor.compute_stft()
            if f is not None and t is not None and Zxx is not None:
                plots['stft'] = SinglePointVisualizer.plot_stft(
                    t, f, Zxx, use_plotly=use_plotly
                )
        
        return plots