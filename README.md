Small project to play around with Pulumi

Same tasks as with terraform project: https://github.com/macaktom-test/terraform-course

Tasks:
1. Create vpc
2. Create Internet Gateway
3. Create Custom Route Table
4. Create a Subnet 
5. Associate subnet with Route Table
6. Create Security Group to allow port 22,80,443
7. Create a network interface with an ip in the subnet that was created in step 4
8. Assign an elastic IP to the network interface created in step 7
9. Setup Nginx server (using EC2 instance) and assign to it network interface, created in step 7
