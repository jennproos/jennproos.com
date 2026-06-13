#!/bin/bash
set -e

aws login
eval $(aws configure export-credentials --format env)
export AWS_DEFAULT_REGION=us-east-1
echo "AWS credentials exported. You can now run CDK commands."
