import numpy as np
import pandas as pd
from scipy import signal
from typing import Tuple, List, Dict, Any, Optional, Union
import os
import sys
import math

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.signal_utils import SignalUtils
from utils.file_utils import FileUtils

class WaveFieldProcessor:
    """
    波场数据处理器，用于处理波场数据
    """
    
    def __init__(self):
        """
        初始化波场数据处理器
        """
        self.wave_data = None  # 原始波场数据，形状为 (nx, ny, nt)
        self.processed_data = None  # 处理后的波场数据
        self.sampling_rate = None  # 采样率
        self.time_axis = None  # 时间轴
        self.nx = None  # x方向网格点数
        self.ny = None  # y方向网格点数
        self.nt = None  # 时间点数
        self.dx = 1.0  # x方向网格间距
        self.dy = 1.0  # y方向网格间距
        self.x_axis = None  # x轴坐标
        self.y_axis = None  # y轴坐标
        self.file_path = None  # 文件路径
        self.energy_map = None  # 能量图
        self.max_amplitude_map = None  # 最大幅值图
        self.arrival_time_map = None  # 到达时间图
        self.signal_utils = SignalUtils()  # 信号处理工具
        self.file_utils = FileUtils()  # 文件处理工具
        
    def load_from_mat(self, file_path: str, data_key: str = 'wave_data', 
                     fs_key: str = 'fs', auto_infer_grid: bool = True) -> bool:
        """
        从MAT文件加载波场数据
        
        Args:
            file_path: 文件路径
            data_key: 波场数据的键名
            fs_key: 采样率的键名
            auto_infer_grid: 是否自动推断网格尺寸
            
        Returns:
            bool: 是否成功加载
        """
        try:
            self.file_path = file_path
            # 使用FileUtils加载MAT文件
            data_dict = self.file_utils.load_from_mat(file_path)
            
            if data_dict is not None and data_key in data_dict:
                wave_data = data_dict[data_key]
                
                # 检查数据维度
                if len(wave_data.shape) == 3:
                    # 3D数据：(nx, ny, nt)
                    self.wave_data = wave_data
                    self.nx, self.ny, self.nt = wave_data.shape
                elif len(wave_data.shape) == 2:
                    # 2D数据：(n_positions, nt)，需要转换为3D
                    if auto_infer_grid:
                        # 尝试推断网格尺寸
                        n_positions, self.nt = wave_data.shape
                        self.nx = int(math.sqrt(n_positions))
                        self.ny = n_positions // self.nx
                        
                        if self.nx * self.ny != n_positions:
                            # 如果不是完美的正方形，尝试其他因子
                            factors = []
                            for i in range(1, int(math.sqrt(n_positions)) + 1):
                                if n_positions % i == 0:
                                    factors.append((i, n_positions // i))
                            
                            # 选择最接近正方形的因子对
                            if factors:
                                best_factor = min(factors, key=lambda x: abs(x[0] - x[1]))
                                self.nx, self.ny = best_factor
                        
                        # 重塑数据为3D
                        self.wave_data = wave_data.reshape(self.nx, self.ny, self.nt)
                    else:
                        print("2D数据需要手动设置网格尺寸")
                        return False
                else:
                    print(f"不支持的数据维度: {len(wave_data.shape)}")
                    return False
                
                # 初始化处理后的数据为原始数据
                self.processed_data = self.wave_data.copy()
                
                # 获取采样率
                if fs_key in data_dict:
                    self.sampling_rate = data_dict[fs_key]
                else:
                    # 默认采样率
                    self.sampling_rate = 1.0
                    print("警告：MAT文件中未找到采样率信息，使用默认值1.0")
                
                # 创建时间轴
                self.time_axis = np.arange(self.nt) / self.sampling_rate
                
                # 创建空间轴
                self.x_axis = np.arange(self.nx) * self.dx
                self.y_axis = np.arange(self.ny) * self.dy
                
                print(f"成功加载波场数据，形状为 ({self.nx}, {self.ny}, {self.nt})")
                return True
            else:
                print(f"MAT文件 {file_path} 中未找到键 '{data_key}'")
                return False
        except Exception as e:
            print(f"加载MAT文件 {file_path} 时出错: {str(e)}")
            return False
    
    def set_grid_size(self, dx: float, dy: float) -> None:
        """
        设置网格尺寸
        
        Args:
            dx: x方向网格间距
            dy: y方向网格间距
        """
        self.dx = dx
        self.dy = dy
        
        # 更新空间轴
        if self.nx is not None and self.ny is not None:
            self.x_axis = np.arange(self.nx) * self.dx
            self.y_axis = np.arange(self.ny) * self.dy
    
    def reset_processing(self) -> None:
        """
        重置处理，将处理后的数据恢复为原始数据
        """
        if self.wave_data is not None:
            self.processed_data = self.wave_data.copy()
            # 清除分析结果
            self.energy_map = None
            self.max_amplitude_map = None
            self.arrival_time_map = None
    
    def apply_bandpass_filter(self, lowcut: float, highcut: float, order: int = 4) -> None:
        """
        应用带通滤波器
        
        Args:
            lowcut: 低截止频率
            highcut: 高截止频率
            order: 滤波器阶数
        """
        if self.processed_data is not None and self.sampling_rate is not None:
            # 对每个空间点的时间序列应用滤波器
            for i in range(self.nx):
                for j in range(self.ny):
                    self.processed_data[i, j, :] = SignalUtils.apply_bandpass_filter(
                        self.processed_data[i, j, :], lowcut, highcut, self.sampling_rate, order
                    )
            # 清除分析结果
            self.energy_map = None
            self.max_amplitude_map = None
            self.arrival_time_map = None
    
    def apply_lowpass_filter(self, cutoff: float, order: int = 4) -> None:
        """
        应用低通滤波器
        
        Args:
            cutoff: 截止频率
            order: 滤波器阶数
        """
        if self.processed_data is not None and self.sampling_rate is not None:
            # 对每个空间点的时间序列应用滤波器
            for i in range(self.nx):
                for j in range(self.ny):
                    self.processed_data[i, j, :] = SignalUtils.apply_lowpass_filter(
                        self.processed_data[i, j, :], cutoff, self.sampling_rate, order
                    )
            # 清除分析结果
            self.energy_map = None
            self.max_amplitude_map = None
            self.arrival_time_map = None
    
    def apply_highpass_filter(self, cutoff: float, order: int = 4) -> None:
        """
        应用高通滤波器
        
        Args:
            cutoff: 截止频率
            order: 滤波器阶数
        """
        if self.processed_data is not None and self.sampling_rate is not None:
            # 对每个空间点的时间序列应用滤波器
            for i in range(self.nx):
                for j in range(self.ny):
                    self.processed_data[i, j, :] = SignalUtils.apply_highpass_filter(
                        self.processed_data[i, j, :], cutoff, self.sampling_rate, order
                    )
            # 清除分析结果
            self.energy_map = None
            self.max_amplitude_map = None
            self.arrival_time_map = None
    
    def apply_median_filter(self, kernel_size: int = 5) -> None:
        """
        应用中值滤波器
        
        Args:
            kernel_size: 核大小
        """
        if self.processed_data is not None:
            # 对每个空间点的时间序列应用滤波器
            for i in range(self.nx):
                for j in range(self.ny):
                    self.processed_data[i, j, :] = SignalUtils.apply_median_filter(
                        self.processed_data[i, j, :], kernel_size
                    )
            # 清除分析结果
            self.energy_map = None
            self.max_amplitude_map = None
            self.arrival_time_map = None
    
    def apply_savgol_filter(self, window_length: int = 11, polyorder: int = 3) -> None:
        """
        应用Savitzky-Golay滤波器
        
        Args:
            window_length: 窗口长度
            polyorder: 多项式阶数
        """
        if self.processed_data is not None:
            # 对每个空间点的时间序列应用滤波器
            for i in range(self.nx):
                for j in range(self.ny):
                    self.processed_data[i, j, :] = SignalUtils.apply_savgol_filter(
                        self.processed_data[i, j, :], window_length, polyorder
                    )
            # 清除分析结果
            self.energy_map = None
            self.max_amplitude_map = None
            self.arrival_time_map = None
    
    def normalize_data(self) -> None:
        """
        归一化波场数据
        """
        if self.processed_data is not None:
            # 全局归一化
            max_val = np.max(np.abs(self.processed_data))
            if max_val > 0:
                self.processed_data = self.processed_data / max_val
    
    def get_time_slice(self, time_index: int) -> np.ndarray:
        """
        获取指定时间点的空间切片
        
        Args:
            time_index: 时间索引
            
        Returns:
            np.ndarray: 空间切片，形状为 (nx, ny)
        """
        if self.processed_data is not None and time_index >= 0 and time_index < self.nt:
            return self.processed_data[:, :, time_index]
        else:
            print(f"时间索引 {time_index} 超出范围")
            return None
    
    def compute_energy_map(self) -> np.ndarray:
        """
        计算能量图
        
        Returns:
            np.ndarray: 能量图，形状为 (nx, ny)
        """
        if self.processed_data is not None:
            # 计算每个空间点的能量（信号平方和）
            self.energy_map = np.sum(self.processed_data ** 2, axis=2)
            return self.energy_map
        return None
    
    def compute_max_amplitude_map(self) -> np.ndarray:
        """
        计算最大幅值图
        
        Returns:
            np.ndarray: 最大幅值图，形状为 (nx, ny)
        """
        if self.processed_data is not None:
            # 计算每个空间点的最大幅值
            self.max_amplitude_map = np.max(np.abs(self.processed_data), axis=2)
            return self.max_amplitude_map
        return None
    
    def compute_arrival_time_map(self, threshold: float = 0.1, normalize: bool = True) -> np.ndarray:
        """
        计算到达时间图
        
        Args:
            threshold: 幅值阈值，用于确定信号到达时间
            normalize: 是否在计算前归一化信号
            
        Returns:
            np.ndarray: 到达时间图，形状为 (nx, ny)
        """
        if self.processed_data is not None and self.time_axis is not None:
            # 初始化到达时间图
            self.arrival_time_map = np.zeros((self.nx, self.ny))
            
            # 对每个空间点计算到达时间
            for i in range(self.nx):
                for j in range(self.ny):
                    signal = self.processed_data[i, j, :]
                    
                    # 归一化信号（如果需要）
                    if normalize:
                        max_val = np.max(np.abs(signal))
                        if max_val > 0:
                            signal = signal / max_val
                    
                    # 计算信号包络
                    envelope = SignalUtils.compute_envelope(signal)
                    
                    # 找到第一个超过阈值的时间点
                    above_threshold = np.where(envelope > threshold)[0]
                    if len(above_threshold) > 0:
                        first_index = above_threshold[0]
                        self.arrival_time_map[i, j] = self.time_axis[first_index]
                    else:
                        # 如果没有超过阈值的点，设置为最大时间
                        self.arrival_time_map[i, j] = self.time_axis[-1]
            
            return self.arrival_time_map
        return None
    
    def save_to_mat(self, output_path: str) -> bool:
        """
        保存处理后的数据和分析结果到MAT文件
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            bool: 是否成功保存
        """
        if self.processed_data is not None:
            try:
                # 准备要保存的数据
                data_dict = {
                    'wave_data': self.processed_data,
                    'original_wave_data': self.wave_data,
                    'time': self.time_axis,
                    'x': self.x_axis,
                    'y': self.y_axis,
                    'fs': self.sampling_rate,
                    'nx': self.nx,
                    'ny': self.ny,
                    'nt': self.nt,
                    'dx': self.dx,
                    'dy': self.dy
                }
                
                # 添加分析结果（如果存在）
                if self.energy_map is not None:
                    data_dict['energy_map'] = self.energy_map
                
                if self.max_amplitude_map is not None:
                    data_dict['max_amplitude_map'] = self.max_amplitude_map
                
                if self.arrival_time_map is not None:
                    data_dict['arrival_time_map'] = self.arrival_time_map
                
                # 使用FileUtils保存到MAT文件
                self.file_utils.save_to_mat(output_path, data_dict)
                print(f"波场数据和分析结果已成功保存到 {output_path}")
                return True
            except Exception as e:
                print(f"保存到MAT文件 {output_path} 时出错: {str(e)}")
                return False
        else:
            print("没有可保存的数据")
            return False