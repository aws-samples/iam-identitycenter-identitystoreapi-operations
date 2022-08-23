#Python program for AWS Identity store User and Group Management
import argparse
import json
import boto3

client = boto3.client('identitystore')


def create_user(args):
    """ 
    This function creates a user and add the user to the group if the group exists.
    - If the group does not exists , this function will create only the user and skip adding user to the group
    
    Note: Uses the region set in the default profile or shell environment
    
    Required parameters
    -------------------
    --identitystoreid - Identity Store Id of SSO configuration
    --username  - User Name for the user
    --givenname - First Name for the user
    --familyname - Last Name for the user

    Optional parameters
    -------------------
    --groupname - Name of the SSO group
        
    Response
    --------
    None

    
    """
    sso_id_storeid = args.identitystoreid
    user_name = args.username
    given_name = args.givenname
    family_name = args.familyname
    group_name = args.groupname
    display_name = "{} {}".format(given_name, family_name)
    create_user_response = client.create_user(
        IdentityStoreId=sso_id_storeid,
        UserName=user_name,
        Name={
            'FamilyName': family_name,
            'GivenName': given_name
        },
        DisplayName=display_name
    )
    user_id = create_user_response["UserId"]
    print("User:{} with UserId:{} created successfully".format(
        user_name, create_user_response["UserId"]))
    group_exists = True
    if group_name:
        try:
            get_group_id_response = client.get_group_id(
                AlternateIdentifier={
                    'UniqueAttribute': {
                        'AttributePath': 'displayName',
                        'AttributeValue': group_name
                    }
                },
                IdentityStoreId=sso_id_storeid
            )
        except client.exceptions.ResourceNotFoundException as e:
            print("Group Name {} does not exists, Skipping adding user to group".format(
                group_name))
            group_exists = False
    if group_exists:
        create_group_membership_response = client.create_group_membership(
            GroupId=(get_group_id_response["GroupId"]),
            IdentityStoreId=sso_id_storeid,
            MemberId={
                'UserId': user_id
            }
        )
        
        print("User:{} added to Group:{} successfully".format(
            user_name, group_name))


def create_group(args):
    """ 
    This function creates a group
    
    Note: Uses the region set in the default profile or shell environment
    
    Required parameters
    -------------------
    --identitystoreid - Identity Store Id of SSO configuration
    --groupname - Name of the Group
    --description - Description of the Group

    Response
    --------
    None
    """
    sso_id_storeid = args.identitystoreid
    display_name = args.groupname
    desc = args.description
    create_group_response = client.create_group(
        IdentityStoreId=sso_id_storeid,
        DisplayName=display_name,
        Description=desc
    )
    print("Group:{} with GroupId:{} created successfully".format(
        display_name, create_group_response["GroupId"]))


def adduser_to_group(args):
    """ 
    This function adds user to an existing group.
    
    Note: Uses the region set in the default profile or shell environment
    
    Required parameters
    -------------------
    --identitystoreid - Identity Store Id of SSO configuration
    --groupname - Name of the Group
    --username - Name of the User

    Response
    --------
    None
    """
    sso_id_storeid = args.identitystoreid
    user_name = args.username
    group_name = args.groupname
    get_group_id_response = client.get_group_id(
        IdentityStoreId=sso_id_storeid,
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'displayName',
                'AttributeValue': group_name
            }
        },
    )
    group_id = get_group_id_response["GroupId"]
    get_user_id_response = client.get_user_id(
        IdentityStoreId=sso_id_storeid,
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'userName',
                'AttributeValue': user_name
            }
        },
    )
    user_id = get_user_id_response['UserId']
    create_group_membership_response = client.create_group_membership(
        GroupId=group_id,
        IdentityStoreId=sso_id_storeid,
        MemberId={
            'UserId': user_id
        }
    )
    print("User:{} added to Group:{} successfully".format(user_name, group_name))


def delete_group(args):
    """ 
    This function deletes an existing SSO group

    Note: Uses the region set in the default profile or shell environment
    
    Required parameters
    -------------------
    --identitystoreid - Identity Store Id of SSO configuration
    --groupname - Name of the Group

    Response
    --------
    None
    """
    sso_id_storeid = args.identitystoreid
    group_name = args.groupname
    get_group_id_response = client.get_group_id(
        IdentityStoreId=sso_id_storeid,
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'displayName',
                'AttributeValue': group_name
            }
        },
    )
    group_id = format(get_group_id_response["GroupId"])
    delete_group_response = client.delete_group(
        IdentityStoreId=sso_id_storeid,
        GroupId=group_id
    )
    print("Group:{} with GroupId:{} deleted successfully".format(group_name, group_id))


