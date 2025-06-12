# 🚀 FastAPI Fake User Generator API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Enterprise-grade API for generating realistic fake user data. Perfect for testing, development, and data simulation.

## 🎯 Key Features

- **🔥 High Performance**: Built with FastAPI for lightning-fast responses
- **🔐 Secure Authentication**: API key-based access control
- **⚡ Rate Limiting**: Prevent abuse with tier-based rate limits
- **📊 Multiple Data Formats**: Export as JSON, CSV, or XML
- **🌍 International Support**: Generate locale-specific user data
- **🎨 Rich User Profiles**: Includes avatars, social media, and more
- **📱 Modern API Design**: RESTful endpoints with OpenAPI documentation
- **🔍 Advanced Filtering**: Customizable data fields and pagination

## 📚 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Features in Detail](#-features-in-detail)
- [Use Cases](#-use-cases)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fake-user-api.git
cd fake-user-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

1. Start the server:
```bash
uvicorn main:app --reload
```

2. Create an API key:
```bash
curl -X POST "http://localhost:8000/api-keys" \
     -H "Content-Type: application/json" \
     -d '{"name": "my-app", "tier": "free"}'
```

3. Generate fake users:
```bash
curl "http://localhost:8000/users/5" \
     -H "X-API-Key: your-api-key"
```

## 📖 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/user` | Get single user |
| GET | `/users/{count}` | Get multiple users |
| POST | `/export` | Export users in various formats |
| GET | `/health` | API health check |
| POST | `/api-keys` | Create new API key |

### Authentication

All endpoints require an API key passed in the `X-API-Key` header:
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/user
```

### Rate Limits

- Free Tier: 100 requests/minute
- Premium Tier: 1000 requests/minute
- Enterprise: Custom limits

## 🎯 Features in Detail

### Rich User Data Fields
- Personal Information
  - Name, Email, Phone
  - Address, Birthday
  - Username, Avatar URL
- Professional Details
  - Job Title, Company
  - Skills, Education
  - Languages
- Online Presence
  - Social Media Profiles
  - Website
  - Professional Links

### Data Export Options
- JSON (default)
- CSV (spreadsheet-friendly)
- XML (legacy systems)
- Field filtering
- Pagination support

### Security Features
- API Key Authentication
- Rate Limiting
- Request Tracking
- Usage Statistics

## 💡 Use Cases

- **Development & Testing**
  - UI/UX Prototyping
  - Load Testing
  - Integration Testing

- **Education & Training**
  - Database Population
  - API Testing Tutorials
  - Development Workshops

- **Demo Applications**
  - Sales Demonstrations
  - Product Showcases
  - POC Development

## 🚀 Deployment

### Render
```bash
# Deploy to Render
render deploy
```

### Docker
```bash
# Build image
docker build -t fake-user-api .

# Run container
docker run -p 8000:8000 fake-user-api
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

[⬆ back to top](#-fastapi-fake-user-generator-api) 