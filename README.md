Registry Tutor plugin
===================================

This is an **experimental** plugin for
[Tutor](https://docs.tutor.overhang.io) that configures access to a 
private container image registry in a Kubernetes namespace.

Version compatibility matrix
----------------------------

You must install a supported release of this plugin to match the Open
edX and Tutor version you are deploying. If you are installing this
plugin from a branch in this Git repository, you must select the
appropriate one:

| Open edX release | Tutor version     | Plugin branch | Plugin release |
|------------------|-------------------|---------------|----------------|
| Olive            | `>=15.0, <16`     | `quince`      | `<1.5.0`       |
| Palm             | `>=16.0, <17`     | `quince`      | `>=1.1.0, <2`  |
| Quince           | `>=17.0, <18`     | `quince`      | `>=1.1.0, <2`  |
| Redwood          | `>=18.0, <19`     | `main`        | `>=2`          |
| Sumac            | `>=19.0, <20`     | `main`        | `>=2.1.0`      |
| Teak             | `>=20.0, <21`     | `main`        | `>=2.2.0`      |


Installation
------------

    pip install git+https://github.com/hastexo/tutor-contrib-registry@v2.1.0

Usage
-----

To enable this plugin, run:

    tutor plugins enable registry
    tutor config save

To test that the command is available, run:

    tutor k8s registry --help

To configure access to a private image registry in your kubernetes namespace, run:

    tutor k8s registry

This will create a secret for each of your private registries and will add them to 
the `default` ServiceAccount in your namespace.

**Important note** : This command *assumes* that your namespace already exists.
As `tutor` will create the namespace for you (if one does not already exist) 
while using `tutor k8s launch`/ `tutor k8s start` commands. But, both of these 
commands will also fail if your services cannot access the private image registry. 
So, for a fresh deployment (meanin the namespace needs to be created during 
the deployment run) you cannot run this command *before* nor *after* you run the 
`start` or `launch` commands.
As a workaround for this we suggest first bringing up a service that uses an upstream
default image and doesn't require access to a private registry. Then configure your 
registry access and run the rest of the deployment as usual. 

An example with `caddy`:

    tutor k8s start caddy
    tutor k8s registry
    tutor k8s launch / tutor k8s start
    ...

Reference documentation can be found [here](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account)

Configuration
-------------

The following values must be set in your `config.yml` file:

* `K8S_NAMESPACE`
* `REGISTRY_CREDENTIALS`

Where the `REGISTRY_CREDENTIALS` configuration value is a dictionary that requires the following structure and values:

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
