# jennproos.com

My personal website showcasing my work, experience, and providing a way to get in touch.

**Live Site:** [jennproos.com](https://jennproos.com/)

## Repository Overview

This repository contains the complete website infrastructure and deployment pipeline, built using AWS services and automated with GitHub Actions.

## Repository Structure

```
jennproos.com/
├── web/              # React front-end application
├── infra/            # AWS CDK infrastructure code
└── .github/          # GitHub Actions workflows
```

## Components

### 1. Web (`web/`)

A React-based front-end application featuring basic information about myself and my background.

The website is a modern, responsive React application that provides an engaging user experience.

### 2. Infrastructure (`infra/`)

AWS CDK (Cloud Development Kit) infrastructure written in Python that provisions:
- **S3 Bucket** - Hosts the static website files with public read access
- **CloudFront Distribution** - CDN for fast, global content delivery with HTTPS
- **Route 53** - DNS management for both root domain and www subdomain
- **ACM Certificate** - SSL/TLS certificate for secure HTTPS connections
- **Lambda Function** - Serverless function to handle contact form submissions
- **API Gateway** - REST API endpoint for the contact form with CORS enabled
- **SES Email Identity** - Email service for sending messages from the contact form
- **IAM User** - GitHub deployment user with S3 access for CI/CD
- **Secrets Manager** - Secure storage for deployment credentials

**Key Features:**
- Infrastructure as Code (IaC) using AWS CDK
- Comprehensive test suite covering all infrastructure components
- Serverless contact form backend with Lambda and API Gateway
- Automated deployment pipeline with GitHub Actions

For detailed infrastructure documentation, see [infra/README.md](infra/README.md)

**Infrastructure Testing:**
```bash
cd infra
./run-tests.sh
```

### 3. CI/CD Automation (`.github/workflows/`)

**test-infra.yaml** - Continuous Integration workflow that:
- Runs on pull requests to `main` branch (when `infra/` files change)
- Executes the complete infrastructure test suite
- Prevents merging if tests fail (when branch protection is enabled)
- Uses Python 3.13 and caches dependencies for fast runs

**deploy-website.yaml** - Deployment workflow that automatically:
- Triggers on push to `main` branch (when `web/` files change)
- Syncs website files to S3 bucket
- Configures S3 bucket for static website hosting
- Can also be manually triggered via workflow_dispatch

**Deployment Process:**
1. Push changes to the `web/` directory
2. GitHub Actions automatically deploys to S3
3. CloudFront serves the updated content globally
4. Changes are live at jennproos.com

## Getting Started

### Prerequisites

- AWS CLI configured with appropriate credentials
- Python 3.13+ (for infrastructure development)
- Node.js and npm (for AWS CDK and React development)
- AWS CDK Toolkit installed (`npm install -g aws-cdk`)

### Deploying Infrastructure

```bash
cd infra
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk deploy
```

### Updating the Website

Simply edit files in the `web/` directory and push to the `main` branch. The GitHub Actions workflow will automatically deploy your changes.

For manual deployment:
```bash
cd web
aws s3 sync . s3://jennproos.com --delete
```

## Architecture

```
User Request
    ↓
Route 53 (DNS)
    ↓
CloudFront (CDN)
    ↓
S3 Bucket (Static Website)

Contact Form Submission
    ↓
API Gateway (REST API)
    ↓
Lambda Function
    ↓
SES (Email Service)
```

**Security:**
- All traffic redirected to HTTPS
- ACM certificate for SSL/TLS encryption
- CloudFront provides DDoS protection
- API Gateway CORS configuration for secure cross-origin requests
- Lambda function uses IAM roles with least privilege access
- Deployment credentials stored securely in AWS Secrets Manager

## Contact Form Flow

1. User fills out contact form on website
2. Form submission sends POST request to API Gateway endpoint
3. API Gateway invokes Lambda function
4. Lambda function processes the form data and sends email via SES
5. User receives confirmation of successful submission

## Development Workflow

1. **Infrastructure Changes:** Modify CDK code in `infra/`, run tests, deploy with `cdk deploy`
2. **Website Changes:** Edit files in `web/`, commit and push to trigger auto-deployment
3. **Lambda Function Updates:** Modify code in `infra/resources/`, deploy with `cdk deploy`
4. **Testing:** Run infrastructure tests with `cd infra && ./run-tests.sh`

## Branch Protection & Quality Gates

To ensure code quality, this repository uses GitHub Actions for automated testing. To require tests to pass before merging:

### Setting Up Branch Protection

1. Go to your GitHub repository **Settings** → **Branches**
2. Click **Add branch protection rule**
3. Configure the rule:
   - **Branch name pattern:** `main`
   - **Require a pull request before merging:** ✅ Check this
   - **Require status checks to pass before merging:** ✅ Check this
   - **Status checks that are required:**
     - Select `test / Test Infrastructure` (appears after first workflow run)
   - **Require branches to be up to date before merging:** ✅ Check this
4. Click **Create** or **Save changes**

Once configured, all pull requests to `main` must pass the infrastructure tests before they can be merged.

## Dependency Management

This repository uses Dependabot to automatically monitor and update dependencies:

- **Python Dependencies** - AWS CDK libraries and pytest are checked weekly
- **GitHub Actions** - Action versions are monitored for security updates
- **Automated PRs** - Dependabot creates pull requests for dependency updates
- **Grouped Updates** - Related packages (like AWS CDK) are grouped together

Dependabot configuration: `.github/dependabot.yml`

## Links

- Website: [jennproos.com](https://jennproos.com/)
- Email: jennproos@gmail.com
