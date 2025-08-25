# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Signal Processing Tool (SPT) with both MATLAB and Python implementations. The Python version is a Streamlit-based web application for signal processing with three main modules:

- **Module A**: Single-point signal processing (completed)
- **Module B**: B-scan signal processing (completed)  
- **Module C**: Wavefield data processing (in development)

## Prompt Optimization - Avoid Exceeding Context Length Limits

When using Claude Code for programming or long-document processing, overly long inputs may trigger "context length exceeded" or "maximum tokens" errors. To avoid this, please follow these guidelines:

Prompt:

When handling long inputs, process them in segments instead of loading everything at once. If the input document or code exceeds the model’s context limit, please:

- Summarize or extract key parts instead of expanding everything word by word.

- Split overly long inputs into chunks and focus on one segment at a time.

- Keep only the necessary context and discard irrelevant content.

- Use concise expressions and avoid repetitive descriptions.

- If the input still exceeds the context limit, remind me with "Input too long, please provide it in segments" instead of throwing an error or forcing the load.

## Development Commands

### Installation
```bash
cd python
pip install -r requirements.txt
```

### Running the Application
```bash
cd python
streamlit run app.py
```

### Testing
Run comprehensive module tests:
```bash
cd python
python test_modules.py
```

Run quick functionality test:
```bash
cd python
python simple_test.py
```

### Data Generation
Generate test data (if needed):
```bash
cd python
python generate_test_data.py
```

## Architecture

### Python Structure
```
python/
├── app.py                 # Main Streamlit application
├── modules/               # Signal processing modules
│   ├── module_a/         # Single-point signal processing
│   ├── module_b/         # B-scan processing  
│   └── module_c/         # Wavefield processing
├── pages/                # Streamlit pages
│   ├── home_page.py      # Home page
│   ├── module_a_page.py  # Module A interface
│   ├── module_b_page.py  # Module B interface
│   └── module_c_page.py  # Module C interface (to be developed)
├── utils/                # Utility functions
│   ├── file_utils.py     # File I/O operations
│   └── signal_utils.py   # Signal processing utilities
└── data/                 # Sample data files
    ├── single_point/     # Single signal examples
    ├── bscan/           # B-scan data
    └── wavefield/       # Wavefield data
```

### Key Components

**Module Architecture**: Each module follows a consistent pattern:
- `processor.py`: Core signal processing logic
- `visualizer.py`: Data visualization methods  
- Page module in `pages/`: Streamlit user interface

**Data Flow**:
1. User uploads TXT/MAT files through Streamlit interface
2. File utilities parse and load data
3. Processor applies filters and analysis
4. Visualizer creates plots and visualizations
5. Results displayed in web interface

## Current Development Status

Based on PROJECT_STATUS.md:
- **Module A**: 100% complete - single signal processing with filters, FFT, envelope extraction
- **Module B**: 100% complete - B-scan processing with waterfall plots, 3D visualization  
- **Module C**: 50% complete - core wavefield processing implemented, UI needs development

## Technical Stack

- **Web Framework**: Streamlit 1.22.0
- **Numerical Computing**: NumPy 1.24.3, SciPy 1.10.1
- **Data Handling**: Pandas 2.0.1, h5py 3.8.0
- **Visualization**: Matplotlib 3.7.1, Plotly 5.14.1
- **Machine Learning**: scikit-learn 1.2.2 (available)

## File Formats Supported

- **TXT**: Time series data with header information
- **MAT**: MATLAB data files (.mat)

## Signal Processing Features

### Available Filters
- Butterworth bandpass/lowpass/highpass filters
- Median filter
- Savitzky-Golay filter
- Hilbert transform envelope extraction

### Analysis Methods
- Fast Fourier Transform (FFT)
- Short-Time Fourier Transform (STFT) 
- Signal normalization
- Envelope detection
- B-scan image creation
- Wavefield time slicing

## Development Priorities

1. **Complete Module C UI** (`pages/module_c_page.py`)
2. **Implement 3D wavefield visualization** 
3. **Add time slice browser for wavefield data**
4. **Performance optimization** for large datasets
5. **Error handling** and input validation

## Testing Strategy

- Use `test_modules.py` for comprehensive module testing
- Use `simple_test.py` for quick functionality verification
- Test with sample data in `data/` directory
- Focus on file I/O, filter operations, and visualization

## Common Development Tasks

When working on this project:
1. Follow the established module pattern (processor + visualizer + page)
2. Use existing utility functions in `utils/`
3. Maintain consistent Streamlit UI styling
4. Test with both TXT and MAT file formats
5. Verify all three modules work independently