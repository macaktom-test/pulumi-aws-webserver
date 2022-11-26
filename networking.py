import pulumi
import pulumi_aws as aws


cfg = pulumi.Config()

vpc = aws.ec2.Vpc(
    'main-vpc',
    cidr_block=cfg.require("vpc_cidr"),
    tags={
        'Name': cfg.require("vpc_name")
    }
)

main_gw = aws.ec2.InternetGateway(
          'gw',
          vpc_id = vpc.id,
          tags = {
          'Name': cfg.require("igw_name")
    }     
)

route_table = aws.ec2.RouteTable(
   'main-route-table',
    vpc_id = vpc.id,
    routes = [
        aws.ec2.RouteTableRouteArgs(
            cidr_block = '0.0.0.0/0',
            gateway_id = main_gw.id
        ),
        aws.ec2.RouteTableRouteArgs(
            ipv6_cidr_block='::/0',
            gateway_id = main_gw.id
        )
    ],
    tags={
        'Name': cfg.require("pub_route_table_name")
    }
)

main_subnet = aws.ec2.Subnet(
        'main-subnet1',
        vpc_id = vpc.id,
        cidr_block = cfg.require("public_subnet_cidr"),
        tags={
        'Name': cfg.require("public_subnet_name")
    }
)

main_route_table_assoc = aws.ec2.RouteTableAssociation(
   "main-route-assoc",
    subnet_id = main_subnet.id,
    route_table_id = route_table.id
)

sg_allow_web = aws.ec2.SecurityGroup(
    "allow_web",
    description = "Allow Web inbound traffic - only for testing",
    vpc_id = vpc.id,
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        description = 'HTTPS from VPC',
        from_port = 443,
        to_port = 443,
        protocol = 'tcp',
        cidr_blocks = ['0.0.0.0/0'],
        ipv6_cidr_blocks = ['::/0'],
    ),aws.ec2.SecurityGroupIngressArgs(
        description = 'HTTP from VPC',
        from_port = 80,
        to_port = 80,
        protocol = 'tcp',
        cidr_blocks = ['0.0.0.0/0'],
        ipv6_cidr_blocks = ['::/0'],
    ),aws.ec2.SecurityGroupIngressArgs(
        description = 'SSH from VPC',
        from_port = 22,
        to_port = 22,
        protocol = 'tcp',
        cidr_blocks = ['0.0.0.0/0'],
        ipv6_cidr_blocks = ['::/0'],
    )],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        from_port = 0,
        to_port = 0,
        protocol = '-1',
        cidr_blocks = ['0.0.0.0/0'],
        ipv6_cidr_blocks = ['::/0'],
    )],
    tags={
        'Name': cfg.require("web_sec_grp_name")
    }
)