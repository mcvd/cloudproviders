# https://diagrams.mingrammer.com/docs/nodes/aws
from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway
from diagrams.aws.database import DynamodbTable
from diagrams.aws.security import IdentityAndAccessManagementIam
from diagrams.aws.devtools import Codebuild
from diagrams.aws.devtools import Codecommit
from diagrams.aws.devtools import Codedeploy
from diagrams.aws.devtools import Codepipeline
from diagrams.aws.management import Cloudformation
from diagrams.aws.devtools import CommandLineInterface
from diagrams.aws.general import User
from diagrams.aws.general import General
from diagrams.onprem.client import Client

with Diagram("Serverless Web Apps", show=False, direction="TB"):
    
    
    with Cluster("Launch API URL"):
        user = User("User")
        console = Client("Browser")
        user >> console

    
    with Cluster("Cloud9", direction="LR"):
        builder = User("Builder")
        cli = CommandLineInterface("AWS CLI")
        builder >> cli
    
    with Cluster("CloudFormation"):
        cloudformation = Cloudformation("Stack")
        cloudformation >> IdentityAndAccessManagementIam("IAM")
        cloudformation >> Codecommit("CodeCommit")
        cloudformation >> Codebuild("CodeBuild")
        cloudformation >> Codepipeline("CodePipeline")
        cloudformation >> S3("S3")
        cli >> cloudformation

    with Cluster("CodePipeline"):
        codepipeline = Codepipeline("Pipeline")
        codepipeline >> Codecommit("CodeCommit")
        codepipeline >> Codebuild("CodeBuild")
        codepipeline >> Cloudformation("CloudFormation")
        
    with Cluster("Serverless Application Model"):
        sam = Cloudformation("SAM Template")
        apigateway = APIGateway("API Gateway")
        mylambda = Lambda("Lambda")
        ddb  = DynamodbTable("DynamoDB")   
        sam >> apigateway
        sam >> mylambda
        sam >> ddb

        cloudformation >> codepipeline >> sam
        
        console >> apigateway