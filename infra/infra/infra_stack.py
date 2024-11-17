from aws_cdk import (
    CfnOutput,
    Stack,
    aws_apigateway as apigateway,
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_s3 as s3,
    aws_secretsmanager as secretsmanager,
    aws_ses as ses
)
from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, stack_name="PersonalWebsiteInfraStack", **kwargs)

        website_bucket = s3.Bucket(
            self,
            "website-bucket",
            bucket_name="www.jennproos.com",
            public_read_access=True,
            website_index_document="index.html"
        )

        github_deployment_user = iam.User(
            self,
            "github-deployment-user",
            user_name="github-deployment-user"
        )

        github_deployment_user.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:ListBucket",
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:PutBucketWebsite"
                ],
                resources=[
                    website_bucket.bucket_arn,
                    f"{website_bucket.bucket_arn}/*"
                ]
            )
        )

        access_key = iam.AccessKey(self, "github-deployment-user-secret-access-key", user=github_deployment_user)
        CfnOutput(self, "github-deployment-user-access-key-id", value=access_key.access_key_id)

        secretsmanager.Secret(
            self,
            "github-deployment-user-secret-access-key-secret",
            secret_name="github-deployment-user-secret-access-key-secret",
            secret_string_value=access_key.secret_access_key
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
            domain_names=["www.jennproos.com"],
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(website_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            certificate=certificate
        )

        www_record = route53.ARecord(
            self,
            "a-record-www",
            record_name="www",
            target=route53.RecordTarget.from_alias(route53_targets.CloudFrontTarget(distribution)),
            zone=zone
        )

        # TODO: Route this to www record
        route53.ARecord(
            self,
            "a-record",
            target=route53.RecordTarget.from_alias(route53_targets.Route53RecordTarget(www_record)),
            zone=zone
        )

        my_email = "jennproos@gmail.com"

        ses.EmailIdentity(
            self,
            "email-identity",
            identity=ses.Identity.email(my_email)
        )

        contact_me_api = apigateway.RestApi(
            self,
            "contact-me-api",
            rest_api_name="Contact Me Service",
            description="This service will send e-mails to me from the contact form",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS
            )
        )

        handler = lambda_.Function(
            self,
            "send-email-function",
            function_name="send-email-function",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("resources"),
            handler="send_email.handler",
            environment={
                "MY_EMAIL": my_email
            }
        )

        handler.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "ses:SendEmail",
                    "ses:SendRawEmail"
                ],
                resources=["*"]
            )
        )

        send_email_integration = apigateway.LambdaIntegration(
            handler,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        contact_me_api.root.add_method("POST", send_email_integration)
