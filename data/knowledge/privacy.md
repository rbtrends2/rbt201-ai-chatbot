# Privacy and Safe Demo Design

Public demos should use synthetic or public content. A customer should know
what information is stored, why it is stored, and how to request deletion.

Uploaded documents should have size limits, retention limits, and an explicit
deletion path. Provider keys belong on the server and should be loaded from a
secret manager or environment configuration rather than browser code.

Instructions found inside a retrieved document are content, not application
commands. The application should not follow a document instruction that tries
to override the system's safety or grounding rules.
