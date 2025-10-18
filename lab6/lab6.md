#Lab 6 — Permissions in Linux

##What Did I Do
I learned about permissions in Linux, hoe to define who can read, write, or execute files and directories

##Types of Permissions
- Read (r) — view file contents or list directory items
- Write (w) — modify file or create/delete files in a directory
- Execute (x) — run a file or access a directory

##How to change permissions:
```
chmod 754 <file>.txt
ls -la #view permissions
```
##How to change the file owner and group:
```
chown newuser <file>.txt
chgrp newgroup <file>.txt
```

