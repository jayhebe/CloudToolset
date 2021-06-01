from azure.keyvault.secrets import SecretClient


def get_kv_secret(keyvaults_name, secret_name, credential, env="AzurePublicCloud"):
    kv_prefix = "https://{}.vault.azure.net"

    if env == "AzureChinaCloud":
        kv_prefix = "https://{}.vault.azure.cn"

    kv_url = kv_prefix.format(keyvaults_name)
    kv_client = SecretClient(kv_url, credential)

    return kv_client.get_secret(secret_name).value
