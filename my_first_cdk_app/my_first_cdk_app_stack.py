

from aws_cdk import (
  aws_eks as eks_objects,
  Stack as stack,
  aws_ssm as ssm,
  # CustomResourceProvider as customprovider,
  CustomResource,
  # CustomResourceProviderRuntime as runtime,
  custom_resources,
  aws_lambda as lambda_function,
  aws_iam as iam,
  Duration,
  CfnParameter as parameter,
  CfnOutput as output,
  Token as token
)

from aws_cdk.lambda_layer_kubectl import KubectlLayer



import json

from constructs import Construct


class MyFirstCdkAppStack(stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # parameter sent in the command line
        environment = parameter(self, "environment", 
            type="String",
            description="The name of the environment")

        # ssm parameter with all the environments
        ssm.StringListParameter(self, "mySsmParameter",
            parameter_name="/platform/account/env",
            string_list_value=["development",
                              "staging",
                              "production"]
        )
        
        # lambda role
        lambda_role = iam.Role(self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            inline_policies={
                "stackPolicy":
                    iam.PolicyDocument(statements=[
                        iam.PolicyStatement(
                            actions=[
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents", 
                                "ssm:*"
                            ],
                            resources=["*"],
                            effect=iam.Effect.ALLOW,
                        )
                    ])
            },
            # managed_policies=[
            #     iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            # ],
        ) 

        # lambda function
        event_handler_function = lambda_function.Function(self, "obtain-ssm-parameter-handler",
          runtime=lambda_function.Runtime.PYTHON_3_12,
          code=lambda_function.Code.from_asset("resources"),
          handler="obtain_ssm_parameter.on_event",
          role=lambda_role,
          timeout=Duration.minutes(10),
          function_name="my_lambda_function"
        )

        # payload to send to the lamba function
        payload = json.dumps('{ "environment": ' + '"' + token.as_string(environment.value_as_string) + '"'' }')

        # Custom resource
        aws_custom_resource = custom_resources.AwsCustomResource(self, "custom_resource",
          on_update=custom_resources.AwsSdkCall(
            action='invoke',
            service='Lambda',
            physical_resource_id=custom_resources.PhysicalResourceId.of("Trigger"),
            parameters={
                "FunctionName": event_handler_function.function_name,
                "InvocationType": "RequestResponse",
                "Payload": payload
            },
          ),
          resource_type="Custom::MyCustomResource",
          on_create=custom_resources.AwsSdkCall(
              action='invoke',
              service='Lambda',
              physical_resource_id=custom_resources.PhysicalResourceId.of("Trigger"),
              parameters={
               "FunctionName": event_handler_function.function_name, 
               "InvocationType": "RequestResponse", 
               "Payload": payload
              }
          ),
          policy=custom_resources.AwsCustomResourcePolicy.from_statements([
                        iam.PolicyStatement(
                            actions=["lambda:InvokeFunction"],
                            resources=["*"],
                            effect=iam.Effect.ALLOW,
                        )
          ])
        )

        # Custom resource return value
        custom_resource_value = token.as_number(aws_custom_resource.get_response_field('Payload'))
        
        # replica_count = ssm.StringParameter.value_for_string_parameter(self,
        #     parameter_name="/platform/account/replicaCount")

        # EKS role
        eks_role = iam.Role(self, "EKSRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKSWorkerNodePolicy"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryReadOnly"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKS_CNI_Policy"),
            ])


        # EKS cluster
        eks_cluster = eks_objects.Cluster(
            self, 'eks-cluster',
            cluster_name="my-test-cluster",
            version=eks_objects.KubernetesVersion.V1_29,
            default_capacity=0, 
            kubectl_layer=KubectlLayer(self, "kubectl")
        )

        # EKS node group
        eks_cluster.add_nodegroup_capacity("custom-node-group",
          ami_type=eks_objects.NodegroupAmiType.AL2_X86_64,
          desired_size=1,
          min_size=1,
          max_size=1,
          disk_size=20,
          node_role=eks_role,
          )

        # Eks helm chart
        eks_cluster.add_helm_chart("helm-chart",
          chart="ingress-nginx",
          release="nginx-test",
          create_namespace=True,
          repository="https://kubernetes.github.io/ingress-nginx",
          namespace="nginx",
          # version="0.0.1",
          values={
            "controller.replicaCount": custom_resource_value 
          }
        )

        # outputs section
        output(self, "CurrentEnvironment",
        value=environment.value_as_string
        )

        output(self, "replicaCount",
        value=str(custom_resource_value)
        )
        

        

