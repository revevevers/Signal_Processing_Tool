import numpy as np
import pandas as pd
from scipy import signal
from typing import Tuple, List, Dict, Any, Optional, Union
import os
import sys

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.signal_utils import SignalUtils
from utils.file_utils import FileUtils

class SinglePointProcessor:
    """
    单点信号处理器，用于处理单个信号文件
    """
    
    def __init__(self):
        """
        初始化单点信号处理器
        """
        self.signal_data = None  # 原始信号数据
        self.processed_data = None  # 处理后的信号数据
        self.sampling_rate = None  # 采样率
        self.time_axis = None  # 时间轴
        self.file_path = None  # 文件路径
        
    def load_from_file(self, file_path: str) -> bool:
        """
        从文件加载信号数据
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否成功加载
        """
        try:
            self.file_path = file_path
            # 使用FileUtils加载TXT文件
            time_data, signal_data, sampling_rate = FileUtils.read_txt_file(file_path)
            
            if signal_data is not None and sampling_rate is not None:
                self.signal_data = signal_data
                self.processed_data = signal_data.copy()  # 初始化处理后的数据为原始数据
                self.sampling_rate = sampling_rate
                # 使用从文件读取的时间轴
                self.time_axis = time_data if len(time_data) == len(self.signal_data) else np.arange(len(self.signal_data)) / self.sampling_rate
                return True
            else:
                print(f"无法从文件 {file_path} 加载有效的信号数据")
                return False
        except Exception as e:
            print(f"加载文件 {file_path} 时出错: {str(e)}")
            return False
    
    def reset_processing(self) -> None:
        """
        重置处理，将处理后的数据恢复为原始数据
        """
        if self.signal_data is not None:
            self.processed_data = self.signal_data.copy()
    
    def apply_bandpass_filter(self, lowcut: float, highcut: float, order: int = 4) -> None:
        """
        应用带通滤波器
        
        Args:
            lowcut: 低截止频率
            highcut: 高截止频率
            order: 滤波器阶数
        """
        if self.processed_data is not None and self.sampling_rate is not None:
            self.processed_data = SignalUtils.apply_bandpass_filter(
                self.processed_data, lowcut, highcut, self.sampling_rate, order
            )
    
    def apply_lowpass_filter(self, cutoff: float, order: int = 4) -> None:
        """
        应用低通滤波器
        
        Args:
            cutoff: 截止频率
            order: 滤波器阶数
        """
        if self.processed_data is not None and self.sampling_rate is not None:
            self.processed_data = SignalUtils.apply_lowpass_filter(
                self.processed_data, cutoff, self.sampling_rate, order
            )
    
    def apply_highpass_filter(self, cutoff: float, order: int = 4) -> None:
        """
        应用高通滤波器
        
        Args:
            cutoff: 截止频率
            order: 滤波器阶数
        """
        if self.processed_data is not None and self.sampling_rate is not None:
            self.processed_data = SignalUtils.apply_highpass_filter(
                self.processed_data, cutoff, self.sampling_rate, order
            )
    
    def apply_median_filter(self, kernel_size: int = 5) -> None:
        """
        应用中值滤波器
        
        Args:
            kernel_size: 核大小
        """
        if self.processed_data is not None:
            self.processed_data = SignalUtils.apply_median_filter(
                self.processed_data, kernel_size
            )
    
    def apply_savgol_filter(self, window_length: int = 11, polyorder: int = 3) -> None:
        """
        应用Savitzky-Golay滤波器
        
        Args:
            window_length: 窗口长度
            polyorder: 多项式阶数
        """
        if self.processed_data is not None:
            self.processed_data = SignalUtils.apply_savgol_filter(
                self.processed_data, window_length, polyorder
            )
    
    def normalize_signal(self) -> None:
        """
        归一化信号
        """
        if self.processed_data is not None:
            self.processed_data = SignalUtils.normalize_signal(self.processed_data)
    
    def compute_envelope(self, method: str = 'hilbert') -> np.ndarray:
        """
        计算信号包络
        
        Args:
            method: 方法，'hilbert'或'peak'
            
        Returns:
            np.ndarray: 信号包络
        """
        if self.processed_data is not None:
            return SignalUtils.compute_envelope(self.processed_data, method)
        return None
    
    def compute_fft(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算FFT
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: 频率和幅值
        """
        if self.processed_data is not None and self.sampling_rate is not None:
            return SignalUtils.compute_fft(self.processed_data, self.sampling_rate)
        return None, None
    
    def compute_stft(self, nperseg: int = 256, noverlap: int = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        计算短时傅里叶变换（STFT）
        
        Args:
            nperseg: 每个段的长度
            noverlap: 重叠的点数
            
        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: 频率、时间和STFT结果
        """
        if self.processed_data is not None and self.sampling_rate is not None:
            return SignalUtils.compute_stft(self.processed_data, self.sampling_rate, nperseg, noverlap)
        return None, None, None
    
    def save_to_mat(self, output_path: str) -> bool:
        """
        保存处理后的数据到MAT文件
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            bool: 是否成功保存
        """
        if self.processed_data is not None and self.time_axis is not None and self.sampling_rate is not None:
            try:
                # 准备要保存的数据
                data_dict = {
                    'signal': self.processed_data,
                    'time': self.time_axis,
                    'fs': self.sampling_rate,
                    'original_signal': self.signal_data
                }
                
                # 使用FileUtils保存到MAT文件
                FileUtils.save_to_mat(output_path, **data_dict)
                return True
            except Exception as e:
                print(f"保存到MAT文件 {output_path} 时出错: {str(e)}")
                return False
        else:
            print("没有可保存的数据")
            return False
    
    def load_from_mat(self, file_path: str) -> bool:
        """
        从MAT文件加载数据
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否成功加载
        """
        try:
            self.file_path = file_path
            # 使用FileUtils加载MAT文件
            data_dict = FileUtils.read_mat_file(file_path)
            
            if data_dict is not None and 'signal' in data_dict and 'fs' in data_dict:
                self.signal_data = data_dict.get('original_signal', data_dict['signal'])
                self.processed_data = data_dict['signal']
                self.sampling_rate = data_dict['fs']
                
                # 如果MAT文件中有时间轴，则使用它，否则创建新的时间轴
                if 'time' in data_dict:
                    self.time_axis = data_dict['time']
                else:
                    self.time_axis = np.arange(len(self.signal_data)) / self.sampling_rate
                    
                return True
            else:
                print(f"MAT文件 {file_path} 中缺少必要的数据字段")
                return False
        except Exception as e:
            print(f"加载MAT文件 {file_path} 时出错: {str(e)}")
            return False