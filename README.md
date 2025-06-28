# 🎫 Multi-Agent AI Helpdesk (IBM Granite)

**Professional AI-powered enterprise helpdesk system built for hackathon demonstration**

A sophisticated multi-agent AI system that processes employee support tickets through intelligent classification, context retrieval, response generation, and confidence assessment using IBM Watsonx Granite models.

## 🚀 Live Demo Features

- **🎯 Smart Classification**: AI categorizes tickets into IT/HR/Finance/Admin/Other
- **📚 Intelligent Retrieval**: Context-aware policy document matching
- **💬 Professional Responses**: IBM Granite-powered reply generation  
- **🎯 Confidence Scoring**: Quality assessment with automatic escalation
- **📊 Real-time Analytics**: Live statistics and processing metrics
- **🔄 Interactive UI**: Streamlit-based professional interface

## 🏗️ System Architecture

### Multi-Agent Pipeline
```
User Ticket → [Classifier Agent] → [Retriever Agent] → [Responder Agent] → [Confidence Agent] → Final Response
```

### 🤖 AI Agents

1. **Classifier Agent**
   - Analyzes ticket content using IBM Granite
   - Categorizes into 5 categories: IT, HR, Finance, Admin, Other
   - Fallback keyword-based classification for reliability

2. **Retriever Agent**  
   - Maps categories to relevant policy documents
   - Searches knowledge base for contextual information
   - Returns "No policy found" for unmatched queries

3. **Responder Agent**
   - Generates professional replies using retrieved context
   - Powered by IBM Granite 13B Instruct v2
   - Produces empathetic, actionable responses

4. **Confidence Agent**
   - Evaluates response quality (0.0 - 1.0 scale)
   - Triggers escalation for scores < 0.6
   - Provides quality assurance layer

## 📂 Project Structure

```
├── app.py                          # Main Streamlit application
├── granite_client.py               # IBM Watsonx API integration  
├── agents.py                       # 4-agent processing system
├── utils.py                        # Helper functions & utilities
├── knowledge_base/                 # Company policy documents
│   ├── vpn_policy.txt              # IT: VPN access procedures
│   ├── leave_policy.txt            # HR: Leave policies & procedures  
│   ├── reimbursement_policy.txt    # Finance: Expense claim process
│   ├── salary_policy.txt           # Finance: Payroll information
│   ├── holiday_calendar.txt        # Admin: Holiday schedules
│   └── hardware_issuance.txt       # Admin: IT equipment requests
├── logs.csv                        # Auto-generated ticket logs
├── requirements.txt                # Python dependencies
└── README.md                       # This documentation
```

## 🔧 Quick Start

### Prerequisites
- Python 3.8+
- IBM Watsonx.ai access

### Installation & Setup

1. **Clone/Download Project**
   ```bash
   # Download all project files to your directory
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Access the Demo**
   - Open browser to `http://localhost:8501`
   - The app is ready for demonstration!

## 🎯 IBM Watsonx Integration

### Model Configuration
- **Model**: `ibm/granite-3-3-8b-instruct`
- **Endpoint**: `https://us-south.ml.cloud.ibm.com`
- **Temperature**: 0.6 (balanced creativity/accuracy)
- **Max Tokens**: 300 (concise responses)
- **Decoding**: Greedy (consistent results)

### Authentication
All IBM Granite credentials are pre-configured in `granite_client.py`:
- API Key: Embedded in code
- Project ID: Pre-configured
- Connection testing available in UI

## 📊 Demo Usage Guide

### For Hackathon Judges

1. **System Overview**
   - Click "Multi-Agent System Overview" to see agent architecture
   - Test IBM Granite connection in sidebar
   - View real-time statistics

2. **Example Tickets** (Pre-loaded for demo)
   - "I can't access the VPN from home"
   - "How many sick leaves am I allowed per year?"
   - "My salary came late this month"
   - "Where can I see the holiday calendar?"
   - "I'm having issues with the finance portal"
   - "How do I apply for reimbursement?"

3. **Processing Flow**
   - Select example or type custom ticket
   - Click "Process Ticket with AI Agents"
   - Observe real-time agent processing
   - Review classification, context, response, and confidence

