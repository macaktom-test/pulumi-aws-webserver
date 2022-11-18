"""An AWS Python Pulumi program for testing out Pulumi"""

import pulumi
import pulumi_aws as aws


web_server_priv_ip = "10.0.1.50"

prod_vpc = aws.ec2.Vpc(
    'prod-vpc',
    cidr_block='10.0.0.0/16',
    tags={
        'Name': 'prod-vpc',
    }
)

main_gw = aws.ec2.InternetGateway(
          'gw',
          vpc_id = prod_vpc.id,
          tags = {
          'Name': 'main-gw'
    }     
)

prod_route_table = aws.ec2.RouteTable(
   'prod-route-table',
    vpc_id = prod_vpc.id,
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
        'Name': 'prod-route-table',
    }
)

prod_subnet = aws.ec2.Subnet(
        'prod-subnet1',
        vpc_id = prod_vpc.id,
        cidr_block = '10.0.1.0/24',
        tags={
        'Name': 'prod-subnet1'
    }
)

prod_route_table_assoc = aws.ec2.RouteTableAssociation(
   "prod-route-assoc",
    subnet_id = prod_subnet.id,
    route_table_id = prod_route_table.id
)

sg_allow_web = aws.ec2.SecurityGroup(
    "allow_web",
    description = "Allow Web inbound traffic - only for testing",
    vpc_id = prod_vpc.id,
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
        'Name': 'allow-web',
    }
)

web_server_nic = aws.ec2.NetworkInterface(
    'web-server-nic',
    subnet_id = prod_subnet.id,
    private_ips = [web_server_priv_ip],
    security_groups = [sg_allow_web.id],
)

web_server_user_data = """
#!/bin/bash
sudo apt update -y
sudo apt install nginx -y
sudo systemctl start nginx
"""

web_server_inst = aws.ec2.Instance(
    "web-server-inst",
    ami = "ami-08c40ec9ead489470",
    instance_type = 't2.micro',
    key_name = "main-key",
    network_interfaces = aws.ec2.InstanceNetworkInterfaceArgs(
      device_index = 0,
      network_interface_id = web_server_nic.id
    ),
    user_data = web_server_user_data,
    tags = {
        'Name': 'web-server',
    }
)

web_server_eip = aws.ec2.Eip(
    'web-server-eip',
    vpc = True,
    instance = web_server_inst.id,
    network_interface = web_server_nic.id,
    associate_with_private_ip = web_server_priv_ip,
    opts = pulumi.ResourceOptions(depends_on=[main_gw])
  )

pulumi.export("web-server-inst-public-ip", web_server_eip.address)