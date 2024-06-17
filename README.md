# Django template production ready.

This repo should be installed with cookiecutter. It's a basic django app with configurations, dockerisation, and common packages used in django applications.
You should have pipx, cookiecutter and make installed.

# Prerequesite

## Install cookicutter

### With pipx
```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions in global scope. See "Global installation" section below.
pipx install cookiecutter
```

### If pipx is not an option, you can install cookiecutter in your Python user directory.
`python -m pip install --user cookiecutter`


## Install make

Linux : `sudo apt install make`

MacOS: `brew install make`

Windows : [StackOverflow](https://stackoverflow.com/a/32127632)


# Run cookiecutter and get the template
 `pipx run cookiecutter https://github.com/lance-kawa/django_template`

 You should specify your desired configuration :
 ```bash
  [1/3] project_slug (my_repo): test_repo
  [2/3] app_name (app): blog
  [3/3] repo_url (repo_git@github.com:orga/my_repo.git): 
Initialized empty Git repository in /home/ekawa/pro/test/test_repo/.git/
```
