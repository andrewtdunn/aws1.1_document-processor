#!/usr/bin/env node
import * as cdk from "aws-cdk-lib/core";
import { InfraStack } from "../lib/infra-stack";

const app = new cdk.App();
new InfraStack(app, "InfraStack", {
  env: { account: "637423577773", region: "us-east-1" },
});

app.synth();
