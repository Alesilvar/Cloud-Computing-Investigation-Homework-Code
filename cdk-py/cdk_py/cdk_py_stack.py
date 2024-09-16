from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput,
    CfnTag,
    Environment
)
from constructs import Construct

class CdkEc2Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Basic VPC
        vpc = ec2.Vpc(
            self,
            "MyVpc",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public-subnet-1",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                )
            ],
        )

        # Create Security Group
        sec_group = ec2.SecurityGroup(
            self, "MySecurityGroup", vpc=vpc, allow_all_outbound=True
        )

        # Create Security Group Ingress Rule
        sec_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow SSH access"
        )

        # Import existing key pair
        key_pair = ec2.KeyPair.from_key_pair_name(self, "KeyPair", "vockey")

        # Create EC2 instance
        instance = ec2.Instance(
            self,
            "MyInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            vpc=vpc,
            security_group=sec_group,
            associate_public_ip_address=True,
            key_name=key_pair.key_pair_name,
        )

        # Output Instance ID
        CfnOutput(self, "InstanceId", value=instance.instance_id)
