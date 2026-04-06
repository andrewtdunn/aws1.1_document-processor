import { Stack, StackProps } from "aws-cdk-lib";
import { Table } from "aws-cdk-lib/aws-dynamodb";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import { S3EventSource } from "aws-cdk-lib/aws-lambda-event-sources";
import { Bucket, EventType } from "aws-cdk-lib/aws-s3";
import { Construct } from "constructs";

interface LambdaProps extends StackProps {
  docs_bucket: Bucket;
  docs_table: Table;
}

export class LambdaStack extends Stack {
  constructor(scope: Construct, id: string, props: LambdaProps) {
    super(scope, id, props);

    const extractHandler = new Function(this, "ExtractHandler", {
      runtime: Runtime.PYTHON_3_9,
      handler: "extract.lambda_handler",
      code: Code.fromAsset("./lambda_code/extract"),
      environment: {
        BUCKET_NAME: props.docs_bucket.bucketName,
        TABLE_NAME: props.docs_table.tableName,
      },
    });

    extractHandler.addEventSource(
      new S3EventSource(props.docs_bucket, {
        events: [EventType.OBJECT_CREATED],
        filters: [{ suffix: ".pdf" }],
      }),
    );
  }
}
