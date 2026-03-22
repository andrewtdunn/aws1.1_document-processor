import { Stack, StackProps } from "aws-cdk-lib";
import { Certificate } from "aws-cdk-lib/aws-certificatemanager";
import { Vpc } from "aws-cdk-lib/aws-ec2";
import { Cluster, ContainerImage } from "aws-cdk-lib/aws-ecs";
import { ApplicationLoadBalancedFargateService } from "aws-cdk-lib/aws-ecs-patterns";
import { Construct } from "constructs";
import * as path from "path";

interface ComputeStackProps extends StackProps {
  vpc: Vpc;
}

const sslCertArn =
  "arn:aws:acm:us-east-1:654654396735:certificate/bdb364ed-0350-4b44-b599-0fd86274f978";

export class ComputeStack extends Stack {
  constructor(scope: Construct, id: string, props?: ComputeStackProps) {
    super(scope, id, props);

    const { vpc } = props!;

    const cluster = new Cluster(this, "compute-cluster", {
      vpc,
    });

    const app = new ApplicationLoadBalancedFargateService(
      this,
      "fargate-service",
      {
        cluster,
        cpu: 256,
        certificate: Certificate.fromCertificateArn(
          this,
          "sslCert",
          sslCertArn,
        ),
        memoryLimitMiB: 512,
        desiredCount: 1,
        taskImageOptions: {
          image: ContainerImage.fromAsset(
            path.resolve(__dirname, "..", "..", "code", "docunosis"),
          ),
        },
      },
    );
  }
}
