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
    def read_txt_file(file_path: str) -> Tuple[np.ndarray, float]:
        """
        读取TXT文件，提取信号数据和采样率
        
        Args:
            file_path: TXT文件路径
            
        Returns:
            Tuple[np.ndarray, float]: 信号数据和采样率
        """
        try:
            # 读取文件内容
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # 提取采样率（假设在第一行）
            sampling_rate = 1000000.0  # 默认值
            for line in lines[:10]:  # 只检查前10行
                if 'sampling rate' in line.lower() or 'fs' in line.lower():
                    # 尝试提取数字
                    parts = line.split(':')
                    if len(parts) > 1:
                        try:
                            sampling_rate = float(parts[1].strip())
                        except ValueError:
                            pass
            
            # 提取信号数据（假设数据从某一行开始，每行一个数值）
            data = []
            data_started = False
            
            for line in lines:
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue
                
                # 尝试将行转换为浮点数
                try:
                    value = float(line)
                    data.append(value)
                    data_started = True
                except ValueError:
                    # 如果已经开始读取数据，但当前行不是数字，则停止读取
                    if data_started:
                        break
            
            return np.array(data), sampling_rate
        
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