# 1. The public IPv4 address of the EC2 instance
output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.web.public_ip
}

# 2. The public DNS hostname assigned by AWS
output "instance_public_dns" {
  description = "Public DNS hostname of the EC2 instance"
  value       = aws_instance.web.public_dns
}

# 3. Web URL ready to open in a browser
output "web_url" {
  description = "HTTP URL to access the Skills Tracker application"
  value       = "http://${aws_instance.web.public_ip}"
}

# 4. Ready-to-copy SSH command helper
output "ssh_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh -i ~/.ssh/${var.key_name}.pem ubuntu@${aws_instance.web.public_ip}"
}
