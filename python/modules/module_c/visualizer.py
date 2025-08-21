import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Tuple, List, Dict, Any, Optional, Union
import os
import sys
from matplotlib.animation import FuncAnimation
from matplotlib import cm

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class WaveFieldVisualizer:
    """
    波场数据可视化器，用于可视化波场数据
    """
    
    def __init__(self):
        """
        初始化波场数据可视化器
        """
        self.fig_size = (10, 8)  # 默认图形大小
        self.dpi = 100  # 默认DPI
        self.cmap = 'viridis'  # 默认颜色映射
        
    def plot_time_slice(self, time_slice: np.ndarray, x_axis: np.ndarray, y_axis: np.ndarray, 
                       time: float, title: str = None, 
                       xlabel: str = "X 位置", ylabel: str = "Y 位置", 
                       fig_size: Tuple[int, int] = None, 
                       show: bool = True) -> plt.Figure:
        """
        绘制时间切片
        
        Args:
            time_slice: 时间切片数据，形状为 (nx, ny)
            x_axis: x轴坐标
            y_axis: y轴坐标
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
            title = f"时间 {time:.6f} s 的波场切片"
            
        if fig_size is None:
            fig_size = self.fig_size
            
        fig, ax = plt.subplots(figsize=fig_size, dpi=self.dpi)
        
        # 创建网格
        X, Y = np.meshgrid(x_axis, y_axis, indexing='ij')
        
        # 绘制时间切片
        im = ax.pcolormesh(X, Y, time_slice, shading='gouraud', cmap=self.cmap)
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.colorbar(im, ax=ax, label='幅值')
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_time_slice_interactive(self, time_slice: np.ndarray, x_axis: np.ndarray, y_axis: np.ndarray, 
                                  time: float, title: str = None, 
                                  xlabel: str = "X 位置", ylabel: str = "Y 位置") -> go.Figure:
        """
        绘制交互式时间切片
        
        Args:
            time_slice: 时间切片数据，形状为 (nx, ny)
            x_axis: x轴坐标
            y_axis: y轴坐标
            time: 时间点
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        if title is None:
            title = f"时间 {time:.6f} s 的波场切片"
            
        fig = go.Figure(data=go.Heatmap(
            z=time_slice.T,  # 转置以匹配Plotly的坐标系
            x=x_axis,
            y=y_axis,
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
    
    def plot_energy_map(self, energy_map: np.ndarray, x_axis: np.ndarray, y_axis: np.ndarray, 
                      title: str = "能量图", 
                      xlabel: str = "X 位置", ylabel: str = "Y 位置", 
                      fig_size: Tuple[int, int] = None, 
                      show: bool = True) -> plt.Figure:
        """
        绘制能量图
        
        Args:
            energy_map: 能量图数据，形状为 (nx, ny)
            x_axis: x轴坐标
            y_axis: y轴坐标
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
        X, Y = np.meshgrid(x_axis, y_axis, indexing='ij')
        
        # 绘制能量图
        im = ax.pcolormesh(X, Y, energy_map, shading='gouraud', cmap=self.cmap)
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.colorbar(im, ax=ax, label='能量')
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_energy_map_interactive(self, energy_map: np.ndarray, x_axis: np.ndarray, y_axis: np.ndarray, 
                                 title: str = "能量图", 
                                 xlabel: str = "X 位置", ylabel: str = "Y 位置") -> go.Figure:
        """
        绘制交互式能量图
        
        Args:
            energy_map: 能量图数据，形状为 (nx, ny)
            x_axis: x轴坐标
            y_axis: y轴坐标
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        fig = go.Figure(data=go.Heatmap(
            z=energy_map.T,  # 转置以匹配Plotly的坐标系
            x=x_axis,
            y=y_axis,
            colorscale='Viridis',
            colorbar=dict(title='能量')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            height=600,
        )
        
        return fig
    
    def plot_max_amplitude_map(self, max_amplitude_map: np.ndarray, x_axis: np.ndarray, y_axis: np.ndarray, 
                             title: str = "最大幅值图", 
                             xlabel: str = "X 位置", ylabel: str = "Y 位置", 
                             fig_size: Tuple[int, int] = None, 
                             show: bool = True) -> plt.Figure:
        """
        绘制最大幅值图
        
        Args:
            max_amplitude_map: 最大幅值图数据，形状为 (nx, ny)
            x_axis: x轴坐标
            y_axis: y轴坐标
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
        X, Y = np.meshgrid(x_axis, y_axis, indexing='ij')
        
        # 绘制最大幅值图
        im = ax.pcolormesh(X, Y, max_amplitude_map, shading='gouraud', cmap=self.cmap)
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.colorbar(im, ax=ax, label='最大幅值')
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_arrival_time_map(self, arrival_time_map: np.ndarray, x_axis: np.ndarray, y_axis: np.ndarray, 
                            title: str = "到达时间图", 
                            xlabel: str = "X 位置", ylabel: str = "Y 位置", 
                            fig_size: Tuple[int, int] = None, 
                            show: bool = True) -> plt.Figure:
        """
        绘制到达时间图
        
        Args:
            arrival_time_map: 到达时间图数据，形状为 (nx, ny)
            x_axis: x轴坐标
            y_axis: y轴坐标
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
        X, Y = np.meshgrid(x_axis, y_axis, indexing='ij')
        
        # 绘制到达时间图
        im = ax.pcolormesh(X, Y, arrival_time_map, shading='gouraud', cmap='plasma')
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.colorbar(im, ax=ax, label='到达时间 (s)')
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def create_wave_propagation_animation(self, wave_data: np.ndarray, x_axis: np.ndarray, y_axis: np.ndarray, 
                                        time_axis: np.ndarray, interval: int = 50, 
                                        title: str = "波场传播动画", 
                                        xlabel: str = "X 位置", ylabel: str = "Y 位置", 
                                        fig_size: Tuple[int, int] = None) -> FuncAnimation:
        """
        创建波场传播动画
        
        Args:
            wave_data: 波场数据，形状为 (nx, ny, nt)
            x_axis: x轴坐标
            y_axis: y轴坐标
            time_axis: 时间轴
            interval: 帧间隔（毫秒）
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            fig_size: 图形大小
            
        Returns:
            FuncAnimation: Matplotlib动画对象
        """
        if fig_size is None:
            fig_size = self.fig_size
            
        fig, ax = plt.subplots(figsize=fig_size, dpi=self.dpi)
        
        # 创建网格
        X, Y = np.meshgrid(x_axis, y_axis, indexing='ij')
        
        # 获取数据范围
        vmin = np.min(wave_data)
        vmax = np.max(wave_data)
        
        # 初始帧
        im = ax.pcolormesh(X, Y, wave_data[:, :, 0], shading='gouraud', cmap=self.cmap, vmin=vmin, vmax=vmax)
        
        # 添加标题和标签
        ax.set_title(f"{title} - 时间: {time_axis[0]:.6f} s")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        # 添加颜色条
        fig.colorbar(im, ax=ax, label='幅值')
        
        # 更新函数
        def update(frame):
            im.set_array(wave_data[:, :, frame].flatten())
            ax.set_title(f"{title} - 时间: {time_axis[frame]:.6f} s")
            return [im]
        
        # 创建动画
        ani = FuncAnimation(fig, update, frames=len(time_axis), interval=interval, blit=True)
        
        plt.tight_layout()
        return ani
    
    def plot_surface_3d(self, data: np.ndarray, x_axis: np.ndarray, y_axis: np.ndarray, 
                      title: str, zlabel: str, 
                      xlabel: str = "X 位置", ylabel: str = "Y 位置", 
                      fig_size: Tuple[int, int] = None, 
                      show: bool = True) -> plt.Figure:
        """
        绘制3D表面图
        
        Args:
            data: 数据，形状为 (nx, ny)
            x_axis: x轴坐标
            y_axis: y轴坐标
            title: 图表标题
            zlabel: z轴标签
            xlabel: x轴标签
            ylabel: y轴标签
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if fig_size is None:
            fig_size = (12, 10)
            
        fig = plt.figure(figsize=fig_size, dpi=self.dpi)
        ax = fig.add_subplot(111, projection='3d')
        
        # 创建网格
        X, Y = np.meshgrid(x_axis, y_axis, indexing='ij')
        
        # 绘制3D表面
        surf = ax.plot_surface(X, Y, data, cmap=self.cmap, 
                             linewidth=0, antialiased=True, alpha=0.8)
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label=zlabel)
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_surface_3d_interactive(self, data: np.ndarray, x_axis: np.ndarray, y_axis: np.ndarray, 
                                 title: str, zlabel: str, 
                                 xlabel: str = "X 位置", ylabel: str = "Y 位置") -> go.Figure:
        """
        绘制交互式3D表面图
        
        Args:
            data: 数据，形状为 (nx, ny)
            x_axis: x轴坐标
            y_axis: y轴坐标
            title: 图表标题
            zlabel: z轴标签
            xlabel: x轴标签
            ylabel: y轴标签
            
        Returns:
            go.Figure: Plotly图形对象
        """
        fig = go.Figure(data=[go.Surface(
            z=data,
            x=x_axis,
            y=y_axis,
            colorscale='Viridis',
            colorbar=dict(title=zlabel)
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
    
    def plot_contour(self, data: np.ndarray, x_axis: np.ndarray, y_axis: np.ndarray, 
                    title: str, 
                    xlabel: str = "X 位置", ylabel: str = "Y 位置", 
                    fig_size: Tuple[int, int] = None, 
                    show: bool = True) -> plt.Figure:
        """
        绘制等高线图
        
        Args:
            data: 数据，形状为 (nx, ny)
            x_axis: x轴坐标
            y_axis: y轴坐标
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
        X, Y = np.meshgrid(x_axis, y_axis, indexing='ij')
        
        # 绘制等高线图
        contour = ax.contourf(X, Y, data, cmap=self.cmap, levels=20)
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.colorbar(contour, ax=ax)
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig
    
    def plot_multi_view(self, wave_data: np.ndarray, time_index: int, 
                       energy_map: np.ndarray, max_amplitude_map: np.ndarray, 
                       x_axis: np.ndarray, y_axis: np.ndarray, time_axis: np.ndarray, 
                       title: str = "多视图分析", 
                       fig_size: Tuple[int, int] = None, 
                       show: bool = True) -> plt.Figure:
        """
        绘制多视图分析
        
        Args:
            wave_data: 波场数据，形状为 (nx, ny, nt)
            time_index: 时间索引
            energy_map: 能量图数据，形状为 (nx, ny)
            max_amplitude_map: 最大幅值图数据，形状为 (nx, ny)
            x_axis: x轴坐标
            y_axis: y轴坐标
            time_axis: 时间轴
            title: 图表标题
            fig_size: 图形大小
            show: 是否显示图形
            
        Returns:
            plt.Figure: Matplotlib图形对象
        """
        if fig_size is None:
            fig_size = (15, 12)
            
        fig, axs = plt.subplots(2, 2, figsize=fig_size, dpi=self.dpi)
        
        # 创建网格
        X, Y = np.meshgrid(x_axis, y_axis, indexing='ij')
        
        # 绘制时间切片
        time_slice = wave_data[:, :, time_index]
        im1 = axs[0, 0].pcolormesh(X, Y, time_slice, shading='gouraud', cmap=self.cmap)
        axs[0, 0].set_title(f"时间 {time_axis[time_index]:.6f} s 的波场切片")
        axs[0, 0].set_xlabel("X 位置")
        axs[0, 0].set_ylabel("Y 位置")
        fig.colorbar(im1, ax=axs[0, 0], label='幅值')
        
        # 绘制能量图
        im2 = axs[0, 1].pcolormesh(X, Y, energy_map, shading='gouraud', cmap=self.cmap)
        axs[0, 1].set_title("能量图")
        axs[0, 1].set_xlabel("X 位置")
        axs[0, 1].set_ylabel("Y 位置")
        fig.colorbar(im2, ax=axs[0, 1], label='能量')
        
        # 绘制最大幅值图
        im3 = axs[1, 0].pcolormesh(X, Y, max_amplitude_map, shading='gouraud', cmap=self.cmap)
        axs[1, 0].set_title("最大幅值图")
        axs[1, 0].set_xlabel("X 位置")
        axs[1, 0].set_ylabel("Y 位置")
        fig.colorbar(im3, ax=axs[1, 0], label='最大幅值')
        
        # 绘制3D表面图（能量图）
        ax4 = fig.add_subplot(2, 2, 4, projection='3d')
        surf = ax4.plot_surface(X, Y, energy_map, cmap=self.cmap, 
                              linewidth=0, antialiased=True, alpha=0.8)
        ax4.set_title("能量图 (3D)")
        ax4.set_xlabel("X 位置")
        ax4.set_ylabel("Y 位置")
        ax4.set_zlabel("能量")
        
        fig.suptitle(title)
        
        if show:
            plt.tight_layout(rect=[0, 0, 1, 0.96])  # 为总标题留出空间
            plt.show()
            
        return fig
    
    def plot_multi_view_interactive(self, wave_data: np.ndarray, time_index: int, 
                                  energy_map: np.ndarray, max_amplitude_map: np.ndarray, 
                                  x_axis: np.ndarray, y_axis: np.ndarray, time_axis: np.ndarray, 
                                  title: str = "多视图分析") -> go.Figure:
        """
        绘制交互式多视图分析
        
        Args:
            wave_data: 波场数据，形状为 (nx, ny, nt)
            time_index: 时间索引
            energy_map: 能量图数据，形状为 (nx, ny)
            max_amplitude_map: 最大幅值图数据，形状为 (nx, ny)
            x_axis: x轴坐标
            y_axis: y轴坐标
            time_axis: 时间轴
            title: 图表标题
            
        Returns:
            go.Figure: Plotly图形对象
        """
        # 创建2x2子图
        fig = make_subplots(
            rows=2, cols=2,
            specs=[
                [{'type': 'heatmap'}, {'type': 'heatmap'}],
                [{'type': 'heatmap'}, {'type': 'surface'}]
            ],
            subplot_titles=(
                f"时间 {time_axis[time_index]:.6f} s 的波场切片",
                "能量图",
                "最大幅值图",
                "能量图 (3D)"
            ),
            vertical_spacing=0.1,
            horizontal_spacing=0.05
        )
        
        # 时间切片
        time_slice = wave_data[:, :, time_index]
        fig.add_trace(
            go.Heatmap(
                z=time_slice.T,
                x=x_axis,
                y=y_axis,
                colorscale='Viridis',
                colorbar=dict(title='幅值', len=0.4, y=0.8)
            ),
            row=1, col=1
        )
        
        # 能量图
        fig.add_trace(
            go.Heatmap(
                z=energy_map.T,
                x=x_axis,
                y=y_axis,
                colorscale='Viridis',
                colorbar=dict(title='能量', len=0.4, y=0.8)
            ),
            row=1, col=2
        )
        
        # 最大幅值图
        fig.add_trace(
            go.Heatmap(
                z=max_amplitude_map.T,
                x=x_axis,
                y=y_axis,
                colorscale='Viridis',
                colorbar=dict(title='最大幅值', len=0.4, y=0.2)
            ),
            row=2, col=1
        )
        
        # 3D能量图
        fig.add_trace(
            go.Surface(
                z=energy_map,
                x=x_axis,
                y=y_axis,
                colorscale='Viridis',
                colorbar=dict(title='能量', len=0.4, y=0.2)
            ),
            row=2, col=2
        )
        
        # 更新布局
        fig.update_layout(
            title=title,
            height=900,
            width=1000,
            scene=dict(
                xaxis_title="X 位置",
                yaxis_title="Y 位置",
                zaxis_title="能量"
            )
        )
        
        # 更新x轴和y轴标签
        fig.update_xaxes(title_text="X 位置", row=1, col=1)
        fig.update_xaxes(title_text="X 位置", row=1, col=2)
        fig.update_xaxes(title_text="X 位置", row=2, col=1)
        
        fig.update_yaxes(title_text="Y 位置", row=1, col=1)
        fig.update_yaxes(title_text="Y 位置", row=1, col=2)
        fig.update_yaxes(title_text="Y 位置", row=2, col=1)
        
        return fig