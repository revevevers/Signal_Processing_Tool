#!/usr/bin/env python3
"""
简单的功能测试脚本
"""

import sys
import os
import numpy as np

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_file_utils():
    """测试文件处理工具"""
    print("测试文件处理工具...")
    
    from utils.file_utils import FileUtils
    
    # 测试读取示例文件
    example_file = "data/single_point/sine_wave.txt"
    if os.path.exists(example_file):
        try:
            time_data, signal_data, sampling_rate = FileUtils.read_txt_file(example_file)
            print(f"✅ 成功读取文件: {len(signal_data)} 个数据点")
            print(f"   采样率: {sampling_rate} Hz")
            print(f"   时间范围: {time_data[0]:.6f} - {time_data[-1]:.6f} 秒")
            return True
        except Exception as e:
            print(f"❌ 文件读取失败: {e}")
            return False
    else:
        print(f"⚠️ 示例文件不存在: {example_file}")
        return False

def test_signal_utils():
    """测试信号处理工具"""
    print("\n测试信号处理工具...")
    
    from utils.signal_utils import SignalUtils
    
    # 创建测试信号
    fs = 1000000  # 1MHz采样率
    t = np.linspace(0, 0.001, 1000)  # 1ms信号
    signal = np.sin(2 * np.pi * 100000 * t)  # 100kHz正弦波
    
    try:
        # 测试带通滤波
        filtered = SignalUtils.apply_bandpass_filter(signal, 50000, 200000, fs)
        print(f"✅ 带通滤波成功: 输入{len(signal)}点 -> 输出{len(filtered)}点")
        
        # 测试FFT
        freqs, magnitudes = SignalUtils.compute_fft(signal, fs)
        print(f"✅ FFT计算成功: {len(freqs)} 个频率点")
        
        # 测试包络提取
        envelope = SignalUtils.compute_envelope(signal)
        print(f"✅ 包络提取成功: {len(envelope)} 个点")
        
        return True
    except Exception as e:
        print(f"❌ 信号处理失败: {e}")
        return False

def test_processor():
    """测试单点处理器"""
    print("\n测试单点处理器...")
    
    from modules.module_a.processor import SinglePointProcessor
    
    try:
        processor = SinglePointProcessor()
        
        # 测试加载示例文件
        example_file = "data/single_point/sine_wave.txt"
        if os.path.exists(example_file):
            if processor.load_from_file(example_file):
                print(f"✅ 处理器加载文件成功")
                
                # 测试滤波
                processor.apply_bandpass_filter(50000, 200000)
                print(f"✅ 带通滤波应用成功")
                
                # 测试FFT
                freqs, mags = processor.compute_fft()
                if freqs is not None:
                    print(f"✅ FFT计算成功: {len(freqs)} 个频率点")
                
                return True
            else:
                print(f"❌ 处理器加载文件失败")
                return False
        else:
            print(f"⚠️ 示例文件不存在，跳过处理器测试")
            return False
    except Exception as e:
        print(f"❌ 处理器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🔬 信号处理工具功能测试")
    print("=" * 50)
    
    success_count = 0
    total_tests = 3
    
    # 运行测试
    if test_file_utils():
        success_count += 1
    
    if test_signal_utils():
        success_count += 1
    
    if test_processor():
        success_count += 1
    
    # 输出结果
    print("\n" + "=" * 50)
    print(f"测试完成: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("✅ 所有测试通过！核心功能工作正常。")
        return True
    else:
        print("❌ 部分测试失败，请检查相关模块。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)