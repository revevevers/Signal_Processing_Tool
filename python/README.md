# 信号处理工具 - Python版本

## 项目概述

这是原MATLAB信号处理工具的Python重新实现版本，使用Streamlit作为GUI框架。该工具提供了一系列信号处理功能，包括单点信号处理、B扫描信号处理和波场数据处理。

## 功能特点

### 模块A：单点信号处理
- 加载和处理单个TXT格式信号文件
- 多种滤波器选项（带通、低通、高通、中值、Savitzky-Golay等）
- 频谱分析和时频分析
- 信号包络提取
- 信号对比分析

### 模块B：B扫描信号处理
- 批量处理多个TXT格式信号文件
- 创建B扫描图像
- 瀑布图和3D可视化
- 信号切片分析

### 模块C：波场数据处理
- 处理MAT格式的波场数据
- 时间切片提取和可视化
- 能量图、最大幅值图和到达时间图计算
- 3D波场可视化

## 安装和使用

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行应用
```bash
cd python
streamlit run app.py
```

## 项目结构
```
python/
├── app.py                 # 主应用入口
├── requirements.txt       # 依赖库列表
├── assets/                # 静态资源
├── data/                  # 示例数据
├── modules/               # 功能模块
│   ├── module_a/          # 单点信号处理
│   ├── module_b/          # B扫描信号处理
│   └── module_c/          # 波场数据处理
├── pages/                 # Streamlit多页面
│   ├── 01_Module_A.py     # 模块A页面
│   ├── 02_Module_B.py     # 模块B页面
│   └── 03_Module_C.py     # 模块C页面
└── utils/                 # 通用工具
    ├── file_utils.py      # 文件处理工具
    ├── signal_utils.py    # 信号处理工具
    └── ui_components.py   # UI组件
```

## 支持的数据格式
- TXT文件：单点信号和B扫描信号
- MAT文件：波场数据和处理结果

## 贡献
欢迎提交问题报告和改进建议。

## 许可
本项目采用MIT许可证。