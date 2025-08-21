import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Tuple, List, Dict, Any, Optional, Union
import os
import sys

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class SinglePointVisualizer:
    """
    单点信号可视化器，用于可视化单点信号数据
    """
    
    def __init__(self):
        """
        初始化单点信号可视化器
        """
        self.fig_size = (10, 6)  # 默认图形大小
        self.dpi = 100  # 默认DPI
        self.cmap = 'viridis'  # 默认颜色映射
        
    def plot_signal(self, time: np.ndarray, signal: np.ndarray, title: str = "信号波形", 
                    xlabel: str = "时间 (s)", ylabel: str = "幅值", 
                    fig_size: Tuple[int, int] = None, show: bool = True) -> plt.Figure:
        """
        绘制信号波形
        
        Args:
            time: 时间轴
            signal: 信号数据
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if fig_size is None:
            fig_size = self.fig_size
            
        fig, ax = plt.subplots(figsize=fig_size, dpi=self.dpi)
        ax.plot(time, signal)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_signal_interactive(self, time: np.ndarray, signal: np.ndarray, 
                               title: str = "信号波形", 
                               xlabel: str = "时间 (s)", 
                               ylabel: str = "幅值") -> go.Figure:
        """
        绘制交互式信号波形
        
        Args:
            time: 时间轴
            signal: 信号数据
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time,
            y=signal,
            mode='lines',
            name='信号'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            hovermode="closest",
            height=500,
        )
        
        return fig
    
    def plot_fft(self, freq: np.ndarray, amplitude: np.ndarray, 
                title: str = "频谱", xlabel: str = "频率 (Hz)", 
                ylabel: str = "幅值", fig_size: Tuple[int, int] = None, 
                show: bool = True) -> plt.Figure:
        """
        绘制频谱
        
        Args:
            freq: 频率轴
            amplitude: 幅值
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if fig_size is None:
            fig_size = self.fig_size
            
        fig, ax = plt.subplots(figsize=fig_size, dpi=self.dpi)
        ax.plot(freq, amplitude)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_fft_interactive(self, freq: np.ndarray, amplitude: np.ndarray, 
                           title: str = "频谱", 
                           xlabel: str = "频率 (Hz)", 
                           ylabel: str = "幅值") -> go.Figure:
        """
        绘制交互式频谱
        
        Args:
            freq: 频率轴
            amplitude: 幅值
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=freq,
            y=amplitude,
            mode='lines',
            name='频谱'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            hovermode="closest",
            height=500,
        )
        
        return fig
    
    def plot_stft(self, f: np.ndarray, t: np.ndarray, Zxx: np.ndarray, 
                 title: str = "短时傅里叶变换", 
                 xlabel: str = "时间 (s)", 
                 ylabel: str = "频率 (Hz)", 
                 fig_size: Tuple[int, int] = None, 
                 show: bool = True) -> plt.Figure:
        """
        绘制短时傅里叶变换
        
        Args:
            f: 频率轴
            t: 时间轴
            Zxx: STFT结果
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if fig_size is None:
            fig_size = self.fig_size
            
        fig, ax = plt.subplots(figsize=fig_size, dpi=self.dpi)
        im = ax.pcolormesh(t, f, Zxx, shading='gouraud', cmap=self.cmap)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.colorbar(im, ax=ax, label='幅值')
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_stft_interactive(self, f: np.ndarray, t: np.ndarray, Zxx: np.ndarray, 
                            title: str = "短时傅里叶变换", 
                            xlabel: str = "时间 (s)", 
                            ylabel: str = "频率 (Hz)") -> go.Figure:
        """
        绘制交互式短时傅里叶变换
        
        Args:
            f: 频率轴
            t: 时间轴
            Zxx: STFT结果
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        fig = go.Figure(data=go.Heatmap(
            z=Zxx,
            x=t,
            y=f,
            colorscale='Viridis',
            colorbar=dict(title='幅值')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            height=600,
        )
        
        return fig
    
    def plot_signal_with_envelope(self, time: np.ndarray, signal: np.ndarray, 
                                 envelope: np.ndarray, 
                                 title: str = "信号与包络", 
                                 xlabel: str = "时间 (s)", 
                                 ylabel: str = "幅值", 
                                 fig_size: Tuple[int, int] = None, 
                                 show: bool = True) -> plt.Figure:
        """
        绘制信号与包络
        
        Args:
            time: 时间轴
            signal: 信号数据
            envelope: 包络数据
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if fig_size is None:
            fig_size = self.fig_size
            
        fig, ax = plt.subplots(figsize=fig_size, dpi=self.dpi)
        ax.plot(time, signal, label='信号')
        ax.plot(time, envelope, 'r-', label='包络')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        ax.legend()
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_signal_with_envelope_interactive(self, time: np.ndarray, signal: np.ndarray, 
                                            envelope: np.ndarray, 
                                            title: str = "信号与包络", 
                                            xlabel: str = "时间 (s)", 
                                            ylabel: str = "幅值") -> go.Figure:
        """
        绘制交互式信号与包络
        
        Args:
            time: 时间轴
            signal: 信号数据
            envelope: 包络数据
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time,
            y=signal,
            mode='lines',
            name='信号'
        ))
        fig.add_trace(go.Scatter(
            x=time,
            y=envelope,
            mode='lines',
            name='包络',
            line=dict(color='red')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            hovermode="closest",
            height=500,
            legend=dict(x=0.02, y=0.98)
        )
        
        return fig
    
    def plot_comparison(self, time: np.ndarray, original: np.ndarray, processed: np.ndarray, 
                       title: str = "原始信号与处理后信号对比", 
                       xlabel: str = "时间 (s)", 
                       ylabel: str = "幅值", 
                       fig_size: Tuple[int, int] = None, 
                       show: bool = True) -> plt.Figure:
        """
        绘制原始信号与处理后信号的对比图
        
        Args:
            time: 时间轴
            original: 原始信号
            processed: 处理后的信号
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if fig_size is None:
            fig_size = self.fig_size
            
        fig, ax = plt.subplots(figsize=fig_size, dpi=self.dpi)
        ax.plot(time, original, 'b-', alpha=0.7, label='原始信号')
        ax.plot(time, processed, 'r-', alpha=0.7, label='处理后信号')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        ax.legend()
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_comparison_interactive(self, time: np.ndarray, original: np.ndarray, processed: np.ndarray, 
                                  title: str = "原始信号与处理后信号对比", 
                                  xlabel: str = "时间 (s)", 
                                  ylabel: str = "幅值") -> go.Figure:
        """
        绘制交互式原始信号与处理后信号的对比图
        
        Args:
            time: 时间轴
            original: 原始信号
            processed: 处理后的信号
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time,
            y=original,
            mode='lines',
            name='原始信号',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=time,
            y=processed,
            mode='lines',
            name='处理后信号',
            line=dict(color='red')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            hovermode="closest",
            height=500,
            legend=dict(x=0.02, y=0.98)
        )
        
        return fig
    
    def plot_multi_view(self, time: np.ndarray, signal: np.ndarray, 
                       freq: np.ndarray, amplitude: np.ndarray, 
                       f: np.ndarray = None, t: np.ndarray = None, Zxx: np.ndarray = None, 
                       title: str = "多视图分析", 
                       fig_size: Tuple[int, int] = None, 
                       show: bool = True) -> plt.Figure:
        """
        绘制多视图分析（时域、频域、时频域）
        
        Args:
            time: 时间轴
            signal: 信号数据
            freq: 频率轴
            amplitude: 幅值
            f: STFT频率轴
            t: STFT时间轴
            Zxx: STFT结果
            title: 图表标题
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if fig_size is None:
            fig_size = (12, 10)
            
        if f is not None and t is not None and Zxx is not None:
            # 三视图：时域、频域、时频域
            fig, axs = plt.subplots(3, 1, figsize=fig_size, dpi=self.dpi)
            
            # 时域图
            axs[0].plot(time, signal)
            axs[0].set_title("时域信号")
            axs[0].set_xlabel("时间 (s)")
            axs[0].set_ylabel("幅值")
            axs[0].grid(True)
            
            # 频域图
            axs[1].plot(freq, amplitude)
            axs[1].set_title("频谱")
            axs[1].set_xlabel("频率 (Hz)")
            axs[1].set_ylabel("幅值")
            axs[1].grid(True)
            
            # 时频域图
            im = axs[2].pcolormesh(t, f, Zxx, shading='gouraud', cmap=self.cmap)
            axs[2].set_title("短时傅里叶变换")
            axs[2].set_xlabel("时间 (s)")
            axs[2].set_ylabel("频率 (Hz)")
            fig.colorbar(im, ax=axs[2], label='幅值')
        else:
            # 双视图：时域、频域
            fig, axs = plt.subplots(2, 1, figsize=fig_size, dpi=self.dpi)
            
            # 时域图
            axs[0].plot(time, signal)
            axs[0].set_title("时域信号")
            axs[0].set_xlabel("时间 (s)")
            axs[0].set_ylabel("幅值")
            axs[0].grid(True)
            
            # 频域图
            axs[1].plot(freq, amplitude)
            axs[1].set_title("频谱")
            axs[1].set_xlabel("频率 (Hz)")
            axs[1].set_ylabel("幅值")
            axs[1].grid(True)
        
        fig.suptitle(title)
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_multi_view_interactive(self, time: np.ndarray, signal: np.ndarray, 
                                  freq: np.ndarray, amplitude: np.ndarray, 
                                  f: np.ndarray = None, t: np.ndarray = None, Zxx: np.ndarray = None, 
                                  title: str = "多视图分析") -> go.Figure:
        """
        绘制交互式多视图分析（时域、频域、时频域）
        
        Args:
            time: 时间轴
            signal: 信号数据
            freq: 频率轴
            amplitude: 幅值
            f: STFT频率轴
            t: STFT时间轴
            Zxx: STFT结果
            title: 图表标题
            
        Returns:
            go.Figure: Plotly图形对象
        """
        if f is not None and t is not None and Zxx is not None:
            # 三视图：时域、频域、时频域
            fig = make_subplots(rows=3, cols=1, 
                              subplot_titles=("时域信号", "频谱", "短时傅里叶变换"),
                              vertical_spacing=0.1)
            
            # 时域图
            fig.add_trace(go.Scatter(
                x=time,
                y=signal,
                mode='lines',
                name='信号'
            ), row=1, col=1)
            
            # 频域图
            fig.add_trace(go.Scatter(
                x=freq,
                y=amplitude,
                mode='lines',
                name='频谱'
            ), row=2, col=1)
            
            # 时频域图
            fig.add_trace(go.Heatmap(
                z=Zxx,
                x=t,
                y=f,
                colorscale='Viridis',
                colorbar=dict(title='幅值', len=0.3, y=0.15),
                name='STFT'
            ), row=3, col=1)
        else:
            # 双视图：时域、频域
            fig = make_subplots(rows=2, cols=1, 
                              subplot_titles=("时域信号", "频谱"),
                              vertical_spacing=0.1)
            
            # 时域图
            fig.add_trace(go.Scatter(
                x=time,
                y=signal,
                mode='lines',
                name='信号'
            ), row=1, col=1)
            
            # 频域图
            fig.add_trace(go.Scatter(
                x=freq,
                y=amplitude,
                mode='lines',
                name='频谱'
            ), row=2, col=1)
        
        fig.update_layout(
            title=title,
            height=800,
            showlegend=True
        )
        
        # 更新x轴标签
        fig.update_xaxes(title_text="时间 (s)", row=1, col=1)
        fig.update_xaxes(title_text="频率 (Hz)", row=2, col=1)
        if f is not None and t is not None and Zxx is not None:
            fig.update_xaxes(title_text="时间 (s)", row=3, col=1)
        
        # 更新y轴标签
        fig.update_yaxes(title_text="幅值", row=1, col=1)
        fig.update_yaxes(title_text="幅值", row=2, col=1)
        if f is not None and t is not None and Zxx is not None:
            fig.update_yaxes(title_text="频率 (Hz)", row=3, col=1)
        
        return fig