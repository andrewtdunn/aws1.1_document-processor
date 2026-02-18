import { InfraStack } from "./infra-stack";
import { Stage, StageProps } from "aws-cdk-lib";
import { Construct } from "constructs";

export class InfraStage extends Stage {
  constructor(scope: Construct, id: string, props?: StageProps) {
    super(scope, id, props);
  }

  InfraStack = new InfraStack(this, "InfraStack", {
    description: "temporary",
  });
}
