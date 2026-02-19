import { Stack, StackProps } from "aws-cdk-lib";
import { Vpc } from "aws-cdk-lib/aws-ec2";
import { Cluster, ContainerImage } from "aws-cdk-lib/aws-ecs";
import { ApplicationLoadBalancedFargateService } from "aws-cdk-lib/aws-ecs-patterns";
import { Construct } from "constructs";

interface ComputeStackProps extends StackProps {
  vpc: Vpc;
}

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
        memoryLimitMiB: 512,
        desiredCount: 1,
        taskImageOptions: {
          image: ContainerImage.fromAsset("../../code/Dockerfile"),
        },
      },
    );
  }
}
