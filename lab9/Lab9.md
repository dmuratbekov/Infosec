# Lab 9 — Package Management

## Work Done

- Updated the package list using:
  sudo apt update

- Installed the nginx package:
  sudo apt install nginx

- Checked the installed version:
  nginx -v

- Verified that nginx service is running:
  sudo service nginx status

- Opened http://localhost in the browser and saw the default nginx welcome page.
- Checked dependencies of the package: 
  apt-cache depends nginx

- Removed nginx package to test removal command:
  sudo apt remove nginx

