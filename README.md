# Sample Lambda function with SnappyFlow Tracing (Python)

The project source includes function code and supporting resources:

- `function` - A Python function.
- `template.yml` - An AWS CloudFormation template that creates an application.
- `1-create-bucket.sh`, `2-build-layer.sh`, etc. - Shell scripts that use the AWS CLI to deploy and manage the application.

Use the following instructions to deploy the sample application.

# Requirements
- [Python 3.8](https://www.python.org/downloads/)
- The Bash shell. For Linux and macOS, this is included by default. In Windows 10, you can install the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to get a Windows-integrated version of Ubuntu and Bash.
- [The AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) v1.17 or newer.

If you use the AWS CLI v2, add the following to your [configuration file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) (`~/.aws/config`):

```
cli_binary_format=raw-in-base64-out
```

This setting enables the AWS CLI v2 to load JSON events from a file, matching the v1 behavior.

# Setup
Download or clone this repository.

    $ git clone https://github.com/upendrasahu/aws-lambda-python-tracing-sample.git
    $ cd aws-lambda-python-tracing-sample

To create a new bucket for deployment artifacts, run `1-create-bucket.sh`.

    aws-lambda-python-tracing-sample$ ./1-create-bucket.sh
    make_bucket: lambda-artifacts-a5e491dbb5b22e0d

To build a Lambda layer that contains the function's runtime dependencies, run `2-build-layer.sh`. Packaging dependencies in a layer reduces the size of the deployment package that you upload when you modify your code.

    aws-lambda-python-tracing-sample$ ./2-build-layer.sh

# Deploy
To deploy the application, run `3-deploy.sh`.

    aws-lambda-python-tracing-sample$ ./3-deploy.sh
    Uploading to e678bc216e6a0d510d661ca9ae2fd941  9519118 / 9519118.0  (100.00%)
    Successfully packaged artifacts and wrote output template to file out.yml.
    Waiting for changeset to be created..
    Waiting for stack create/update to complete
    Successfully created/updated stack - aws-lambda-python-tracing-sample

This script uses AWS CloudFormation to deploy the Lambda functions and an IAM role. If the AWS CloudFormation stack that contains the resources already exists, the script updates it with any changes to the template or function code.
# Configure ENV variables
Configure these env variables in AWS lambda function
- PROJECT_NAME: Name of the project in SnappyFlow
- APP_NAME: Name of the application in SnappyFlow
- SF_PROFILE_KEY: Key copied from SnappyFlow Profile

# Test
To invoke the function, run `4-invoke.sh`.

    aws-lambda-python-tracing-sample$ ./4-invoke.sh
    {
        "StatusCode": 200,
        "ExecutedVersion": "$LATEST"
    }
    {"TotalCodeSize": 410713698, "FunctionCount": 45}

Let the script invoke the function a few times and then press `CRTL+C` to exit.

# Cleanup
To delete the application, run `5-cleanup.sh`.

    aws-lambda-python-tracing-sample$ ./5-cleanup.sh
