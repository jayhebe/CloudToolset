from azure.identity import ClientSecretCredential, KnownAuthorities


def get_credential(client_id, client_secret, tenant_id, env="AzurePublicCloud"):
    authority = KnownAuthorities.AZURE_PUBLIC_CLOUD

    if env == "AzureChinaCloud":
        authority = KnownAuthorities.AZURE_CHINA

    credential = ClientSecretCredential(
        client_id=client_id,
        client_secret=client_secret,
        tenant_id=tenant_id,
        authority=authority
    )

    return credential
