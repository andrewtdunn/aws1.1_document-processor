import { InfraStack } from "./infra-stack";
import { Stage, StageProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import { NetworkStack } from "./network-stack";

export class InfraStage extends Stage {
  constructor(scope: Construct, id: string, props?: StageProps) {
    super(scope, id, props);
  }

  network = new NetworkStack(this, "network-stack");
}
