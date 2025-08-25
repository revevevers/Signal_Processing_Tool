import os
import numpy as np
import scipy.io as sio
import glob
from typing import Tuple, List, Dict, Any, Optional, Union

class FileUtils:
    """
    文件处理工具类，用于处理TXT和MAT文件的读写操作
    """
    
    @staticmethod
    def read_txt_signal(file_path: str) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        读取TXT文件，提取时间序列和信号数据（专用于B扫描格式）
        
        Args:
            file_path: TXT文件路径
            
        Returns:
            Tuple[np.ndarray, np.ndarray, float]: 时间序列、信号数据和采样率
        """
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # 处理B扫描数据格式：跳过前5行头部信息
            data_start_line = 5
            
            # 提取时间和信号数据
            time_data = []
            signal_data = []
            
            for line in lines[data_start_line:]:
                line = line.strip()
                # 跳过空行
                if not line:
                    continue
                
                # 解析时间和信号数据（制表符分割）
                try:
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        time_val = float(parts[0])
                        signal_val = float(parts[1])
                        time_data.append(time_val)
                        signal_data.append(signal_val)
                except (ValueError, IndexError):
                    # 如果解析失败，跳过这一行
                    continue
            
            time_array = np.array(time_data)
            signal_array = np.array(signal_data)
            
            # 计算采样率
            if len(time_array) > 1:
                dt = time_array[1] - time_array[0]
                sampling_rate = 1.0 / dt
            else:
                sampling_rate = 1000000.0  # 默认值
            
            return time_array, signal_array, sampling_rate
        
        except Exception as e:
            raise Exception(f"读取TXT文件失败: {str(e)}")
    
    @staticmethod
    def save_to_mat(file_path: str, **kwargs) -> None:
        """
        保存数据到MAT文件
        
        Args:
            file_path: 保存路径
            **kwargs: 要保存的变量，格式为变量名=变量值
        """
        try:
            sio.savemat(file_path, kwargs)
        except Exception as e:
            raise Exception(f"保存MAT文件失败: {str(e)}")
    
    @staticmethod
    def save_bscan_to_mat(file_path: str, data_xyt: np.ndarray, data_time: np.ndarray) -> None:
        """
        保存B扫描数据到MAT文件
        
        Args:
            file_path: 保存路径
            data_xyt: B扫描数据矩阵，形状为 (位置数, 时间点数)
            data_time: 时间轴数据
        """
        try:
            # 确保时间轴数据是一维数组
            if data_time.ndim > 1:
                data_time = data_time.flatten()
            
            # 使用MATLAB兼容的格式保存
            data_dict = {
                'data_xyt': np.asarray(data_xyt, dtype=np.float64),
                'data_time': np.asarray(data_time, dtype=np.float64).reshape(1, -1)  # MATLAB默认行向量
            }
            sio.savemat(file_path, data_dict)
        except Exception as e:
            raise Exception(f"保存B扫描MAT文件失败: {str(e)}")
    
    @staticmethod
    def read_mat_file(file_path: str) -> Dict[str, Any]:
        """
        读取MAT文件
        
        Args:
            file_path: MAT文件路径
            
        Returns:
            Dict[str, Any]: MAT文件中的变量字典
        """
        try:
            # 尝试使用scipy.io读取MAT文件
            data = sio.loadmat(file_path)
            
            # 移除特殊变量（以双下划线开头的变量）
            keys_to_remove = [key for key in data.keys() if key.startswith('__')]
            for key in keys_to_remove:
                data.pop(key)
            
            return data
        except NotImplementedError:
            # 如果是高版本MAT文件（v7.3），使用h5py读取
            try:
                import h5py
                with h5py.File(file_path, 'r') as f:
                    data = {}
                    for key in f.keys():
                        data[key] = np.array(f[key])
                return data
            except Exception as e:
                raise Exception(f"读取高版本MAT文件失败: {str(e)}")
        except Exception as e:
            raise Exception(f"读取MAT文件失败: {str(e)}")
    
    @staticmethod
    def get_files_with_extension(directory: str, extension: str) -> List[str]:
        """
        获取指定目录下特定扩展名的文件列表
        
        Args:
            directory: 目录路径
            extension: 文件扩展名（如'.txt'）
            
        Returns:
            List[str]: 文件路径列表
        """
        if not extension.startswith('.'):
            extension = '.' + extension
        
        pattern = os.path.join(directory, f'*{extension}')
        files = glob.glob(pattern)
        
        # 按文件名排序
        files.sort()
        
        return files
    
    @staticmethod
    def get_files_with_pattern(directory: str, pattern: str) -> List[str]:
        """
        获取指定目录下匹配特定模式的文件列表
        
        Args:
            directory: 目录路径
            pattern: 文件名模式（如'signal_*.txt'）
            
        Returns:
            List[str]: 文件路径列表
        """
        full_pattern = os.path.join(directory, pattern)
        files = glob.glob(full_pattern)
        
        # 按文件名排序
        files.sort()
        
        return files