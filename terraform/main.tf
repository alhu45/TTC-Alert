# Tells Terraform, to talk to local kubeconfig file
provider "kubernetes" {
  config_path = "~/.kube/config"
}

# SMS Server Deployment
resource "kubernetes_deployment" "sms_server" {
  metadata {
    name = "sms-server"
    labels = {
      app = "sms-server"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "sms-server"
      }
    }

    template {
      metadata {
        labels = {
          app = "sms-server"
        }
      }

      spec {
        container {
          name  = "sms-server"
          image = "alhu45/sms-server:latest"

          port {
            container_port = 4000
          }

          env_from {
            config_map_ref {
              name = "sms-config"
            }
          }

          env_from {
            secret_ref {
              name = "sms-secrets"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "sms_server" {
  metadata {
    name = "sms-server"
  }

  spec {
    selector = {
      app = "sms-server"
    }

    port {
      port        = 4000
      target_port = 4000
    }

    type = "NodePort"
  }
}

# ETL Deployment
resource "kubernetes_deployment" "etl" {
  metadata {
    name = "etl"
    labels = {
      app = "etl"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "etl"
      }
    }

    template {
      metadata {
        labels = {
          app = "etl"
        }
      }

      spec {
        container {
          name  = "etl"
          image = "alhu45/etl:latest"

          port {
            container_port = 5000
          }

          env_from {
            config_map_ref {
              name = "etl-config"
            }
          }

          env_from {
            secret_ref {
              name = "etl-secrets"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "etl" {
  metadata {
    name = "etl"
  }

  spec {
    selector = {
      app = "etl"
    }

    port {
      port        = 5000
      target_port = 5000
    }

    type = "NodePort"
  }
}

##########################
# ConfigMaps
##########################

resource "kubernetes_config_map" "sms_config" {
  metadata {
    name = "sms-config"
  }

  data = {
    FLASK_ENV     = "production"
    TWILIO_NUMBER = var.twilio_number
    TARGET_PHONE  = var.target_phone
  }
}

resource "kubernetes_config_map" "etl_config" {
  metadata {
    name = "etl-config"
  }

  data = {
    FLASK_ENV               = "production"
    KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
    MONGO_URI               = "mongodb://mongo:27017"
    TWILIO_NUMBER           = var.twilio_number
    TARGET_PHONE            = var.target_phone
  }
}

# Secrets
resource "kubernetes_secret" "sms_secrets" {
  metadata {
    name = "sms-secrets"
  }

  data = {
    TWILIO_SID    = base64encode(var.twilio_sid)
    TWILIO_TOKEN  = base64encode(var.twilio_token)
    TWILLIO_OTHER = base64encode(var.twilio_other)
  }

  type = "Opaque"
}

resource "kubernetes_secret" "etl_secrets" {
  metadata {
    name = "etl-secrets"
  }

  data = {
    TRANSIT_API   = base64encode(var.transit_api)
    MONGODB       = base64encode(var.mongodb_uri)
    TWILIO_SID    = base64encode(var.twilio_sid)
    TWILIO_TOKEN  = base64encode(var.twilio_token)
    TWILLIO_OTHER = base64encode(var.twilio_other)
  }

  type = "Opaque"
}
