import pulumi
import pulumi_aws as aws
import networking as net


cfg = pulumi.Config()
webserver_prop = cfg.require_object("webserver_ec2_inst")


ubuntu_ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["099720109477"],
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
        )]
)

web_server_nic = aws.ec2.NetworkInterface(
    'web-server-nic',
    subnet_id = net.main_subnet.id,
    private_ips = [webserver_prop.get("priv_ip")],
    security_groups = [net.sg_allow_web.id],
)

web_server_user_data = """
#!/bin/bash
sudo apt update -y
sudo apt install nginx -y
sudo systemctl start nginx
"""

