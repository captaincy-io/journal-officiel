ui            = true
disable_mlock = true
cluster_addr  = "http://{{ GetPrivateIP }}:8201"
api_addr      = "http://{{ GetPrivateIP }}:8200"
log_level     = "error"

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}

storage "raft" {
  path = "/vault/file"

  retry_join {
    leader_api_addr = "http://vault-server-1:8200"
  }

  retry_join {
    leader_api_addr = "http://vault-server-2:8200"
  }

  retry_join {
    leader_api_addr = "http://vault-server-3:8200"
  }
}
