import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Tuple, List, Dict, Any, Optional, Union
import os
import sys

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class BScanVisualizer:
    """
    B扫描信号可视化器，用于可视化B扫描数据
    """
    
    def __init__(self):
        """
        初始化B扫描信号可视化器
        """
        self.fig_size = (10, 6)  # 默认图形大小
        self.dpi = 100  # 默认DPI
        self.cmap = 'viridis'  # 默认颜色映射
        
    def plot_bscan(self, bscan_data: np.ndarray, time_axis: np.ndarray, positions: List[float], 
                  title: str = "B扫描图像", 
                  xlabel: str = "时间 (s)", 
                  ylabel: str = "位置", 
                  fig_size: Tuple[int, int] = None, 
                  show: bool = True) -> plt.Figure:
        """
        绘制B扫描图像
        
        Args:
            bscan_data: B扫描数据，形状为 (位置数, 时间点数)
            time_axis: 时间轴
            positions: 位置列表
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
        
        # 创建网格
        X, Y = np.meshgrid(time_axis, positions)
        
        # 绘制B扫描图像
        im = ax.pcolormesh(X, Y, bscan_data, shading='gouraud', cmap=self.cmap)
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.colorbar(im, ax=ax, label='幅值')
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_bscan_interactive(self, bscan_data: np.ndarray, time_axis: np.ndarray, positions: List[float], 
                             title: str = "B扫描图像", 
                             xlabel: str = "时间 (s)", 
                             ylabel: str = "位置") -> go.Figure:
        """
        绘制交互式B扫描图像
        
        Args:
            bscan_data: B扫描数据，形状为 (位置数, 时间点数)
            time_axis: 时间轴
            positions: 位置列表
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        fig = go.Figure(data=go.Heatmap(
            z=bscan_data,
            x=time_axis,
            y=positions,
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
    
    def plot_signal_at_position(self, time_axis: np.ndarray, signal: np.ndarray, position: float, 
                              title: str = None, 
                              xlabel: str = "时间 (s)", 
                              ylabel: str = "幅值", 
                              fig_size: Tuple[int, int] = None, 
                              show: bool = True) -> plt.Figure:
        """
        绘制指定位置的信号
        
        Args:
            time_axis: 时间轴
            signal: 信号数据
            position: 位置
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if title is None:
            title = f"位置 {position} 处的信号"
            
        if fig_size is None:
            fig_size = self.fig_size
            
        fig, ax = plt.subplots(figsize=fig_size, dpi=self.dpi)
        ax.plot(time_axis, signal)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_signal_at_position_interactive(self, time_axis: np.ndarray, signal: np.ndarray, position: float, 
                                         title: str = None, 
                                         xlabel: str = "时间 (s)", 
                                         ylabel: str = "幅值") -> go.Figure:
        """
        绘制交互式指定位置的信号
        
        Args:
            time_axis: 时间轴
            signal: 信号数据
            position: 位置
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        if title is None:
            title = f"位置 {position} 处的信号"
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_axis,
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
    
    def plot_waterfall(self, bscan_data: np.ndarray, time_axis: np.ndarray, positions: List[float], 
                      title: str = "瀑布图", 
                      xlabel: str = "时间 (s)", 
                      zlabel: str = "幅值", 
                      ylabel: str = "位置", 
                      fig_size: Tuple[int, int] = None, 
                      show: bool = True) -> plt.Figure:
        """
        绘制瀑布图
        
        Args:
            bscan_data: B扫描数据，形状为 (位置数, 时间点数)
            time_axis: 时间轴
            positions: 位置列表
            title: 图表标题
            xlabel: x轴标签
            zlabel: z轴标签
            ylabel: y轴标签
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if fig_size is None:
            fig_size = (12, 8)
            
        fig = plt.figure(figsize=fig_size, dpi=self.dpi)
        ax = fig.add_subplot(111, projection='3d')
        
        # 创建网格
        X, Y = np.meshgrid(time_axis, positions)
        
        # 绘制瀑布图
        for i, position in enumerate(positions):
            ax.plot(time_axis, np.ones_like(time_axis) * position, bscan_data[i], 
                   alpha=0.7, color=plt.cm.viridis(i / len(positions)))
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_waterfall_interactive(self, bscan_data: np.ndarray, time_axis: np.ndarray, positions: List[float], 
                                 title: str = "瀑布图", 
                                 xlabel: str = "时间 (s)", 
                                 zlabel: str = "幅值", 
                                 ylabel: str = "位置") -> go.Figure:
        """
        绘制交互式瀑布图
        
        Args:
            bscan_data: B扫描数据，形状为 (位置数, 时间点数)
            time_axis: 时间轴
            positions: 位置列表
            title: 图表标题
            xlabel: x轴标签
            zlabel: z轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        fig = go.Figure()
        
        # 为每个位置添加一条线
        for i, position in enumerate(positions):
            fig.add_trace(go.Scatter3d(
                x=time_axis,
                y=np.ones_like(time_axis) * position,
                z=bscan_data[i],
                mode='lines',
                name=f'位置 {position}',
                line=dict(
                    color=f'rgba({int(255 * i / len(positions))}, {int(255 * (1 - i / len(positions)))}, 255, 0.7)',
                    width=2
                )
            ))
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title=xlabel,
                yaxis_title=ylabel,
                zaxis_title=zlabel,
            ),
            height=700,
            margin=dict(l=0, r=0, b=0, t=30),
        )
        
        return fig
    
    def plot_bscan_3d(self, bscan_data: np.ndarray, time_axis: np.ndarray, positions: List[float], 
                     title: str = "3D B扫描图像", 
                     xlabel: str = "时间 (s)", 
                     ylabel: str = "位置", 
                     zlabel: str = "幅值", 
                     fig_size: Tuple[int, int] = None, 
                     show: bool = True) -> plt.Figure:
        """
        绘制3D B扫描图像
        
        Args:
            bscan_data: B扫描数据，形状为 (位置数, 时间点数)
            time_axis: 时间轴
            positions: 位置列表
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            zlabel: z轴标签
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if fig_size is None:
            fig_size = (12, 8)
            
        fig = plt.figure(figsize=fig_size, dpi=self.dpi)
        ax = fig.add_subplot(111, projection='3d')
        
        # 创建网格
        X, Y = np.meshgrid(time_axis, positions)
        
        # 绘制3D表面
        surf = ax.plot_surface(X, Y, bscan_data, cmap=self.cmap, 
                             linewidth=0, antialiased=True, alpha=0.8)
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='幅值')
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_bscan_3d_interactive(self, bscan_data: np.ndarray, time_axis: np.ndarray, positions: List[float], 
                                title: str = "3D B扫描图像", 
                                xlabel: str = "时间 (s)", 
                                ylabel: str = "位置", 
                                zlabel: str = "幅值") -> go.Figure:
        """
        绘制交互式3D B扫描图像
        
        Args:
            bscan_data: B扫描数据，形状为 (位置数, 时间点数)
            time_axis: 时间轴
            positions: 位置列表
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            zlabel: z轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        fig = go.Figure(data=[go.Surface(
            z=bscan_data,
            x=time_axis,
            y=positions,
            colorscale='Viridis',
            colorbar=dict(title='幅值')
        )])
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title=xlabel,
                yaxis_title=ylabel,
                zaxis_title=zlabel,
            ),
            height=700,
            margin=dict(l=0, r=0, b=0, t=30),
        )
        
        return fig
    
    def plot_signal_at_time(self, positions: List[float], signal: np.ndarray, time: float, 
                          title: str = None, 
                          xlabel: str = "位置", 
                          ylabel: str = "幅值", 
                          fig_size: Tuple[int, int] = None, 
                          show: bool = True) -> plt.Figure:
        """
        绘制指定时间点的位置切片
        
        Args:
            positions: 位置列表
            signal: 信号数据
            time: 时间点
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if title is None:
            title = f"时间 {time:.6f} s 处的位置切片"
            
        if fig_size is None:
            fig_size = self.fig_size
            
        fig, ax = plt.subplots(figsize=fig_size, dpi=self.dpi)
        ax.plot(positions, signal)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_signal_at_time_interactive(self, positions: List[float], signal: np.ndarray, time: float, 
                                     title: str = None, 
                                     xlabel: str = "位置", 
                                     ylabel: str = "幅值") -> go.Figure:
        """
        绘制交互式指定时间点的位置切片
        
        Args:
            positions: 位置列表
            signal: 信号数据
            time: 时间点
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        if title is None:
            title = f"时间 {time:.6f} s 处的位置切片"
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=positions,
            y=signal,
            mode='lines+markers',
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