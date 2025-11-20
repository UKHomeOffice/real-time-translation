variable "region" {
  type        = string
  description = "AWS Region Name"
  default     = "eu-west-2"
}

variable "project" {
  type        = string
  description = "Name of project"
  default     = "real-time-translation"
}

variable "account_number" {
  type        = string
  description = "AWS Account Number"
}

variable "whisper_endpoint_gpu" {
  description = "Whether Whisper Endpoint should be deployed with GPU or CPU"
  type        = bool
  default     = false
}
