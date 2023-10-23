variable "image_name" {
  type        = string
  description = "image:tag used for cloud run deployment"
}
variable "domain_name" {
  type        = string
  description = "verified domain name for your cloud run service"
  default     = ""
}
