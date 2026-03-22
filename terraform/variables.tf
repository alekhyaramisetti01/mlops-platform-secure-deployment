variable "location" {
  type    = string
  default = "East US"
}

variable "resource_group_name" {
  type    = string
  default = "rg-secure-ml-platform"
}

variable "aks_cluster_name" {
  type    = string
  default = "aks-secure-ml-platform"
}

variable "node_count" {
  type    = number
  default = 2
}