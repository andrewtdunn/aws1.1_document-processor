import { aws_dynamodb } from "aws-cdk-lib";
import { Table } from "aws-cdk-lib/aws-dynamodb";
import { Vpc } from "aws-cdk-lib/aws-ec2";
import { BlockPublicAccess, Bucket } from "aws-cdk-lib/aws-s3";
import * as cdk from "aws-cdk-lib/core";
import { Construct } from "constructs";

export class StorageStack extends cdk.Stack {
  // public readonly vpc: Vpc;
  public s3: Bucket;
  public usersTable: Table;
  public documentsTable: Table;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    this.s3 = new Bucket(this, "atd2005-genai-1.1-bucket", {
      bucketName: "docunosis-bucket",
      blockPublicAccess: new BlockPublicAccess({
        blockPublicAcls: false,
        blockPublicPolicy: false,
        ignorePublicAcls: false,
        restrictPublicBuckets: false,
      }),
      publicReadAccess: true,
      enforceSSL: true,
    });

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
  }
}
