# Doc2Pdf-bot

Convert DOC or DOCX using a Telegram Bot

<p align="center">
  <img src="https://user-images.githubusercontent.com/9201111/44356676-4db97800-a4b0-11e8-92fa-0c2a6807fbb8.png">
</p>


## Getting Started

If you want to run this bot locally on your machine you only have to install the requirements, edit [Secrets.py](Secrets.py) with your [token](https://core.telegram.org/bots/faq#how-do-i-create-a-bot) and run: 

`python bot.py`

Then, go to Telegram and start it with the `/start` command.


### Requirements

This code needs:

* [LibreOffice](https://libreoffice.org/)
* Linux (Althought can be ported easily to Windows or MacOs)
* Python

You can install the necessary python dependencies by moving to the project directory and running:
```
pip install -r requirements.txt
```

## Deployment

I deployed this script in Heroku. For the deployment using Heroku is necessary to create some files: 

1. Create a file named `Procfile` with the following content:
```
worker: python Bot.py	
```
2. An `Aptfile` with the following content:
```
libreoffice
libxfixes3
libxinerama-dev
libxinerama1
libxdamage1
libglu1-mesa:i386
``` 
3. You will need Java for LibreOffice, so create a dummy `pom.xml` like the following:
```
<?xml version="1.0" encoding="UTF-8"?>
<project>
   <modelVersion>4.0.0</modelVersion>
   <groupId>com.dummy</groupId>
   <artifactId>dummy</artifactId>
   <version>1.0-SNAPSHOT</version>
   <packaging>pom</packaging>
</project>
```
4. Create an app on Heroku, using CLI or Dashboard.
5. Add the [buildpacks:](https://devcenter.heroku.com/articles/buildpacks)
```
heroku/java
https://github.com/heroku/heroku-buildpack-apt.git
heroku/python
 ```
6. LibreOffice will give you an issue with [`libGL.so.1`](https://github.com/rishihahs/heroku-buildpack-libreoffice/issues/13), so you must run the following command:
```
ln -s ~/.apt/usr/lib/x86_64-linux-gnu/mesa/libGL.so.1 ~/.apt/usr/lib/x86_64-linux-gnu/
```
You can make it run by forking and editing https://github.com/heroku/heroku-buildpack-apt.git or adding the following line (at main) to the Bot.py:
```
subprocess.call("""ln -s  ~/.apt/usr/lib/x86_64-linux-gnu/mesa/libGL.so.1 ~/.apt/usr/lib/x86_64-linux-gnu/""", shell=True)
```

7. Now you can finally deploy your app and scale your dyno!
```
heroku ps:scale worker=1
```

## Contributing

Feel free to contribute to this repository, but first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

## Authors

* **Alejandro Fuster** - [AlejandroFuster](https://github.com/alejandrofuster)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
