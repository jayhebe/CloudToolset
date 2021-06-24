from azure.keyvault.secrets import SecretClient


def get_kv_secret(keyvault_name, credential, secret_name=None, env="AzurePublicCloud"):
    kv_prefix = "https://{}.vault.azure.net"

    if env == "AzureChinaCloud":
        kv_prefix = "https://{}.vault.azure.cn"

    kv_url = kv_prefix.format(keyvault_name)
    kv_client = SecretClient(kv_url, credential)

    if secret_name:
        return kv_client.get_secret(secret_name).value
    else:
        return kv_client.list_properties_of_secrets()
