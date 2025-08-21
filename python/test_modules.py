#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
信号处理工具模块测试脚本
用于验证各个模块的基本功能是否正常工作
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import h5py
import time

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入工具类
from utils.file_utils import FileUtils
from utils.signal_utils import SignalUtils

# 导入处理器和可视化器
from modules.module_a import SinglePointProcessor, SinglePointVisualizer
from modules.module_b import BScanProcessor, BScanVisualizer
from modules.module_c import WaveFieldProcessor, WaveFieldVisualizer


def test_file_utils():
    """测试文件工具类"""
    print("\n测试 FileUtils 类...")
    file_utils = FileUtils()
    
    # 测试获取文件列表
    current_dir = os.path.dirname(os.path.abspath(__file__))
    py_files = file_utils.get_files_with_extension(current_dir, ".py")
    print(f"当前目录下的Python文件数量: {len(py_files)}")
    if len(py_files) > 0:
        print(f"示例文件: {py_files[0]}")
    
    # 创建测试信号并保存
    print("创建测试信号...")
    fs = 1000  # 采样率
    t = np.arange(0, 1, 1/fs)
    test_signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)
    
    # 保存为MAT文件
    test_mat_path = os.path.join(current_dir, "test_signal.mat")
    file_utils.save_to_mat(test_mat_path, signal=test_signal, fs=fs)
    print(f"测试信号已保存到: {test_mat_path}")
    
    # 读取MAT文件
    data = file_utils.read_mat_file(test_mat_path)
    if data is not None and "signal" in data:
        print(f"成功读取MAT文件，信号长度: {len(data['signal'])}")
    
    # 清理测试文件
    if os.path.exists(test_mat_path):
        os.remove(test_mat_path)
        print(f"已删除测试文件: {test_mat_path}")
    
    return True


def test_signal_utils():
    """测试信号处理工具类"""
    print("\n测试 SignalUtils 类...")
    signal_utils = SignalUtils()
    
    # 创建测试信号
    fs = 1000  # 采样率
    t = np.arange(0, 1, 1/fs)
    test_signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)
    
    # 测试滤波器
    print("测试带通滤波器...")
    filtered_signal = signal_utils.apply_bandpass_filter(test_signal, 40, 60, fs)
    print(f"滤波后信号长度: {len(filtered_signal)}")
    
    # 测试FFT
    print("测试FFT...")
    freq, magnitude = signal_utils.compute_fft(test_signal, fs)
    print(f"频率范围: {min(freq):.1f} - {max(freq):.1f} Hz")
    
    # 测试希尔伯特包络
    print("测试希尔伯特包络...")
    envelope = signal_utils.compute_envelope(test_signal, method='hilbert')
    print(f"包络长度: {len(envelope)}")
    
    return True


def test_single_point_processor():
    """测试单点信号处理器"""
    print("\n测试 SinglePointProcessor 类...")
    
    # 创建处理器实例
    processor = SinglePointProcessor()
    
    # 创建测试信号
    fs = 1000  # 采样率
    t = np.arange(0, 1, 1/fs)
    test_signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)
    
    # 设置信号
    processor.signal_data = test_signal
    processor.processed_data = test_signal.copy()
    processor.sampling_rate = fs
    processor.time_axis = t
    print(f"已设置测试信号，长度: {len(processor.signal_data)}，采样率: {processor.sampling_rate} Hz")
    
    # 测试滤波
    print("应用带通滤波器...")
    processor.apply_bandpass_filter(40, 60)
    print(f"处理后信号长度: {len(processor.processed_data)}")
    
    # 测试归一化
    print("应用归一化...")
    processor.normalize_signal()
    print(f"归一化后信号范围: {min(processor.processed_data):.2f} - {max(processor.processed_data):.2f}")
    
    # 测试包络
    print("计算包络...")
    envelope = processor.compute_envelope(method="hilbert")
    print(f"包络长度: {len(envelope)}")
    
    return True


