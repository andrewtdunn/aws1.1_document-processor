import { Vpc } from "aws-cdk-lib/aws-ec2";
import { Bucket } from "aws-cdk-lib/aws-s3";
import * as cdk from "aws-cdk-lib/core";
import { Construct } from "constructs";

export class InfraStack extends cdk.Stack {
  public readonly vpc: Vpc;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const s3 = new Bucket(this, "atd2005-genai-1.1-bucket");
    this.vpc = new Vpc(this, "Claims-Processor-VPC", {
      maxAzs: 3, // default is all AZs in region
      natGateways: 1, // default is one NAT gateway per AZ
    });
  }
}
