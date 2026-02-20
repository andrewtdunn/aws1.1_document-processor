# Product Overview

Bedrock Document Parser is a proof-of-concept document processing solution for insurance claims. It extracts structured information from claim documents and generates summaries using Amazon Bedrock's AI models.

## Core Functionality

- Extracts key information from insurance claim documents (claimant name, policy number, incident date, claim amount, description)
- Generates concise summaries of claims using AI
- Processes documents stored in S3
- Leverages Amazon Bedrock (Claude models) for natural language processing

## Architecture

The solution consists of:

- Python Flask web service for document processing
- AWS infrastructure deployed via CDK
- S3 for document storage
- Amazon Bedrock for AI-powered extraction and summarization
- CI/CD pipeline using AWS CodePipeline
