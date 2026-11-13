# ==============================================================================
# Step 5: Infrastructure as Code (Terraform)
# Project 01: Python Flask Monolith & Linux Systemd on AWS EC2
# ==============================================================================

# Configure Terraform core settings and required provider plugins
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Configure the AWS Provider targeting the user-defined region
provider "aws" {
  region = var.aws_region
}

# 1. Custom Virtual Private Cloud (VPC) for isolated network infrastructure
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "skills-tracker-vpc"
    Environment = "production"
  }
}

# 2. Internet Gateway (IGW) to enable traffic between VPC and public internet
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "skills-tracker-igw"
  }
}

# 3. Public Subnet where the EC2 instance resides
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}a"

  tags = {
    Name = "skills-tracker-public-subnet"
  }
}

# 4. Route Table sending all 0.0.0.0/0 internet traffic to the Internet Gateway
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "skills-tracker-public-rt"
  }
}

# 5. Associate Route Table with our Public Subnet
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# 6. Security Group (Virtual Firewall at the hypervisor level)
resource "aws_security_group" "web_sg" {
  name        = "skills-tracker-sg"
  description = "Security group for Skills-Tracker Web App"
  vpc_id      = aws_vpc.main.id

  # Allow HTTP traffic on port 80 from anywhere
  ingress {
    description = "Allow HTTP traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow SSH traffic on port 22 from the configured CIDR block
  ingress {
    description = "Allow SSH traffic"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  # Allow all outbound traffic (for OS updates, packages, and telemetry)
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "skills-tracker-sg"
  }
}

# 7. Query the latest official Canonical Ubuntu 24.04 LTS Noble AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical's official AWS Account ID

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# 8. EC2 Virtual Machine Instance hosting the application
resource "aws_instance" "web" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true
  key_name                    = var.key_name != "" ? var.key_name : null

  # Root disk volume configuration (gp3 is modern, baseline 3000 IOPS)
  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    delete_on_termination = true
  }

  # Cloud-init / User Data script: runs automatically on first instance boot
  user_data = <<-EOF
              #!/bin/bash
              set -e

              # Update system packages
              apt-get update -y
              DEBIAN_FRONTEND=noninteractive apt-get install -y \
                python3 \
                python3-pip \
                python3-venv \
                git \
                curl

              # Prepare production directory
              mkdir -p /opt/skills-tracker
              chown -R ubuntu:ubuntu /opt/skills-tracker

              echo "Base system initialization completed." > /var/log/bootstrap.log
              EOF

  tags = {
    Name        = "skills-tracker-web"
    Environment = "production"
  }
}
