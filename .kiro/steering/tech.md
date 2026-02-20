# Technology Stack

## Backend

- Python 3.11
- Flask 3.1.2 web framework
- boto3 for AWS SDK integration
- Docker containerization

## Infrastructure

- AWS CDK 2.215.0 (TypeScript)
- TypeScript 5.9.3
- Node.js with npm

## AWS Services

- Amazon S3 (document storage)
- Amazon Bedrock (AI/ML models - Claude v2)
- AWS CodePipeline (CI/CD)
- AWS CodeConnections (GitHub integration)

## Testing

- Jest for infrastructure tests
- ts-jest for TypeScript testing

## Common Commands

### Python Application

```bash
# Install dependencies
cd code
python -m pip install -r requirements.txt

# Run Flask server locally
python server.py
# Server runs on port 80 at 0.0.0.0

# Build Docker image
docker build -t document-processor .
```

### Infrastructure (CDK)

```bash
cd infra

# Install dependencies
npm ci

# Build TypeScript
npm run build

# Watch mode for development
npm run watch

# Run tests
npm test

# CDK commands
npx cdk synth      # Synthesize CloudFormation
npx cdk deploy     # Deploy to AWS
npx cdk diff       # Show differences
```

## Development Notes

- Flask app runs in debug mode on port 80
- Docker uses Python 3.11-slim base image
- CDK uses ts-node for TypeScript execution
- Pipeline deploys to production account automatically on main branch commits
