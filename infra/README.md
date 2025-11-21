
# Welcome to your CDK Python project!

## Prerequisites

Before getting started, ensure you have the following installed:
- **Python 3.13+**
- **Node.js and npm** (for AWS CDK CLI)
- **AWS CLI** configured with appropriate credentials

## Setup Instructions

### 1. Install AWS CDK CLI

The AWS CDK CLI is a Node.js package. Install it locally in the project:

```bash
$ npm install
```

This will install the CDK CLI (version specified in `package.json`) locally in the `node_modules` directory.

To run CDK commands, use `npx`:

```bash
$ npx cdk --version    # Verify installation
$ npx cdk diff         # Compare deployed stack with current state
$ npx cdk deploy       # Deploy the stack
```

**Optional:** Create an alias for convenience:
```bash
$ alias cdk="npx cdk"
```

### 2. Set Up Python Virtual Environment

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project. The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory. To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```bash
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```bash
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```bash
$ pip install -r requirements.txt
```

### 3. Synthesize CloudFormation Template

At this point you can now synthesize the CloudFormation template for this code.

```bash
$ npx cdk synth
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

 * `npx cdk ls`          list all stacks in the app
 * `npx cdk synth`       emits the synthesized CloudFormation template
 * `npx cdk deploy`      deploy this stack to your default AWS account/region
 * `npx cdk diff`        compare deployed stack with current state
 * `npx cdk docs`        open CDK documentation
