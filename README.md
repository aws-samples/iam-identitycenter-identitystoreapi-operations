# AWS IAM Identity Center User and Group API Operations

This project provides examples and sample code to manage and audit AWS IAM identity store User and Group operations at scale using APIs. With these APIs, you can build automation workflows to:
    1. Provision and de-provision users and groups 
    2. Add new members to a group or remove them from a group
    3. Query information about users and groups in IAM Identity Center
    4. Update information about these users and groups
    5. Find out which users are members of which groups

## Prerequisites

Before you start you should have the following prerequisites:
    1. An Organization in AWS Organizations
    2. Administrative access to the AWS IAM Identity Center
    3. Python version 3.10.5 or later
    4. AWS CLI

## Environment Setup

Clone this repo:

```
git clone https://github.com/aws-samples/iam-identitycenter-identitystoreapi-operations

```

## Test

Here is an example to see all supported operations available in the sample script.

```
python identitystore_operations.py —h

*Sample Output:*
usage: identitystore_operations.py [-h]
                                   {create_user,create_group,adduser_to_group,delete_group,list_members,list_membership}
                                   ...
positional arguments:
  {create_user,create_group,adduser_to_group,delete_group,list_members,list_membership}

options:
  -h, --help            show this help message and exit

```

## AWS IAM Identity Center User and Group API Operations

Here is an example of how you can create a new user “John Doe” in the IAM Identity Center identity store and add the user to an existing “AWS_Data_Science” Group.

```
python identitystore_operations.py create_user --identitystoreid d-123456a7890 --username johndoe --givenname John --familyname Doe --groupname AWS_SSO_Data_Science

*Sample Output:*
User:johndoe with UserId:94482488-3041-7026-18f3-be45837cd0e4 created successfully
User:johndoe added to Group:AWS_Data_Science successfully
```

Now, consider the data scientist transitions to an applied scientist role and needs access to additional AWS applications and resources. Previously, you had to manually update their information and add them to the “AWS_Applied_Scientists” group so they get the right access. Now, your automation can update the user and provide them with the access they need. 
 
Here is an example of how a previously created user “John Doe” can be added to“AWS_Applied_Scientists” group

```
python identitystore_operations.py adduser_to_group --identitystoreid d-123456a7890 --groupname AWS_SSO_Applied_Scientists --username johndoe

*Sample Output:*
User:johndoe added to Group:AWS_Applied_Scientists successfully
```

## AWS IAM Identity Center User and Group Audit Operations

Here is an example of how you can find all members of “AWS_Applied_Scientists” group

```
python identitystore_operations.py list_members --identitystoreid d-123456a7890 --groupname AWS_SSO_Applied_Scientists 

*Sample Output:*
UserName:johndoe,Display Name: John Doe 
```

Here is an example of how you can find group memberships of a specific user “johndoe”

```
python identitystore_operations.py list_membership --identitystoreid d-123456a7890 --username johndoe

*Sample Output*
User :johndoe is a member of the following groups
AWS_Data_Science
AWS_Applied_Scientists
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

