Unreleased
-----------------------------

* Add a `tutor k8s registry` command for configuring 
  access to a private image registry. 
  Running the command will create imagePullSecret(s)
  and apply them to the `default` ServiceAccount in 
  the given namespace.
