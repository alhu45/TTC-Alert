# variables.tf

variable "twilio_sid" {
  type      = string
  sensitive = true
}

variable "twilio_token" {
  type      = string
  sensitive = true
}

variable "twilio_number" {
  type = string
}

variable "target_phone" {
  type = string
}

variable "twilio_other" {
  type      = string
  sensitive = true
}

variable "transit_api" {
  type      = string
  sensitive = true
}

variable "mongodb_uri" {
  type      = string
  sensitive = true
}
