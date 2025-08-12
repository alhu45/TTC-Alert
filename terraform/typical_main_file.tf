# Typical Structure Order
# Terraform block (required providers, versions)
# Provider block (AWS, Kubernetes, GCP, etc.)
# Variables & locals (optional for DRY code)
# Resources (Deployments, Services, Buckets, etc.)
# Data sources (pulling info from existing infra)
# Outputs (what Terraform prints after apply)


##########################
# 1. Provider
##########################
terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
  required_version = ">= 1.0.0"
}

provider "kubernetes" {
  config_path = "~/.kube/config" # Path to kubeconfig (adjust for cloud providers)
}

##########################
# 2. Variables & Locals (optional)
##########################
# Variables are normally in variables.tf, but you can inline if small.
variable "app_name" {
  type    = string
  default = "my-app"
}

locals {
  labels = {
    app = var.app_name
  }
}

##########################
# 3. Resources
##########################

# Example: Deployment
resource "kubernetes_deployment" "app" {
  metadata {
    name   = var.app_name
    labels = local.labels
  }
  spec {
    replicas = 1
    selector {
      match_labels = local.labels
    }
    template {
      metadata {
        labels = local.labels
      }
      spec {
        container {
          name  = var.app_name
          image = "nginx:latest"

          port {
            container_port = 80
          }
        }
      }
    }
  }
}

# Example: Service
resource "kubernetes_service" "app" {
  metadata {
    name = var.app_name
  }
  spec {
    selector = local.labels
    port {
      port        = 80
      target_port = 80
    }
    type = "NodePort"
  }
}

##########################
# 4. Config / Secrets (if needed)
##########################
resource "kubernetes_config_map" "app_config" {
  metadata {
    name = "${var.app_name}-config"
  }
  data = {
    ENV = "production"
  }
}

resource "kubernetes_secret" "app_secrets" {
  metadata {
    name = "${var.app_name}-secrets"
  }
  data = {
    API_KEY = base64encode("myapikey")
  }
  type = "Opaque"
}

##########################
# 5. Outputs (optional)
##########################
output "service_ip" {
  value = kubernetes_service.app.spec[0].cluster_ip
}


