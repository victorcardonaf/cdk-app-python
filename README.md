
# cdk-app-python

This project creates CDK app with an instance of a stack (`my_first_cdk_app_stack`)
which creates a simple `EKS cluster`, a `SSM parameter` with the value `development`, `staging` and `production`, a `custom resource` 
backed by a `lambda function` that returns a value based on the environment from ssm and then, as a final step, it creates a nginx `helm chart` 
that uses this returned value as parameter to define the replicas.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

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

**NOTE**: Please take into account that you need to execute the pip command from the virtual 
enviroment, instead of the one configured in your machine globally.
```
$ pip install -r requirements.txt
```


## CDK Execution ##

You need to configure your AWS credentials

-> On Mac/Linux: ~/.aws/credentials

-> On Windows: C:\Users\username\.aws\credentials

Use this link as reference -> https://docs.aws.amazon.com/powershell/latest/userguide/specifying-your-aws-credentials.html

At this point you can now synthesize the CloudFormation template for this code. This project should be executed using a parameter
from `development`, `staging` and `production`


To verify composition of template:
```
$ cdk synth --parameters environment=development
```


To create resources:
```
$ cdk deploy --parameters environment=production
```


There is a test configured that you can execute as well:
```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
# cdk-app-python
