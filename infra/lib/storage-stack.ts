import { aws_dynamodb } from "aws-cdk-lib";
import { Table } from "aws-cdk-lib/aws-dynamodb";
import { AnyPrincipal, Effect, PolicyStatement } from "aws-cdk-lib/aws-iam";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import { S3EventSource } from "aws-cdk-lib/aws-lambda-event-sources";
import { BlockPublicAccess, Bucket, EventType } from "aws-cdk-lib/aws-s3";
import * as cdk from "aws-cdk-lib/core";
import { Construct } from "constructs";
import path from "path";

export class StorageStack extends cdk.Stack {
  // public readonly vpc: Vpc;
  public s3: Bucket;
  public usersTable: Table;
  public documentsTable: Table;
  public eventSource: S3EventSource;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    this.s3 = new Bucket(this, "atd2005-genai-1.1-bucket", {
      bucketName: "claim-documents-poc-atd",
      publicReadAccess: false,
      blockPublicAccess: BlockPublicAccess.BLOCK_ACLS_ONLY,
    });

    const domainPolicy = new PolicyStatement({
      effect: Effect.ALLOW,
      principals: [new AnyPrincipal()], // 'Any' because the filter is the Referer header
      actions: ["s3:GetObject"],
      resources: [this.s3.arnForObjects("*")],
      conditions: {
        StringLike: {
          "aws:Referer": [
            "https://docunosis.com*",
            "https://www.docunosis.com*",
          ],
        },
      },
    });

    this.s3.addToResourcePolicy(domainPolicy);

    this.usersTable = new Table(this, "users-ddb-table", {
      tableName: "docunosis-users",
      partitionKey: {
        name: "username",
        type: aws_dynamodb.AttributeType.STRING,
      },
    });

    this.documentsTable = new Table(this, "documents-ddb-table", {
      tableName: "docunosis-scans",
      partitionKey: {
        name: "doc_id",
        type: aws_dynamodb.AttributeType.STRING,
      },
    });

    const extractHandler = new Function(this, "ExtractHandler", {
      runtime: Runtime.PYTHON_3_9,
      handler: "extract.lambda_handler",
      code: Code.fromAsset(path.join(__dirname, "./lambda_code/extract")),
      environment: {
        BUCKET_NAME: this.s3.bucketName,
      },
    });

    const eventSource = new S3EventSource(this.s3, {
      events: [EventType.OBJECT_CREATED],
      filters: [{ suffix: ".pdf" }],
    });

    extractHandler.addEventSource(eventSource);
  }
}
