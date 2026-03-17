# Cloud-Data-Maturity-Evaluator

A **React + Python API** application for assessing organizational Cloud, Data, and AI maturity, generating AI-powered recommendations, and producing a consolidated roadmap with PowerPoint export.

## 🚀 Features

### Core Assessment Capabilities
- **Interactive Maturity Sliders** - Rate sub-capabilities on a 1-5 scale (Greenfield to Optimized)
- **Detailed Sub-Capabilities** - 36 specific sub-areas across all categories
- **Company Context Input** - Industry, size, IT department, and priority projects

### AI-Powered Insights
- **OpenAI Integration** - Generate executive and technical recommendations
- **Baseball Cards** - Structured project summaries for each capability area
- **8-Week Sprint Roadmap** - Detailed short-term implementation plan
- **3-Year Strategic Roadmap** - Long-term transformation vision

### Export & Visualization
- **PowerPoint Export** - Download comprehensive presentation with all insights
- **Interactive Diagrams** - Visual roadmap representations
- **Consolidated Reports** - Executive summaries and priority rankings

## 🛠️ Technology Stack

- **Frontend**: React + Vite (`DA-SaaS-Portal-Dashboard/`)
- **Backend**: FastAPI (`backend/api.py`)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **AI Integration**: OpenAI GPT-3.5-turbo
- **Export**: python-pptx for PowerPoint generation
- **Environment**: python-dotenv for secure API key management

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet connection for AI features

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Cloud-Data-Maturity-Evaluator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy the template
   cp .env_template .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here
   ```

## 🚀 Running the Application (Backend + Frontend)

### 1) Start the backend API
From the repo root:

```bash
python -m uvicorn backend.api:app --reload --port 8000
```

Health check: `http://127.0.0.1:8000/health`  
API schema: `http://127.0.0.1:8000/api/schema`

### 2) Start the React frontend
In a separate terminal:

```bash
cd DA-SaaS-Portal-Dashboard
npm install
npm run dev
```

The frontend runs on `http://localhost:3000` and proxies `/api/*` requests to the backend.

## 📊 Maturity Assessment Categories

### 1. Cloud Architecture
- Infrastructure Design
- Scalability & Performance
- Multi-cloud Strategy
- Cost Optimization
- Disaster Recovery
- Service Architecture

### 2. Data Management
- Data Quality
- Data Integration
- Master Data Management
- Data Lifecycle
- Data Storage Strategy
- Real-time Processing

### 3. Data Visualization & Insights
- Dashboard Design
- Data Storytelling
- Interactive Visualizations
- Advanced Analytics Techniques
- Self-Service Analytics
- Insight Communication

### 4. AI/ML Integration
- Model Development
- MLOps & Deployment
- AI Ethics & Bias
- Business Integration
- AutoML Capabilities
- AI Governance

### 5. Governance & Security
- Data Privacy
- Compliance Management
- Access Controls
- Risk Management
- Audit & Monitoring
- Policy Enforcement

### 6. Business Engagement
- Stakeholder Alignment
- Change Management
- Skills & Training
- Value Measurement
- Business Process Integration
- Strategic Planning

## 🎯 Maturity Levels

1. **Greenfield** - Starting from scratch
2. **Emerging** - Basic capabilities in place
3. **Developing** - Growing capabilities with some maturity
4. **Established** - Well-developed, consistent capabilities
5. **Optimized** - Advanced, continuously improving capabilities

## 📁 Project Structure

```
Cloud-Data-Maturity-Evaluator/
├── backend/api.py                          # FastAPI backend
├── app/                                    # Reusable maturity logic (non-UI)
├── ai_gen/                                 # OpenAI prompts + parsing/normalization
├── requirements.txt                        # Python dependencies
├── .env_template                          # Environment variables template
├── .gitignore                             # Git ignore rules
└── README.md                              # This file
```

## 🔐 Security

- API keys are stored in `.env` file (not committed to version control)
- `.gitignore` excludes sensitive files
- Environment variables loaded securely using `python-dotenv`

## 🚧 Future Enhancements

### Phase I
- [ ] Enhanced maturity model details and display
- [ ] High-priority keyword input for each area
- [ ] Improved heatmap with 4-square cubes per area
- [ ] Visual diagram of 18-month roadmap
- [ ] Optional polygon radar spider chart (AS-IS vs TO-BE)

### Phase II
- [ ] Automated PPT creation with recommendations
- [ ] One-click PPT download functionality

### Phase III
- [ ] Search similar projects in i11 Hub
- [ ] List available leveraging areas
- [ ] Display common team structures from past projects

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**"streamlit: command not found"**
```bash
# Use Python module syntax instead
python -m streamlit run "MaturityLevelEvaluation+AI7_v2.py"
```

**"OpenAI API key not found"**
- Ensure `.env` file exists with valid `OPENAI_API_KEY`
- Check `.env_template` for reference format

**App won't start**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

## 📞 Support

For issues or questions, please create an issue in the repository or contact the development team.