4. **Quality Features**
   - Confidence scoring with color coding
   - Automatic escalation alerts
   - Retrieved context display
   - User feedback collection

### Sample Demo Script

```
1. "Let me show you our multi-agent AI helpdesk system..."
2. Select VPN ticket → Shows IT classification & technical response
3. Select leave ticket → Shows HR classification & policy response  
4. Select salary ticket → Shows Finance classification & escalation
5. "Notice how confidence scores trigger human escalation..."
6. "The system logs everything for continuous improvement..."
```

## 🔍 Technical Highlights

### AI/ML Features
- **Natural Language Processing**: IBM Granite 13B Instruct v2
- **Multi-Agent Architecture**: 4 specialized AI agents
- **Confidence Scoring**: Automated quality assessment
- **Fallback Systems**: Keyword-based classification backup
- **Context-Aware Retrieval**: Smart policy matching

### Software Engineering
- **Clean Code**: Modular, documented, professional structure
- **Error Handling**: Graceful failures with user feedback
- **Logging**: Comprehensive system and user activity logs
- **UI/UX**: Professional Streamlit interface with custom CSS
- **Data Persistence**: CSV logging for analytics

### Enterprise Features
- **Scalable Architecture**: Easily extendable agent system
- **Knowledge Management**: File-based policy system
- **Analytics Dashboard**: Real-time metrics and insights
- **Quality Assurance**: Multi-layer validation and escalation

## 📈 System Metrics

### Performance Indicators
- **Processing Time**: ~3-5 seconds per ticket
- **Classification Accuracy**: Keyword fallback ensures 100% categorization
- **Escalation Rate**: Automatically calculated and displayed
- **User Satisfaction**: Feedback collection system

### Monitoring Features
- Real-time ticket statistics
- Category breakdown analysis
- Confidence score tracking
- Recent ticket history

## 🔮 Future Enhancements

### Technical Roadmap
- **Advanced ML**: Custom classification model training
- **Vector Search**: Semantic similarity for knowledge retrieval
- **Multi-Language**: International support capabilities
- **Integration APIs**: Enterprise system connectivity
- **Advanced Analytics**: ML-powered insights dashboard

### Business Features
- **Role-Based Access**: Department-specific views
- **SLA Tracking**: Response time monitoring
- **Escalation Workflows**: Complex routing logic
- **Knowledge Base Management**: Dynamic policy updates

## 🏆 Hackathon Readiness

### Demo Strengths
✅ **Professional UI** - Polished, corporate-ready interface  
✅ **Live AI Integration** - Real IBM Granite API calls  
✅ **Complete Pipeline** - End-to-end ticket processing  
✅ **Real-time Features** - Live statistics and feedback  
✅ **Error Handling** - Graceful failure management  
✅ **Documentation** - Comprehensive, professional docs  
✅ **Scalable Architecture** - Production-ready design  
✅ **Business Value** - Clear enterprise use case  

### Judge Evaluation Points
- **Technical Innovation**: Multi-agent AI architecture
- **Code Quality**: Clean, modular, well-documented
- **User Experience**: Intuitive, professional interface  
- **Business Impact**: Real enterprise helpdesk solution
- **Completeness**: Fully functional end-to-end system
- **Scalability**: Extensible, production-ready design

## 🛠️ Troubleshooting

### Common Issues
1. **Import Errors**: Run `pip install -r requirements.txt`
2. **Streamlit Issues**: Update to latest version
3. **IBM Connection**: Check network connectivity
4. **File Permissions**: Ensure write access for logs.csv

### Debug Mode
- Check console logs for detailed error information
- Use sidebar connection test for IBM Granite status
- Verify knowledge base files are accessible

## 📞 Support & Contact

- **Technical Issues**: Check logs and error messages
- **Demo Questions**: Review this README thoroughly
- **System Requirements**: Python 3.8+, stable internet connection

---

## 🎉 Built for Innovation

**Technologies**: IBM Watsonx.ai, Streamlit, Python, Multi-Agent AI  
**Use Case**: Enterprise Helpdesk Automation  
**Status**: Hackathon Demo Ready  
**License**: Educational/Demonstration Use  

*This system demonstrates the power of IBM Granite models in enterprise AI applications with sophisticated multi-agent architectures.* 