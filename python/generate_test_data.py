#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
示例数据生成脚本
用于生成测试用的信号数据、B扫描数据和波场数据
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import h5py

# 添加当前目录到系统路径
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入工具类
from utils.file_utils import FileUtils


def create_directory(directory):
    """创建目录（如果不存在）"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"创建目录: {directory}")
    return directory


def generate_single_point_data(output_dir, num_samples=5):
    """生成单点信号数据"""
    print("\n生成单点信号数据...")
    output_dir = create_directory(output_dir)
    file_utils = FileUtils()
    
    # 基本参数
    fs = 1000  # 采样率 (Hz)
    duration = 1.0  # 信号持续时间 (秒)
    t = np.arange(0, duration, 1/fs)
    
    # 生成不同类型的信号
    signal_types = [
        ("sine_wave", lambda t: np.sin(2 * np.pi * 50 * t)),
        ("chirp", lambda t: signal.chirp(t, f0=10, f1=150, t1=duration, method='linear')),
        ("damped_sine", lambda t: np.sin(2 * np.pi * 50 * t) * np.exp(-3 * t)),
        ("noisy_sine", lambda t: np.sin(2 * np.pi * 50 * t) + 0.2 * np.random.randn(len(t))),
        ("multi_component", lambda t: np.sin(2 * np.pi * 30 * t) + 0.5 * np.sin(2 * np.pi * 90 * t))
    ]
    
    # 生成并保存信号
    for i in range(min(num_samples, len(signal_types))):
        name, signal_func = signal_types[i]
        signal_data = signal_func(t)
        
        # 保存为TXT文件
        txt_path = os.path.join(output_dir, f"{name}.txt")
        with open(txt_path, 'w') as f:
            f.write(f"{fs}\n")  # 第一行写入采样率
            for val in signal_data:
                f.write(f"{val}\n")
        print(f"已保存TXT文件: {txt_path}")
        
        # 保存为MAT文件
        mat_path = os.path.join(output_dir, f"{name}.mat")
        file_utils.save_to_mat(mat_path, signal=signal_data, fs=fs)
        print(f"已保存MAT文件: {mat_path}")
    
    return output_dir


def generate_bscan_data(output_dir, num_positions=20):
    """生成B扫描数据"""
    print("\n生成B扫描数据...")
    output_dir = create_directory(output_dir)
    file_utils = FileUtils()
    
    # 基本参数
    fs = 1000  # 采样率 (Hz)
    duration = 1.0  # 信号持续时间 (秒)
    t = np.arange(0, duration, 1/fs)
    positions = np.linspace(0, 100, num_positions)  # 位置点 (mm)
    
    # 创建B扫描数据
    signals = []
    for pos in positions:
        # 创建随位置变化的信号
        delay = int((pos / 100) * 200)  # 位置相关的延迟
        signal_data = np.zeros_like(t)
        if delay < len(t):
            # 创建一个随位置变化的衰减正弦波
            wave = np.sin(2 * np.pi * 50 * t[:len(t)-delay]) * np.exp(-5 * t[:len(t)-delay])
            signal_data[delay:] = wave
            # 添加一些噪声
            signal_data += 0.05 * np.random.randn(len(t))
        signals.append(signal_data)
    
    # 保存为TXT文件
    txt_dir = create_directory(os.path.join(output_dir, "txt_files"))
    for i, (pos, signal_data) in enumerate(zip(positions, signals)):
        txt_path = os.path.join(txt_dir, f"signal_{pos:.1f}.txt")
        with open(txt_path, 'w') as f:
            f.write(f"{fs}\n")  # 第一行写入采样率
            for val in signal_data:
                f.write(f"{val}\n")
    print(f"已保存 {num_positions} 个TXT文件到: {txt_dir}")
    
    # 保存为MAT文件
    mat_path = os.path.join(output_dir, "bscan_data.mat")
    signals_array = np.array(signals)
    file_utils.save_to_mat(mat_path, signals=signals_array, positions=positions, fs=fs)
    print(f"已保存B扫描MAT文件: {mat_path}")
    
    return output_dir


def generate_wavefield_data(output_dir, grid_size=(50, 50), time_steps=100):
    """生成波场数据"""
    print("\n生成波场数据...")
    output_dir = create_directory(output_dir)
    file_utils = FileUtils()
    
    # 基本参数
    nx, ny = grid_size
    nt = time_steps
    dx, dy = 1.0, 1.0  # 网格间距 (mm)
    
    # 创建波场数据 (圆形波)
    wavefield_data = np.zeros((nt, nx, ny))
    x_center, y_center = nx // 2, ny // 2
    
    # 生成圆形扩散波
    for t in range(nt):
        radius = t * 0.4  # 随时间扩散的半径
        for i in range(nx):
            for j in range(ny):
                dist = np.sqrt((i - x_center)**2 + (j - y_center)**2)
                # 创建一个随距离衰减的波
                if dist > 0:  # 避免除以零
                    wavefield_data[t, i, j] = np.sin(dist - 0.8 * t) * np.exp(-0.01 * dist) / np.sqrt(dist)
    
    # 添加一些噪声
    wavefield_data += 0.02 * np.random.randn(*wavefield_data.shape)
    
    # 保存为MAT文件
    mat_path = os.path.join(output_dir, "wavefield_data.mat")
    file_utils.save_to_mat(mat_path, wavefield_data=wavefield_data, dx=dx, dy=dy, nx=nx, ny=ny, nt=nt)
    print(f"已保存波场数据MAT文件: {mat_path}")
    
    # 生成3D波场数据
    print("生成3D波场数据...")
    nx, ny, nz = 30, 30, 10  # 较小的网格以减少计算量
    wavefield_data_3d = np.zeros((nt, nx, ny, nz))
    x_center, y_center, z_center = nx // 2, ny // 2, nz // 2
    
    # 生成3D球形扩散波
    for t in range(nt):
        radius = t * 0.3  # 随时间扩散的半径
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    dist = np.sqrt((i - x_center)**2 + (j - y_center)**2 + (k - z_center)**2)
                    # 创建一个随距离衰减的波
                    if dist > 0:  # 避免除以零
                        wavefield_data_3d[t, i, j, k] = np.sin(dist - 0.6 * t) * np.exp(-0.02 * dist) / np.sqrt(dist)
    
    # 添加一些噪声
    wavefield_data_3d += 0.02 * np.random.randn(*wavefield_data_3d.shape)
    
    # 保存为MAT文件
    mat_path_3d = os.path.join(output_dir, "wavefield_data_3d.mat")
    file_utils.save_to_mat(mat_path_3d, wavefield_data=wavefield_data_3d, dx=dx, dy=dy, dz=1.0, nx=nx, ny=ny, nz=nz, nt=nt)
    print(f"已保存3D波场数据MAT文件: {mat_path_3d}")
    
    return output_dir


def generate_all_test_data():
    """生成所有测试数据"""
    print("开始生成测试数据...")
    
    # 创建数据目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = create_directory(os.path.join(base_dir, "data"))
    
    # 生成各类数据
    single_point_dir = create_directory(os.path.join(data_dir, "single_point"))
    bscan_dir = create_directory(os.path.join(data_dir, "bscan"))
    wavefield_dir = create_directory(os.path.join(data_dir, "wavefield"))
    
    generate_single_point_data(single_point_dir)
    generate_bscan_data(bscan_dir)
    generate_wavefield_data(wavefield_dir)
    
    print("\n所有测试数据生成完成！")
    print(f"数据保存在: {data_dir}")


if __name__ == "__main__":
    generate_all_test_data()