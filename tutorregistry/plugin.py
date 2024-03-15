from __future__ import annotations

import click
import json

from tutor import config as tutor_config
from tutor import exceptions, hooks, utils
from tutor.commands.k8s import k8s

from .__about__ import __version__


hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        ("REGISTRY_VERSION", __version__),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        ("REGISTRY_CREDENTIALS", {}),
    ]
)


@k8s.command(help="Configure access to a private registry with an "
                  "imagePullSecret")
@click.pass_obj
def registry(context) -> None:
    """
    Create imagePullSecret(s) for private registries and
    add them to the default ServiceAccount in the given namespace.
    If a secret with the same name already exists delete and
    recreate it, so credentials are always up to date for the secrets.
    run CMD --> tutor k8s registry
    """
    config = tutor_config.load(context.root)
    namespace = config["K8S_NAMESPACE"]
    creds = config["REGISTRY_CREDENTIALS"]

    all_keys = {"imagePullSecrets": []}

    for registry, cred in creds.items():
        try:
            key_name = cred["key_name"]
            username = cred["username"]
            password = cred["password"]
            # email is optional; depending on the registry
            email = cred.get("email", "")
        except KeyError:
            raise exceptions.TutorError(
                "Missing credentials for a private registry. Please "
                "provide a 'key_name', 'username' and 'password' for each "
                "of your registries via the 'REGISTRY_CREDENTIALS' definition "
                "in your 'config.yml' file."
            )

        utils.kubectl(
            "delete", "secret", key_name,
            f"--namespace={namespace}",
            "--wait=true",
            "--ignore-not-found=true")

        utils.kubectl(
            "create", "secret", "docker-registry", f"{key_name}",
            f"--namespace={namespace}",
            f"--docker-server={registry}",
            f"--docker-username={username}",
            f"--docker-password={password}",
            f"--docker-email={email}")

        all_keys["imagePullSecrets"].append({"name": key_name})

    # Add the secret(s) to the default ServiceAccount. If the secrets are
    # already present, it will be patched with no change, no need to catch
    # an error here.
    utils.kubectl(
        "patch", "serviceaccount", "default",
        "-p", json.dumps(all_keys),
        f"--namespace={namespace}")
