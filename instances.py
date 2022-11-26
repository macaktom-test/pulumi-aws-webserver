import pulumi
import pulumi_aws as aws
import inst_properties as inst_prop

cfg = pulumi.Config()
inst_data = cfg.require_object("webserver_ec2_inst")


web_server_inst = aws.ec2.Instance(
    "web-server-inst",
    ami = inst_prop.ubuntu_ami.id,
    instance_type = inst_data.get("type"),
    key_name = inst_data.get("key_name"),
    network_interfaces = [aws.ec2.InstanceNetworkInterfaceArgs(
      device_index = 0,
      network_interface_id = inst_prop.web_server_nic.id
    )],
    user_data = inst_prop.web_server_user_data,
    tags = {
        'Name': inst_data.get("name"),
    }
)