# 🚨 RescueSync Agent

AI-powered disaster response coordination system using multi-step reasoning, persistent memory, and performance tracking.

[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-FF9900?logo=amazon-aws)](https://aws.amazon.com/bedrock/)
[![Claude 3.5](https://img.shields.io/badge/Claude-3.5%20Sonnet-8A2BE2)](https://www.anthropic.com/claude)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Problem Statement

During disasters (earthquakes, building collapses, floods), first responders from different agencies face **critical coordination gaps**:
- Duplicated rescue efforts
- Missed victims in high-priority zones
- Inefficient resource allocation
- 2-4 hour coordination delays that cost lives

**Real-world impact**: Turkey's 2023 earthquakes showed "lack of coordination and reliable information in first hours" as the #1 rescue barrier (source: peer-reviewed disaster response research).

---

## 💡 Solution

**RescueSync** is an autonomous AI agent that:
1. **Analyzes** disaster scenarios using structured multi-step reasoning
2. **Prioritizes** search zones by survivor count, structural safety, and access difficulty
3. **Assigns** response teams (Fire, Medical, K9) to optimal zones based on expertise
4. **Generates** minute-by-minute coordination timelines with safety checkpoints

### Key Features
✅ **Multi-Step Reasoning**: 3-stage analysis (Priority → Allocation → Timeline)  
✅ **Persistent Memory**: Tracks incidents across sessions (AgentCore simulation)  
✅ **Performance Metrics**: Real-time execution time, cost, and token tracking  
✅ **Multi-Scenario Support**: Building collapse, earthquake, flood response  
✅ **Autonomous Decisions**: No human input needed for coordination plans

---

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│ USER (Web Browser) │
└────────────────────────────┬────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ S3 Static Website (index.html) │
│ - Scenario selector (3 disaster types) │
│ - Real-time metrics display │
└────────────────────────────┬────────────────────────────────┘
│ HTTPS POST
▼
┌─────────────────────────────────────────────────────────────┐
│ Amazon API Gateway (REST API) │
│ - /prod endpoint │
│ - CORS enabled │
└────────────────────────────┬────────────────────────────────┘
│ Lambda Proxy
▼
┌─────────────────────────────────────────────────────────────┐
│ AWS Lambda (Python 3.11) │
│ ┌─────────────────────────────────────────────────┐ │
│ │ RescueSync Agent Logic: │ │
│ │ 1. Parse scenario + type │ │
│ │ 2. Build context-aware prompt │ │
│ │ 3. Call Bedrock inference profile │ │
│ │ 4. Track performance metrics │ │
│ │ 5. Log to memory (incident ID) │ │
│ │ 6. Format structured output │ │
│ └─────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
│ invoke_model()
▼
┌─────────────────────────────────────────────────────────────┐
│ Amazon Bedrock (Inference Profile) │
│ - Model: us.anthropic.claude-3-5-sonnet-20241022-v2:0 │
│ - Cross-region routing (us-east-1, us-east-2, us-west-2) │
│ - Multi-step reasoning with structured prompts │
└─────────────────────────────────────────────────────────────┘


---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Amazon Bedrock + Claude 3.5 Sonnet v2 | Multi-step reasoning engine |
| **Inference** | Bedrock Inference Profile | Cross-region routing, high availability |
| **Compute** | AWS Lambda (Python 3.11) | Serverless agent execution |
| **API** | Amazon API Gateway (REST) | Public endpoint for web access |
| **Storage** | Amazon S3 | Static website hosting |
| **Memory** | In-memory log (scalable to DynamoDB) | Persistent incident tracking |
| **IAM** | AWS IAM Roles | Least-privilege access control |

---

## 🚀 Live Demo

🌐 **Website**: http://rescuesync-demo-yourname.s3-website-us-east-1.amazonaws.com  
🔗 **API Endpoint**: https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod  
📹 **Video Demo**: [YouTube Link]  

### Try It Now
1. Visit the live website
2. Select a disaster scenario type (Building Collapse / Earthquake / Flood)
3. Click "Run RescueSync Agent"
4. See AI-generated coordination plan in ~15 seconds
5. Check performance metrics (execution time, cost, tokens, incident ID)

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Execution Time** | 5-15 seconds (depends on scenario complexity) |
| **Cost per Coordination** | $0.01-0.03 USD |
| **Tokens Processed** | 1,500-2,500 tokens |
| **Tokens per Second** | 150-200 tps |
| **Latency** | <200ms API Gateway + 5-13s Bedrock inference |

---

## 🎥 Demo Video

[![RescueSync Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://youtube.com/watch?v=YOUR_VIDEO_ID)

**Highlights**:
- 0:00 - Problem overview (coordination gaps in disasters)
- 0:30 - Live demo (select scenario → run agent → output)
- 1:30 - Multi-step reasoning walkthrough
- 2:00 - Performance metrics & memory features
- 2:30 - Architecture & AWS services

---

## 📝 Example Output

╔═══════════════════════════════════════════════════════════════╗
║ RESCUESYNC AI DISASTER COORDINATOR ║
║ Multi-Step Reasoning Architecture (v1.0) ║
╚═══════════════════════════════════════════════════════════════╝

🎯 SCENARIO TYPE: BUILDING COLLAPSE
📋 INCIDENT ID: INC-20251017-140723

STEP 1️⃣ - SEARCH PRIORITY ANALYSIS
Priority 1: Floor 3 - 12 people, 20% safe, Hard access
Priority 2: Floor 2 - 8 people, 70% safe, Easy access
Priority 3: Basement - 5 people, 40% safe, Hard access

STEP 2️⃣ - RESOURCE ALLOCATION
🔥 Fire_Alpha → Floor 3 - Create structural support and debris removal
⚕️ Medical_Beta → Floor 2 - Triage and stabilize casualties
🐕 K9_Gamma → Basement - Pinpoint survivor locations

STEP 3️⃣ - 10-MINUTE COORDINATION TIMELINE
Minutes 0-3: Teams deploy, establish entry points [CHECKPOINT]
Minutes 4-6: Primary rescue operations [CHECKPOINT]
Minutes 7-10: Secondary search, evacuation [CHECKPOINT]

════════════════════════════════════════════════════════════════
📊 AGENT MEMORY & PERFORMANCE METRICS
════════════════════════════════════════════════════════════════

💾 PERSISTENT MEMORY:

Total incidents coordinated: 3

Incident ID: INC-20251017-140723

Session context maintained

⚡ PERFORMANCE METRICS:

Execution time: 12.45 seconds

Estimated cost: $0.0187 USD

Tokens processed: ~1,847 tokens


## 📦 Installation & Deployment

### Quick Start (30 minutes)
1. Clone repository
git clone https://github.com/yourusername/rescuesync-agent.git
cd rescuesync-agent

2. Follow deployment-guide.md for AWS setup
3. Update index.html with your API Gateway URL
4. Deploy to S3
text

See **[deployment-guide.md](deployment-guide.md)** for detailed instructions.

---

## 🏆 AWS AI Agent Global Hackathon 2025

### Judging Criteria Alignment

| Criterion | Weight | Our Approach |
|-----------|--------|--------------|
| **Potential Value/Impact** | 20% | Solves documented problem in disaster response coordination (Turkey 2023 research) |
| **Creativity** | 10% | Novel application of Bedrock inference profiles for underserved disaster ops niche |
| **Technical Execution** | 50% | Production-ready serverless architecture, proper IAM, inference profiles, error handling |
| **Functionality** | 10% | Multi-scenario support, autonomous decisions, working live demo |
| **Demo Presentation** | 10% | Clean UI, clear reasoning steps, performance metrics, 3-min video |

### Prize Categories
- ✅ **General Prizes**: 1st/2nd/3rd place ($16k/$9k/$5k)
- ✅ **Best Amazon Bedrock AgentCore Implementation** ($3k): Memory simulation + reasoning
- ✅ **Best Amazon Bedrock Application** ($3k): Inference profile + multi-step reasoning

---

## 🔒 Security & Compliance

- **IAM**: Least-privilege roles (Lambda execution + Bedrock access only)
- **API**: No authentication (demo only); production would use Cognito/API keys
- **Data**: No PII stored; scenarios are synthetic
- **CORS**: Enabled for web access from S3 static site

---

## 💰 Cost Analysis

| Component | Usage | Cost |
|-----------|-------|------|
| **Bedrock** | 50 coordinations × 2,000 tokens × $0.003/1K = | $0.30 |
| **Lambda** | 50 invocations × 15s × $0.0000166667/GB-s = | $0.01 |
| **API Gateway** | 50 requests (free tier) = | $0.00 |
| **S3** | Static hosting (free tier) = | $0.00 |
| **Total Demo Cost** | | **$0.31** |

**Production scaling**: $3-5 per 100 coordinations (well within budget).

---

## 🧪 Testing

### Manual Testing (Web UI)
1. Access S3 website
2. Test all 3 scenario types
3. Verify metrics display
4. Check incident ID increments

### API Testing (curl)
curl -X POST https://YOUR-API-GATEWAY-URL/prod
-H "Content-Type: application/json"
-d '{
"scenario": "Building collapsed, 5 floors, 10 casualties",
"scenario_type": "building_collapse"
}'

text

---

## 🗺️ Roadmap (Post-Hackathon)

- [ ] DynamoDB integration for persistent memory
- [ ] Real-time radio feed integration (OpenMHZ API)
- [ ] Mobile app for field responders
- [ ] Multi-language support (Spanish, Hindi, Arabic)
- [ ] Integration with 911 CAD systems
- [ ] Drone feed analysis (thermal imaging)
- [ ] AgentCore Bedrock orchestration for sub-agents

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 👥 Team

Built for AWS AI Agent Global Hackathon 2025  
**Developer**: [Your Name]  
**GitHub**: [@yourusername](https://github.com/yourusername)  
**LinkedIn**: [Your Profile]

---

## 🙏 Acknowledgments

- **AWS**: Amazon Bedrock, Lambda, API Gateway, S3
- **Anthropic**: Claude 3.5 Sonnet v2 model
- **Research**: Turkey 2023 earthquake coordination studies
- **Inspiration**: Real first responders solving coordination challenges daily

---

## 📞 Contact

Questions? Issues? Feedback?  
- **Email**: your.email@example.com
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/rescuesync-agent/issues)
- **Devpost**: [Project Page](https://devpost.com/software/rescuesync-agent)

---

**Built with ❤️ for first responders worldwide**

