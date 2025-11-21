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
