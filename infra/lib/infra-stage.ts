import { NetworkingStack } from "./networking-stack";
import { InfraStack } from "./infra-stack";
import { Stage, StageProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import { ComputeStack } from "./compute-stack";

export class InfraStage extends Stage {
  constructor(scope: Construct, id: string, props?: StageProps) {
    super(scope, id, props);

    const infraStack = new InfraStack(this, "InfraStack");
    const networkStack = new NetworkingStack(this, "NetworkingStack");
    const computeStack = new ComputeStack(this, "ComputeStack", {
      vpc: networkStack.vpc,
    });
  }
}
