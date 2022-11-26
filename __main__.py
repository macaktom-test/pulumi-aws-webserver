"""An AWS Python Pulumi program for testing out Pulumi"""

import pulumi
import pulumi_aws as aws
import instances as inst
import inst_properties as inst_prop
import networking as net


cfg = pulumi.Config()

web_server_eip = aws.ec2.Eip(
    'web-server-eip',
    vpc = True,
    network_interface = inst_prop.web_server_nic.id,
    instance = inst.web_server_inst.id,
    opts = pulumi.ResourceOptions(depends_on=[net.main_gw]),
    tags={
      'Name': cfg.require("eip_name")
    }
  )


pulumi.export("web-server-inst-public-ip", web_server_eip.public_ip)
pulumi.export("web-server-az", inst.web_server_inst.availability_zone)