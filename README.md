# lambdamanager

A command to help you to manage aws lambda functions.

These aws lambda runtimes are supported by now:
  - python2.7

[![Build Status](https://travis-ci.org/AudienseCo/lambdamanager.svg?branch=master)](https://travis-ci.org/AudienseCo/lambdamanager)

## Installation

Using pip:

```
pip install git+https://github.com/AudienseCo/lambdamanager
```

*This package is going to be published in pypi. By now, use this install method.*

**Tip:** Install the manager in a isolated virtualenv and link the command `lambdamanager` into the bin directory in your home.

## Upgrade

Using pip:

```
pip install --upgrade git+https://github.com/AudienseCo/lambdamanager
```

## AWS Credentials setup

The login is based in boto, so it is compatible with the procedure in [aws-cli package](https://github.com/aws/aws-cli#getting-started)

## Function setup

We need to create the function setup definition. The default name used by the command is `functions.yml`, and it support more than one function in the same file.

### The functions.yml file structure

This is a example with only one function, based on the [function_sample](https://github.com/AudienseCo/lambdamanager/tree/master/tests/assets/function_sample) in tests directory. The file use yaml format.

```YAML
---
function-one:
  Runtime: python2.7
  Role: arn:aws:iam::000000000000:role/lambda_basic_execution
  Handler: function_one.lambda_handler
  Description: A function example for tests
  Code:
     S3Bucket: bucket_with_code
     S3KeyPath: function_one
     Directory: function_one
  MemorySize: 128
  Timeout: 30
  VpcConfig:
      SubnetIds:
          - subnet-0000000
      SecurityGroupIds:
          - sg-00000000
  Environment:
    Variables:
      S3_BUCKET: writable_bucket
      S3_FILENAME: example/timestamp
```

The function description is very similar to the one used by aws-cli. The block `function-name.Code` has been customized with the entry, `Directory`. This is where the function code is in your system. Usualy the code directory is a child directory of the directory with `functions.yml` like next example:

```
myfunctions/
   functions.yml
   function_one/
       function_one.py
       __init__.py
       requirements.txt
```

## The lambdamanager command

```
Usage: lambdamanager [-c FILE] <command> [<args>...]

-h --help           show this
-c --config FILE    The function config file [default: ./functions.yml]

These are the available commands:

 create: Create lambda functions in AWS service.
 create_package: create the zip package without publish it.
 create_release: Create a new release for the selected lambda function.
 list_aliases: List the available aliases for a given function.
 invoke: Execute the remote function code .
 promote_release: Update the alias named 'production'.
 update_config: Update the function configuration.

See 'lambdamanager help <command>' for more information on a specific command.
```

### Python runtime

If there is a file named `requirements.txt` in the top level of code directory, `pip install -r requirements.txt --target .` is going to be launched in the temporary directory created to pack the code.


