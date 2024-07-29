terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.60.0"
    }
  }

  cloud {
    organization = "captaincy"

    workspaces {
      name = "production"
    }
  }

  required_version = ">= 1.5"
}

provider "aws" {
  region  = "eu-west-3" # Paris
}