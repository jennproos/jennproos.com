import aws_cdk as core
import aws_cdk.assertions as assertions

from infra.infra_stack import InfraStack


# Helper to create test environment
def get_test_env():
    return core.Environment(account='120086452202', region='us-east-1')


def test_s3_bucket_created():
    """Test that S3 bucket is created with correct configuration"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify S3 bucket exists with correct properties
    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketName": "jennproos.com",
        "PublicAccessBlockConfiguration": {
            "BlockPublicAcls": False,
            "BlockPublicPolicy": False,
            "IgnorePublicAcls": False,
            "RestrictPublicBuckets": False
        },
        "WebsiteConfiguration": {
            "IndexDocument": "index.html"
        }
    })


def test_cloudfront_distribution_created():
    """Test that CloudFront distribution is created with correct configuration"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify CloudFront distribution exists
    template.has_resource_properties("AWS::CloudFront::Distribution", {
        "DistributionConfig": {
            "DefaultRootObject": "index.html",
            "Aliases": ["jennproos.com", "www.jennproos.com"],
            "ViewerCertificate": {
                "AcmCertificateArn": assertions.Match.any_value(),
                "SslSupportMethod": "sni-only"
            },
            "DefaultCacheBehavior": {
                "AllowedMethods": ["GET", "HEAD", "OPTIONS"],
                "ViewerProtocolPolicy": "redirect-to-https"
            }
        }
    })


def test_acm_certificate_created():
    """Test that ACM certificate is created with correct domain names"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify certificate exists with correct domains
    template.has_resource_properties("AWS::CertificateManager::Certificate", {
        "DomainName": "jennproos.com",
        "SubjectAlternativeNames": ["www.jennproos.com"],
        "DomainValidationOptions": assertions.Match.any_value()
    })


def test_route53_records_created():
    """Test that Route 53 A records are created for both root and www domains"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify A records are created
    # Should have 2 A records: one for root domain and one for www subdomain
    template.resource_count_is("AWS::Route53::RecordSet", 2)

    # Verify root domain A record
    template.has_resource_properties("AWS::Route53::RecordSet", {
        "Type": "A",
        "AliasTarget": {
            "DNSName": assertions.Match.any_value(),
            "HostedZoneId": assertions.Match.any_value()
        }
    })


def test_stack_has_correct_resource_count():
    """Test that the stack creates the expected number of resources"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify expected resource counts
    template.resource_count_is("AWS::S3::Bucket", 1)
    template.resource_count_is("AWS::CloudFront::Distribution", 1)
    template.resource_count_is("AWS::CertificateManager::Certificate", 1)
    template.resource_count_is("AWS::Route53::RecordSet", 2)


def test_s3_bucket_has_removal_policy():
    """Test that S3 bucket has DESTROY removal policy"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify bucket has deletion policy set to Delete (RemovalPolicy.DESTROY)
    template.has_resource("AWS::S3::Bucket", {
        "DeletionPolicy": "Delete",
        "UpdateReplacePolicy": "Delete"
    })


def test_cloudfront_uses_s3_origin():
    """Test that CloudFront distribution uses S3 as origin"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify CloudFront has an origin configured
    template.has_resource_properties("AWS::CloudFront::Distribution", {
        "DistributionConfig": {
            "Origins": assertions.Match.array_with([
                assertions.Match.object_like({
                    "CustomOriginConfig": assertions.Match.any_value()
                })
            ])
        }
    })


def test_lambda_function_created():
    """Test that Lambda function is created with correct configuration"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify Lambda function exists with correct properties
    template.has_resource_properties("AWS::Lambda::Function", {
        "FunctionName": "send-email-function",
        "Runtime": "python3.13",
        "Handler": "send_email.handler",
        "Environment": {
            "Variables": {
                "MY_EMAIL": "jennproos@gmail.com"
            }
        }
    })


def test_lambda_has_ses_permissions():
    """Test that Lambda function has SES send email permissions"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify IAM role policy allows SES actions
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": assertions.Match.array_with([
                assertions.Match.object_like({
                    "Action": ["ses:SendEmail", "ses:SendRawEmail"],
                    "Effect": "Allow",
                    "Resource": "*"
                })
            ])
        }
    })


def test_api_gateway_created():
    """Test that API Gateway REST API is created with correct configuration"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify API Gateway exists
    template.has_resource_properties("AWS::ApiGateway::RestApi", {
        "Name": "Contact Me Service",
        "Description": "This service will send e-mails to me from the contact form"
    })


def test_api_gateway_has_cors_enabled():
    """Test that API Gateway has CORS configuration"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify OPTIONS method exists (CORS preflight)
    template.has_resource_properties("AWS::ApiGateway::Method", {
        "HttpMethod": "OPTIONS"
    })


def test_api_gateway_post_method_created():
    """Test that API Gateway has POST method integrated with Lambda"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify POST method exists
    template.has_resource_properties("AWS::ApiGateway::Method", {
        "HttpMethod": "POST",
        "Integration": {
            "Type": "AWS_PROXY",
            "IntegrationHttpMethod": "POST"
        }
    })


def test_github_deployment_user_created():
    """Test that GitHub deployment IAM user is created"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify IAM user exists
    template.has_resource_properties("AWS::IAM::User", {
        "UserName": "github-deployment-user"
    })


def test_github_deployment_user_has_s3_permissions():
    """Test that GitHub deployment user has correct S3 permissions"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify IAM policy with S3 permissions exists
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": assertions.Match.array_with([
                assertions.Match.object_like({
                    "Action": [
                        "s3:ListBucket",
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject",
                        "s3:PutBucketWebsite"
                    ],
                    "Effect": "Allow"
                })
            ])
        }
    })


def test_github_deployment_user_access_key_created():
    """Test that access key is created for GitHub deployment user"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify access key exists
    template.has_resource_properties("AWS::IAM::AccessKey", {
        "UserName": assertions.Match.any_value()
    })


def test_secrets_manager_secret_created():
    """Test that Secrets Manager secret is created for access key"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify Secrets Manager secret exists
    template.has_resource_properties("AWS::SecretsManager::Secret", {
        "Name": "github-deployment-user-secret-access-key-secret"
    })


def test_ses_email_identity_created():
    """Test that SES email identity is created"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify SES email identity exists
    template.has_resource_properties("AWS::SES::EmailIdentity", {
        "EmailIdentity": "jennproos@gmail.com"
    })


def test_complete_resource_count():
    """Test that all expected resources are created"""
    app = core.App()
    stack = InfraStack(app, "infra", env=get_test_env())
    template = assertions.Template.from_stack(stack)

    # Verify all resource counts
    template.resource_count_is("AWS::S3::Bucket", 1)
    template.resource_count_is("AWS::CloudFront::Distribution", 1)
    template.resource_count_is("AWS::CertificateManager::Certificate", 1)
    template.resource_count_is("AWS::Route53::RecordSet", 2)
    template.resource_count_is("AWS::Lambda::Function", 1)
    template.resource_count_is("AWS::ApiGateway::RestApi", 1)
    template.resource_count_is("AWS::IAM::User", 1)
    template.resource_count_is("AWS::IAM::AccessKey", 1)
    template.resource_count_is("AWS::SecretsManager::Secret", 1)
    template.resource_count_is("AWS::SES::EmailIdentity", 1)
