import { NetworkingStack } from "./networking-stack";
import { StorageStack } from "./storage-stack";
import { Stage, StageProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import { ComputeStack } from "./compute-stack";

export class InfraStage extends Stage {
  constructor(scope: Construct, id: string, props?: StageProps) {
    super(scope, id, props);

    const storageStack = new StorageStack(this, "StorageStack");
    const networkStack = new NetworkingStack(this, "NetworkingStack");
    const computeStack = new ComputeStack(this, "ComputeStack", {
      vpc: networkStack.vpc,
      s3: storageStack.s3,
      usersTable: storageStack.usersTable,
      documentsTable: storageStack.documentsTable,
    });
  }
}
