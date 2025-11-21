
# Welcome to your CDK Python project!

## Pre-deployment Step
The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Testing

This project includes comprehensive infrastructure tests to validate the CDK stack configuration.

### Running Tests

The easiest way to run tests is using the provided script:

```bash
./run-tests.sh
```

This script will:
- Create a virtual environment if it doesn't exist
- Install dependencies automatically
- Run all infrastructure tests

You can also pass pytest arguments to the script:

```bash
./run-tests.sh -k test_s3_bucket_created    # Run specific test
./run-tests.sh -v                            # Verbose output
./run-tests.sh --tb=short                    # Short traceback format
```

### Manual Test Execution

If you prefer to run tests manually:

```bash
source .venv/bin/activate
python -m pytest tests/unit/test_infra_stack.py -v
```

### Test Coverage

The test suite validates:
- S3 bucket configuration (public access, website hosting)
- CloudFront distribution (HTTPS redirect, domain aliases)
- ACM certificate (domain names, validation)
- Route 53 A records (root and www domains)
- Resource counts and removal policies

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
