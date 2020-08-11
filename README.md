# Mental-Health-Support-Discussion-Forum
A discussion forum for mental health featuring a [Reddit](http://reddit.com) style tree based comment system.

### Features
* Anyone is able to register by creating an anonymous account with a chosen username
* Create discussion topics
* Other users can comment and provide support on discussions
* People can vote on comments and discussions.
* Features a [Reddit](http://reddit.com) style tree based comment system - which enhances readability of discussions.
* Sort discussions based on three criterias
    - New
    - Trending
    - Popular

### Running Instructions
```
1.	Make sure you have python 3.8.2 installed
2.	Extract the project zip file in any path.
3.	Go inside the scripts folder in the project
4.	Edit the file named ‘Activate.bat’ using notepad or any other application:
a.	In line 11 of the file, amend the path according to the path in which the project was extracted. It should look like as follows:
b.	set VIRTUAL_ENV=<<Directory path where the project was extracted>>
5.	go to the project folder and edit the file named – ‘pyvenv.cfg’
6.	amend the first line of the file to make it point to the folder in which python was installed:
a.	home = <<python installation folder>>
7.	go to the scripts folder and run cmd
8.	execute the command – ‘activate.bat’
9.	execute the command – ‘cd ..’
10.	execute the command – ‘python manage.py runserver’
11.	you should have the URL of the website printed in the command prompt in the format –http://127.0.0.1:8000/. Copy the URL and paste it in any browser to run the website.

```
### Libraries Used
- [Django - 2.2.7](https://www.djangoproject.com)
- [Django-Mptt - 0.9.1](https://django-mptt.readthedocs.io/en/latest/)
- [Bootstrap – 4.3.1](https://getbootstrap.com)
- [JQuery – 3.3.1](https://jquery.com)
- [Markdown – 3.0.1](https://pypi.org/project/django-markdown/)
- [Bleach – 3.0.2](https://pypi.org/project/django-bleach/)
