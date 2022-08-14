#!/bin/sh
aws cloudformation deploy --template-file=schema.yaml --stack-name=algotrading-data-schema --capabilities=CAPABILITY_IAM