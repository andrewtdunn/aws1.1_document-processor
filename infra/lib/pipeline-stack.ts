import * as cdk from "aws-cdk-lib";
import {
  CodePipeline,
  CodePipelineSource,
  ShellStep,
} from "aws-cdk-lib/pipelines";
import { Construct } from "constructs";
import { InfraStage } from "./infra-stage";

const repoName = "andrewtdunn/aws1.1_document-processor";
const branch = "main";
const connectionArn =
  "arn:aws:codeconnections:us-east-1:219765858109:connection/109a5933-4d04-4d46-91af-35d61aa78fa0";
const prodAccount: string = "471112703167";
const deployRegion = "us-east-1";

export class PipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const pipeline = new CodePipeline(this, "Pipeline", {
      pipelineName: "document-processor-pipeline",
      crossAccountKeys: true,
      synth: new ShellStep("Synth", {
        input: CodePipelineSource.connection(repoName, branch, {
          connectionArn,
        }),
        commands: ["npm ci", "npm run build", "npx cdk synth"],
        primaryOutputDirectory: "infra/cdk.out",
      }),
    });

    const prod = pipeline.addStage(
      new InfraStage(this, "Prod", {
        env: { account: prodAccount, region: deployRegion },
      }),
    );
  }
}
