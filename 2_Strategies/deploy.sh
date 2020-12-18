#!/bin/bash
image=$1
service=$1

# Get the account number associated with the current IAM credentials
account=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]
then
    exit 255
fi

# Get the region defined in the current configuration
region=$(aws configure get region)
region=${region:-us-east-1}

echo "create docker-compose.yml"

cp docker-compose.yml.template docker-compose.yml
sed -i "s/\$ENV/${env}/g" docker-compose.yml
sed -i "s/\$REGION/${region}/g" docker-compose.yml
sed -i "s/\$IMAGE/${account}.dkr.ecr.${region}.amazonaws.com\/${image}/g" docker-compose.yml
sed -i "s/\$SERVICE/${service}/g" docker-compose.yml

AWS_EXPORTS=`aws cloudformation list-exports`

VPC=`echo $AWS_EXPORTS | jq -r '.Exports[] | select (.Name=="AlgorithmicTrading-VPC") | .Value'`
SUBNET1=`echo $AWS_EXPORTS | jq -r '.Exports[] | select (.Name=="AlgorithmicTrading-PrivateSubnet1") | .Value'`
SUBNET2=`echo $AWS_EXPORTS | jq -r '.Exports[] | select (.Name=="AlgorithmicTrading-PrivateSubnet2") | .Value'`
SG=`echo $AWS_EXPORTS | jq -r '.Exports[] | select (.Name=="AlgorithmicTrading-ECSHostSecurityGroup") | .Value'`
TASK_ROLE=`echo $AWS_EXPORTS | jq -r '.Exports[] | select (.Name=="AlgorithmicTrading-ECSTaskExecutionRole") | .Value'`
ROLE_ARN=`echo $AWS_EXPORTS | jq -r '.Exports[] | select (.Name=="AlgorithmicTrading-AlgoExecutionRole-ARN") | .Value'`
CLUSTER=`echo $AWS_EXPORTS | jq -r '.Exports[] | select (.Name=="AlgorithmicTrading-ECSCluster") | .Value'`

echo "create ecs-params.yml"

cp ecs-params.yml.template ecs-params.yml
sed -i "s/\$VPC/${VPC}/g" ecs-params.yml
sed -i "s/\$SUBNET1/${SUBNET1}/g" ecs-params.yml
sed -i "s/\$SUBNET2/${SUBNET2}/g" ecs-params.yml
sed -i "s/\$SG/${SG}/g" ecs-params.yml
sed -i "s/\$TASK_ROLE/${TASK_ROLE}/g" ecs-params.yml
sed -i "s@\$ROLE_ARN@${ROLE_ARN}@g" ecs-params.yml

if [ ! -f "ecs-cli" ] ; then
  curl -Lo ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
  chmod 777 ecs-cli
  echo "ecs-cli installed"
fi

./ecs-cli configure --region ${region} --cluster ${CLUSTER} --default-launch-type FARGATE