def list_members(args):
    """ 
    This function list members of a group

    Note: Uses the region set in the default profile or shell environment
    
    Required parameters
    -------------------
    --identitystoreid - Identity Store Id of SSO configuration
    --groupname - Name of the Group

    Response
    --------
    None
    """
    sso_id_storeid = args.identitystoreid
    group_name = args.groupname
    get_groupid_response = client.get_group_id(
        IdentityStoreId=sso_id_storeid,
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'displayName',
                'AttributeValue': group_name
            }
        },
    )
    group_id = get_groupid_response["GroupId"]
    list_group_memberships_response = client.list_group_memberships(
        IdentityStoreId=sso_id_storeid,
        GroupId=group_id,
        MaxResults=100,
    )
    group_membership_response = list_group_memberships_response["GroupMemberships"]
    for group_membership in group_membership_response:
        member_id = format(group_membership["MemberId"]["UserId"])
        describe_user_response = client.describe_user(
            IdentityStoreId=sso_id_storeid,
            UserId=member_id
        )
        print(describe_user_response)
        print("UserName:{},Display Name: {} ".format(
            describe_user_response["UserName"], describe_user_response["DisplayName"]))


def list_membership(args):
    """ 
    This function lists user's group membership. 

    Note: Uses the region set in the default profile or shell environment
    
    Required parameters
    -------------------
    --identitystoreid - Identity Store Id of SSO configuration
    --username - Name of the User

    Response
    --------
    None
    """
    sso_id_storeid = args.identitystoreid
    user_name = args.username
    get_user_id_response = client.get_user_id(
        IdentityStoreId=sso_id_storeid,
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'userName',
                'AttributeValue': user_name
            },
        },
    )
    user_id = get_user_id_response["UserId"]
    list_group_memberships_for_member_response = client.list_group_memberships_for_member(
        IdentityStoreId=sso_id_storeid,
        MemberId={
            'UserId': user_id
        },
    )
    group_membership_response = list_group_memberships_for_member_response["GroupMemberships"]
    for group_membership in group_membership_response:
        group_id = format(group_membership["GroupId"])
        describe_group_response = client.describe_group(
            IdentityStoreId=sso_id_storeid,
            GroupId=group_id,
        )
        group_names = describe_group_response["DisplayName"]
        print(group_names)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    #sub-parsers for creating a new user in IAM Identity Store
    create_user_parser = subparsers.add_parser('create_user')
    create_user_parser.add_argument(
        '--identitystoreid', required=True, help="Identity Store Id for IAM Identity Center Directory Configuration")
    create_user_parser.add_argument(
        '--username', required=True, help="User Name for the user")
    create_user_parser.add_argument(
        '--givenname', required=True, help="First Name for the user")
    create_user_parser.add_argument(
        '--familyname', required=True, help="Last Name for the user")
    create_user_parser.add_argument(
        '--groupname', help="if provided and valid, the newly created user will be added to group")
    create_user_parser.set_defaults(func=create_user)

    #sub-parser for creating a new group in IAM Identity Store
    create_group_parser = subparsers.add_parser('create_group')
    create_group_parser.add_argument('--identitystoreid', required=True, help="Identity Store Id for IAM Identity Center Directory Configuration")
    create_group_parser.add_argument('--groupname', required=True, help="Name of the Group")
    create_group_parser.add_argument('--description', required=True, help="Group Description")
    create_group_parser.set_defaults(func=create_group)

    #sub-parser for adding an existing user to the group in IAM Identity Store
    adduser_to_group_parser = subparsers.add_parser('adduser_to_group')
    adduser_to_group_parser.add_argument('--identitystoreid', required=True, help="Identity Store Id for IAM Identity Center Directory Configuration")
    adduser_to_group_parser.add_argument('--groupname', required=True, help="Name of the group")
    adduser_to_group_parser.add_argument('--username', required=True, help="Name of the user")
    adduser_to_group_parser.set_defaults(func=adduser_to_group)

    #sub-parser for deleting a group in IAM Identity Store
    delete_group_parser = subparsers.add_parser('delete_group')
    delete_group_parser.add_argument('--identitystoreid', required=True, help="Identity Store Id for IAM Identity Center Directory Configuration")
    delete_group_parser.add_argument('--groupname', required=True, help="Name of the group")
    delete_group_parser.set_defaults(func=delete_group)

    #sub-parser for Listing members of a group in IAM Identity Store
    list_members_parser = subparsers.add_parser('list_members')
    list_members_parser.add_argument('--identitystoreid', required=True, help="Identity Store Id for IAM Identity Center Directory Configuration")
    list_members_parser.add_argument('--groupname', required=True, help="Name of the group")
    list_members_parser.set_defaults(func=list_members)

    #sub-parser for Listing User's group membership in IAM Identity Store
    list_membership_parser = subparsers.add_parser('list_membership')
    list_membership_parser.add_argument('--identitystoreid', required=True, help="Identity Store Id for IAM Identity Center Directory Configuration")
    list_membership_parser.add_argument('--username', required=True, help="Name of the user")
    list_membership_parser.set_defaults(func=list_membership)
    args = parser.parse_args()
    args.func(args)
