import * as cdk from "aws-cdk-lib/core";
import { Stack, StackProps } from "aws-cdk-lib";
import { Vpc } from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";

export class NetworkingStack extends Stack {
  public readonly vpc: Vpc;

  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    this.vpc = new Vpc(this, "Claims-Processor-VPC", {
      maxAzs: 3, // default is all AZs in region
      natGateways: 1, // default is one NAT gateway per AZ
    });
  }
}
