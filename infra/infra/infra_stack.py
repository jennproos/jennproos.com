from aws_cdk import (
    Stack,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment
)
from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, stack_name="PersonalWebsiteInfraStack", **kwargs)

        domain_bucket = s3.Bucket(
            self,
            "domain-bucket",
            bucket_name="jennproos.com",
            public_read_access=True,
            website_index_document="index.html"
        )

        s3.Bucket(
            self,
            "subdomain-bucket",
            bucket_name="www.jennproos.com",
            website_redirect=s3.RedirectTarget(
                host_name=domain_bucket.bucket_name,
                protocol=s3.RedirectProtocol.HTTP
            )
        )

        s3_deployment.BucketDeployment(
            self,
            "bucket-deployment",
            sources=[s3_deployment.Source.asset("../personal-website/build")],
            destination_bucket=domain_bucket
        )

        zone = route53.HostedZone.from_lookup(
            self,
            "hosted-zone",
            domain_name="jennproos.com"
        )

        route53.ARecord(
            self,
            "a-record",
            target=route53.RecordTarget.from_alias(route53_targets.BucketWebsiteTarget(domain_bucket)),
            zone=zone
        )
