# Potential Insight Compass (PIC)

## 🎯 Overview

Potential Insight Compass (PIC) is an AI-powered career counseling support system that analyzes interview records and counseling notes to discover hidden strengths and career potentials. Using Google Gemini API, it transforms negative self-perceptions into positive insights and provides both qualitative and quantitative analysis of individual capabilities.

![Main Interface](_images/mainpage1.jpeg)
*Main application interface showing text input and analysis options*

## ✨ Key Features

- **AI-Driven Analysis**: Leverages Google Gemini API for objective and consistent analysis
- **Positive Reframing**: Converts negative traits into potential strengths
- **Dual Perspective**: Provides both qualitative insights and quantitative visualizations
- **Interactive Charts**: Radar charts showing 6-dimensional capability scores
- **User-Friendly Interface**: Built with Streamlit for intuitive operation

![Analysis Results](_images/analysisResult1.jpeg)
![Analysis Results](_images/analysisResult2.jpeg)
![Analysis Results](_images/analysisResult3.jpeg)
![Analysis Results](_images/analysisResult4.jpeg)
![Analysis Results](_images/analysisResult5.jpeg)
![Analysis Results](_images/analysisResult6.jpeg)
*Sample analysis results showing qualitative insights and quantitative visualizations*

## 🏗️ Repository Structure

```
potential-insight-compass/
├── .env                    # Environment variables (DO NOT COMMIT)
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
├── README.md             # This file (English)
├── README-ja.md          # Japanese version
├── SPECIFICATION.md      # Detailed system specifications (Japanese)
├── requirements.txt      # Python dependencies
├── app.py               # Main Streamlit application
├── _images/             # UI screenshots and demo images
│   ├── mainpage1.jpeg    # Main interface screenshot
│   ├── analysisResult*.jpeg # Analysis results examples
│   └── resultExport.jpeg # Export functionality demo
├── docs/                # Documentation
│   ├── code-documentation.md # Detailed code documentation
│   └── api-reference.md     # API reference guide
├── src/                 # Source code directory
│   ├── __init__.py
│   ├── ai_analyzer.py   # Gemini API integration
│   ├── data_processor.py # Data processing utilities
│   └── visualizer.py    # Chart generation functions
└── tests/              # Test files
    ├── __init__.py
    └── test_analyzer.py # Unit tests for analyzer
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12.4 or higher
- Google AI Studio API key ([Get it here](https://aistudio.google.com/))
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yf591/potential-insight-compass.git
   cd potential-insight-compass
   ```

2. **Create and activate virtual environment** ⚠️ **IMPORTANT**
   ```bash
   # Create virtual environment
   python3 -m venv .venv
   
   # Activate virtual environment (macOS/Linux)
   source .venv/bin/activate
   
   # Activate virtual environment (Windows)
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   # Ensure virtual environment is activated
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Google Gemini API key
   # GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   # Ensure virtual environment is activated
   streamlit run app.py
   ```

### Environment Setup Details

> **🔴 CRITICAL**: Always work within the virtual environment to avoid system-wide package conflicts.

**Before any operation, always activate the virtual environment.**
```bash
source .venv/bin/activate
```

**To deactivate the virtual environment.**
```bash
deactivate
```

**To verify you're in the virtual environment.**
```bash
which python  # Should show path containing .venv
python --version  # Should show Python 3.12.4
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Google Gemini API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# ngrok Token (Optional - for external access testing)
NGROK_TOKEN=your_ngrok_token_here
```

### API Key Setup

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Copy the key and add it to your `.env` file
4. Never commit the `.env` file to version control

## 🎮 Usage

1. **Start the application**
   ```bash
   source .venv/bin/activate  # Always activate first!
   streamlit run app.py
   ```

2. **Access the web interface**
   - Open your browser and go to `http://localhost:8501`

3. **Input analysis text**
   - Paste counseling notes or interview records into the text area
   - **Click "Analyze"** to process the input
  ![main page - after the input](_images/mainpage2.jpeg)

4. **View results**
   - **Qualitative analysis**: 5 strengths and 3 career recommendations
  ![analysis result](_images/analysisResult1.jpeg)
  ![analysis result](_images/analysisResult2.jpeg)
  ![analysis result](_images/analysisResult3.jpeg)
   - **Quantitative analysis**: Interactive radar chart with 6 capability dimensions
  ![analysis result](_images/analysisResult4.jpeg)
  ![analysis result](_images/analysisResult5.jpeg)
  ![analysis result](_images/analysisResult6.jpeg)

![Export Functionality](_images/resultExport.jpeg)
*Export analysis results in JSON or Markdown format*

## 📊 Analysis Dimensions

The system evaluates individuals across 6 key dimensions.

1. **継続・集中力** (Persistence & Focus)
2. **実行・行動力** (Execution & Action)
3. **共感・協調性** (Empathy & Cooperation)
4. **論理・分析力** (Logic & Analysis)
5. **創造・発想力** (Creativity & Innovation)
6. **計画・堅実性** (Planning & Reliability)

## 🧪 Development

### Running Tests
```bash
source .venv/bin/activate
python -m pytest tests/
```

### Code Quality
```bash
source .venv/bin/activate
# Linting
flake8 src/
# Type checking
mypy src/
```

### Adding Dependencies
```bash
source .venv/bin/activate
pip install new-package
pip freeze > requirements.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes in the virtual environment
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini API for powerful language processing
- Streamlit for the excellent web framework
- Plotly for beautiful data visualizations

## 📕 Documentation

- **[Code Documentation](docs/code-documentation.md)**: Detailed explanation of all modules and functions
- **[API Reference](docs/api-reference.md)**: Complete API reference with examples
- **[System Specification](SPECIFICATION.md)**: Technical specifications (Japanese)
- **[Japanese README](README-ja.md)**: 日本語版README

## 🤙 Support

If you encounter any issues or have questions, please
1. Check the [documentation](docs/) for detailed technical information
2. Review the [SPECIFICATION.md](SPECIFICATION.md) for system requirements
3. Open an issue on GitHub
4. Ensure you're working in the virtual environment when reporting bugs

---

**⚠️ Remember: Always activate your virtual environment before working on this project!**

```bash
source .venv/bin/activate
```