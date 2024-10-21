# CoTrack

## AutoDeployment
GitLab CI has been configured.
To *create* a CI Pipeline, a tag is required.

Example:
```
git tag -a v1.0 -m "Version 1.0"
git push origin --tags
```

**Important:** The CI Pipeline is configured to *manual*, which means, when a tag has been created, only the Pipeline is *created* but you have to start the Pipeline yourself.

## Defined CI Variables

**REMOTE_SYSTEM** - Destination system where the Docker container should run.
**SSH_PRIVATE_KEY** - SSH key for the connection to the remote system.
**SSH_USER** - SSH user for the SSH connection.