def test_bscan_processor():
    """测试B扫描处理器"""
    print("\n测试 BScanProcessor 类...")
    
    # 创建处理器实例
    processor = BScanProcessor()
    
    # 创建测试B扫描数据
    fs = 1000  # 采样率
    t = np.arange(0, 1, 1/fs)
    positions = np.arange(0, 10, 0.5)  # 20个位置点
    
    signals = []
    for pos in positions:
        # 创建随位置变化的信号
        delay = int(pos * 10)  # 位置相关的延迟
        signal_data = np.zeros_like(t)
        if delay < len(t):
            signal_data[delay:] = np.sin(2 * np.pi * 50 * t[:len(t)-delay]) * np.exp(-0.01 * np.arange(len(t)-delay))
        signals.append(signal_data)
    
    # 设置信号
    processor.signals = signals
    processor.processed_signals = [s.copy() for s in signals]
    processor.positions = positions
    processor.sampling_rate = fs
    processor.time_axis = t
    print(f"已设置B扫描数据，信号数量: {len(processor.signals)}，采样率: {processor.sampling_rate} Hz")
    
    # 测试滤波
    print("应用带通滤波器...")
    processor.apply_bandpass_filter(40, 60)
    print(f"处理后信号数量: {len(processor.processed_signals)}")
    
    # 创建B扫描图像
    print("创建B扫描图像...")
    processor.create_bscan(normalize=True, envelope=True)
    print(f"B扫描图像尺寸: {processor.bscan_data.shape}")
    
    return True


def test_wavefield_processor():
    """测试波场处理器"""
    print("\n测试 WaveFieldProcessor 类...")
    
    # 创建处理器实例
    processor = WaveFieldProcessor()
    
    # 创建测试波场数据 (2D)
    nx, ny = 20, 20  # 网格尺寸
    nt = 100  # 时间步数
    dx, dy = 0.1, 0.1  # 网格间距
    
    # 创建简单的波场数据 (圆形波)
    wavefield_data = np.zeros((nt, nx, ny))
    x_center, y_center = nx // 2, ny // 2
    
    for t in range(nt):
        radius = t * 0.15  # 随时间扩散的半径
        for i in range(nx):
            for j in range(ny):
                dist = np.sqrt((i - x_center)**2 + (j - y_center)**2)
                if abs(dist - radius) < 2:
                    wavefield_data[t, i, j] = np.exp(-(dist - radius)**2)
    
    # 设置波场数据
    processor.wave_data = wavefield_data
    processor.processed_data = wavefield_data.copy()
    processor.nx = nx
    processor.ny = ny
    processor.nt = nt
    processor.dx = dx
    processor.dy = dy
    processor.x_axis = np.arange(nx) * dx
    processor.y_axis = np.arange(ny) * dy
    processor.time_axis = np.arange(nt)
    print(f"已设置波场数据，尺寸: {processor.wave_data.shape}")
    
    # 测试归一化
    print("应用归一化...")
    processor.normalize_data()
    print(f"归一化后数据范围: {np.min(processor.processed_data):.2f} - {np.max(processor.processed_data):.2f}")
    
    # 计算能量图
    print("计算能量图...")
    processor.compute_energy_map()
    print(f"能量图尺寸: {processor.energy_map.shape}")
    
    # 计算最大幅值图
    print("计算最大幅值图...")
    processor.compute_max_amplitude_map()
    print(f"最大幅值图尺寸: {processor.max_amplitude_map.shape}")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("开始测试信号处理工具模块...\n")
    start_time = time.time()
    
    tests = [
        ("文件工具测试", test_file_utils),
        ("信号处理工具测试", test_signal_utils),
        ("单点信号处理器测试", test_single_point_processor),
        ("B扫描处理器测试", test_bscan_processor),
        ("波场处理器测试", test_wavefield_processor)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"运行 {test_name}")
        print(f"{'='*50}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"测试失败: {str(e)}")
            results.append((test_name, False))
    
    # 打印测试结果摘要
    print(f"\n{'='*50}")
    print("测试结果摘要:")
    print(f"{'='*50}")
    all_passed = True
    for test_name, success in results:
        status = "通过" if success else "失败"
        print(f"{test_name}: {status}")
        if not success:
            all_passed = False
    
    elapsed_time = time.time() - start_time
    print(f"\n总测试时间: {elapsed_time:.2f} 秒")
    print(f"总体结果: {'全部通过' if all_passed else '部分测试失败'}")


if __name__ == "__main__":
    run_all_tests()