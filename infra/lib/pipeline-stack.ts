import * as cdk from "aws-cdk-lib";
import {
  CodePipeline,
  CodePipelineSource,
  ShellStep,
} from "aws-cdk-lib/pipelines";
import { Construct } from "constructs";
import { InfraStage } from "./infra-stage";
import { Effect, PolicyStatement } from "aws-cdk-lib/aws-iam";

const repoName = "andrewtdunn/aws1.1_document-processor";
const branch = "main";
const connectionArn =
  "arn:aws:codeconnections:us-east-1:637423577773:connection/5aaaaa13-84f7-403e-b14f-a3b92040799e";
const prodAccount: string = "219765858109";
const deployRegion = "us-east-1";

export class PipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const pipeline = new CodePipeline(this, "Pipeline", {
      pipelineName: "claims-processor-pipeline",
      crossAccountKeys: true,
      synth: new ShellStep("Synth", {
        input: CodePipelineSource.connection(repoName, branch, {
          connectionArn,
        }),
        commands: ["cd infra", "npm ci", "npm run build", "npx cdk synth"],
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
