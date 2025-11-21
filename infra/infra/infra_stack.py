from aws_cdk import (
    CfnOutput,
    RemovalPolicy,
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

        domain_name = "jennproos.com"
        subdomain = f"www.{domain_name}"

        domain_bucket = s3.Bucket(
            self,
            "DomainBucket",
            bucket_name=domain_name,
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            removal_policy=RemovalPolicy.DESTROY,
            website_index_document="index.html"
        )

        hosted_zone = route53.HostedZone.from_lookup(
            self,
            "HostedZone",
            domain_name=domain_name
        )

        certificate = acm.Certificate(
            self,
            "WebsiteCertificate",
            domain_name=domain_name,
            certificate_name="Personal Website Certificate",
            subject_alternative_names=[subdomain],
            validation=acm.CertificateValidation.from_dns(hosted_zone)
        )

        distribution = cloudfront.Distribution(
            self,
            "SiteDistribution",
            certificate=certificate,
            default_root_object="index.html",
            domain_names=[domain_name, subdomain],
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3StaticWebsiteOrigin(domain_bucket),
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            )
        )

        route53.ARecord(
            self,
            "SiteAliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(route53_targets.CloudFrontTarget(distribution))
        )

        route53.ARecord(
            self,
            "WWWSiteAliasRecord",
            zone=hosted_zone,
            record_name=subdomain,
            target=route53.RecordTarget.from_alias(route53_targets.CloudFrontTarget(distribution))
        )

        my_email = "jennproos@gmail.com"

        ses.EmailIdentity(
            self,
            "EmailIdentity",
            identity=ses.Identity.email(my_email)
        )

        contact_me_api = apigateway.RestApi(
            self,
            "ContactMeApi",
            rest_api_name="Contact Me Service",
            description="This service will send e-mails to me from the contact form",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS
            )
        )

        handler = lambda_.Function(
            self,
            "SendEmailFunction",
            function_name="send-email-function",
            runtime=lambda_.Runtime.PYTHON_3_13,
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

        github_deployment_user = iam.User(
            self,
            "GitHubDeploymentUser",
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
                    domain_bucket.bucket_arn,
                    f"{domain_bucket.bucket_arn}/*"
                ]
            )
        )

        access_key = iam.AccessKey(self, "GitHubDeploymentUserAccessKey", user=github_deployment_user)
        CfnOutput(self, "GitHubDeploymentUserAccessKeyId", value=access_key.access_key_id)

        secretsmanager.Secret(
            self,
            "GitHubDeploymentUserAccessKeySecret",
            secret_name="github-deployment-user-secret-access-key-secret",
            secret_string_value=access_key.secret_access_key
        )

