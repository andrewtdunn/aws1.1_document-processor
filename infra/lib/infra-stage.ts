import { NetworkingStack } from "./networking-stack";
import { InfraStack } from "./infra-stack";
import { Stage, StageProps } from "aws-cdk-lib";
import { Construct } from "constructs";

export class InfraStage extends Stage {
  constructor(scope: Construct, id: string, props?: StageProps) {
    super(scope, id, props);

    const infraStack = new InfraStack(this, "InfraStack");
  }
}
