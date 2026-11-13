# AWS Region where all resources (VPC, EC2, SG) will be provisioned
variable "aws_region" {
  type        = string
  description = "AWS region for deployment"
  default     = "us-east-1"
}

# EC2 Compute instance sizing (t3.micro has 2 vCPUs, 1 GiB RAM, Free Tier eligible)
variable "instance_type" {
  type        = string
  description = "AWS EC2 instance type"
  default     = "t3.micro"
}

# EC2 SSH Key Pair name created in your AWS Console
variable "key_name" {
  type        = string
  description = "AWS EC2 Key Pair name for SSH access"
  default     = "skills-tracker-key"
}

# Firewall rule: CIDR block allowed to connect to SSH port 22
variable "allowed_ssh_cidr" {
  type        = string
  description = "CIDR block permitted for SSH access"
  default     = "0.0.0.0/0"
}
