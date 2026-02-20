# Project Structure

## Root Layout

```
/
├── code/           # Python application code
├── infra/          # AWS CDK infrastructure code
└── readme_images/  # Documentation assets
```

## Code Directory (`/code`)

Python Flask application and document processing logic.

```
code/
├── server.py                  # Flask web server with health/reverse endpoints
├── document_processor.py      # Core logic for S3 + Bedrock integration
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container definition
└── venv/                      # Python virtual environment (local)
```

## Infrastructure Directory (`/infra`)

AWS CDK TypeScript project for infrastructure as code.

```
infra/
├── bin/
│   └── infra.ts              # CDK app entry point
├── lib/
│   ├── infra-stack.ts        # Main infrastructure stack (S3)
│   ├── infra-stage.ts        # Stage definition for pipeline
│   ├── pipeline-stack.ts     # CI/CD pipeline configuration
│   ├── compute-stack.ts      # Compute resources
│   ├── lambda-stack.ts       # Lambda functions
│   └── networking-stack.ts   # VPC and networking
├── test/
│   └── infra.test.ts         # Infrastructure tests
├── cdk.json                  # CDK configuration
├── package.json              # Node dependencies and scripts
└── tsconfig.json             # TypeScript configuration
```

## Architecture Patterns

### Stack Organization

- Modular stack design with separate concerns (networking, compute, lambda, pipeline)
- Stage-based deployment for environment promotion
- Cross-account pipeline deployment to production

### Naming Conventions

- Stack files: `{purpose}-stack.ts`
- Kebab-case for file names
- PascalCase for TypeScript classes
- Snake_case for Python files and functions

### Configuration

- Pipeline configured for GitHub repo via CodeConnections
- Production account: 219765858109
- Deploy region: us-east-1
- Main branch triggers automatic deployment
