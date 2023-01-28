from aws_cdk import (
    Stack,
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
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

        certificate = acm.Certificate(
            self,
            "certificate",
            domain_name="*.jennproos.com",
            subject_alternative_names=["jennproos.com"],
            certificate_name="Jenn Proos Website",
            validation=acm.CertificateValidation.from_dns(zone)
        )

        distribution = cloudfront.Distribution(
            self,
            "distribution",
            domain_names=["jennproos.com", "www.jennproos.com"],
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(domain_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            certificate=certificate
        )

        route53.ARecord(
            self,
            "a-record",
            target=route53.RecordTarget.from_alias(route53_targets.CloudFrontTarget(distribution)),
            zone=zone
        )

        route53.ARecord(
            self,
            "a-record-www",
            record_name="www",
            target=route53.RecordTarget.from_alias(route53_targets.CloudFrontTarget(distribution)),
            zone=zone
        )
