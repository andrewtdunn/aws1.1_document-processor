import { Bucket } from "aws-cdk-lib/aws-s3";
import * as cdk from "aws-cdk-lib/core";
import { Construct } from "constructs";
import { NetworkingStack } from "./networking-stack";

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const s3 = new Bucket(this, "atd2005-genai-1.1-bucket");
    const networkStack = new NetworkingStack(this, "NetworkingStack", props);
  }
}
