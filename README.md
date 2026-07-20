# Registry Tutor plugin

This is an **experimental** plugin for [Tutor](https://docs.tutor.overhang.io) that configures access to a private container image registry in a Kubernetes namespace.

This repository was previously hosted under the `hastexo` GitHub organization.
It was moved to `cleura` in December 2025 as part of a routine repository consolidation.

## Version compatibility matrix

You must install a supported release of this plugin to match the Open edX and Tutor version you are deploying.
If you are installing this plugin from a branch in this Git repository, you must select the appropriate one:

| Open edX release | Tutor version     | Plugin branch | Plugin release |
|------------------|-------------------|---------------|----------------|
| Olive            | `>=15.0, <16`     | `quince`      | `<1.5.0`       |
| Palm             | `>=16.0, <17`     | `quince`      | `>=1.1.0, <2`  |
| Quince           | `>=17.0, <18`     | `quince`      | `>=1.1.0, <2`  |
| Redwood          | `>=18.0, <19`     | `main`        | `>=2`          |
| Sumac            | `>=19.0, <20`     | `main`        | `>=2.2.0`      |
| Teak             | `>=20.0, <21`     | `main`        | `>=2.2.0`      |
| Ulmo             | `>=21.0, <22`     | `main`        | `>=2.3.0`      |
| Verawood         | `>=22.0, <23`     | `main`        | `>=2.4.0`      |

## Installation

Run the command below to install the plugin:

```bash
pip install git+https://github.com/cleura/tutor-contrib-registry@v2.3.0
```

## Usage

To enable this plugin, run the commands below:

```bash
tutor plugins enable registry
tutor config save
```

To test that the command is available, run the command below:

```bash
tutor k8s registry --help
```

To configure access to a private image registry in your Kubernetes namespace, run the command below:

```bash
tutor k8s registry
```

This will create a secret for each of your private registries.
The command will add these secrets to the `default` ServiceAccount in your namespace.

**Important note**: This command *assumes* that your namespace already exists.
The `tutor` tool will create the namespace for you while using `tutor k8s launch` or `tutor k8s start` commands.
Both of these commands will fail if your services cannot access the private image registry.
So you cannot run the registry command *before* nor *after* you run the `start` or `launch` commands on a fresh deployment.

As a workaround for this issue we suggest first bringing up a service that uses an upstream default image and doesn't require access to a private registry.
Then configure your registry access and run the rest of the deployment as usual.

An example with `caddy`:

```bash
tutor k8s start caddy
tutor k8s registry
tutor k8s launch / tutor k8s start
...
```

Reference documentation can be found [here](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account)

## Configuration

The following values must be set in your `config.yml` file:

* `K8S_NAMESPACE`
* `REGISTRY_CREDENTIALS`

The `REGISTRY_CREDENTIALS` configuration value is a dictionary that requires the
following structure and values:

```yaml
REGISTRY_CREDENTIALS:
    private-registry.example.com:
        key_name: <key_name>
        password: <password>
        username: <username>
    private-registry.example.org:
        email: <email>  # optional, depending on your registry
        key_name: <key_name>
        password: <password>
        username: <username>
```
