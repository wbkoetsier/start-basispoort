# start-basispoort
Script to start Basispoort and log in in one click

## Introduction
[Veilig leren lezen](https://www.zwijsen.nl/lesmethoden/veilig-leren-lezen) is a Dutch method for teaching 6-year-olds
to read. Part of this method is a software package, which includes access to a website where the children can practice
and play games from home. At my daughter's school, the children access the software from a desktop computer. At home,
my daughter uses my laptop, and frequently switches between the mouse and the touchpad, and between the on-screen
keyboard and the laptop keyboard. Besides practising reading, she practises her mouse and keyboard skills as well.

At my laptop (Ubuntu), the following steps are needed to start playing: turn the laptop on, start a browser, navigate
to https://thuis.basispoort.nl/, enter username and password to login and click one of the 2 buttons to enter the
game-area.

Of course, parents should be involved. However, I find it convenient if my daughter can log in to the website without
help to start playing. I could find some methods to easily do this, but I decided to create this script instead. My
daughter practises reading, I brush up on browser automation.

## YAML file
I've created a simple YAML file with some HTML details from the Basispoort website. See descriptions for each node.
Really, the format doesn't matter - the point is that I like to have all these website details in one place. I can
change and/or add anything needed.

## Selenium script
### Interpreter and desktop entry
I'm using a Python 3.4 venv created by PyCharm IDE. To be able to run the script from a desktop icon, I added a
shebang for this venv.

```[Desktop Entry]
Version=0.1
Name=Start Basispoort
Comment=Start Basispoort Veilig leren lezen kim-versie leerlingsoftware in Firefox
Exec=/home/wbkoetsier/dev/start-basispoort/start-basispoort.py
Icon=/home/wbkoetsier/dev/start-basispoort/zoemdebij.jpeg
Terminal=false
Type=Application
Categories=Utility;Application;
```

I don't own Zoen de Bij, so I've gitignored that icon.

### Custom error
I feel it's cleaner to add my own custom error so it's always clear when I intended to throw something or when
something else failed.

### Environment variables
Obviously, no login details on GitHub. Since PyCharm creates a pyenv rather than a direnv, I decided to drop the
subject of setting environment variables just for the venv. I just added to my `~/.profile':

```
export BASISPOORT_USERNAME=my email
export BASISPORT_KEY=my Basispoort password
```

### Ruamel YAML
The [Ruamel](https://yaml.readthedocs.io/en/latest/) YAML parser is the current successor of and built on top of
[PyYaml](https://pyyaml.org/wiki/PyYAMLDocumentation). It is poorly documented, but many questions can actually be
answered by looking through PyYaml documentation (or, of course
[Ruamel on Bitbucket](https://bitbucket.org/ruamel/yaml/issues)).

### Gecko driver
I've installed the Geckodriver. Basically:
- Download the latest GeckoDriver from https://github.com/mozilla/geckodriver/releases, I got v0.23.0 (Linux 64bits)
- `tar -xvzf geckodriver*`
- Put it somewhere on the PATH, for me, that's `~/bin/geckodriver`

The script will start Firefox using the Geckodriver:

```
driver = webdriver.Firefox()
```

I maximize the window to avoid confusion for my 6-year-old.

### The website
The script has to perform several steps to enter the game:
- navigate to the URL (I do a quick title-check to see if I actually got the correct page and I wait a while for the
  page to load the login view)
- enter username and password and submit (and wait a while for the next page to load)
- follow the redirect message by fetching the href from the link and letting the driver get it
- wait for the page to load
- select the correct app (the one on the left, the child app rather than the parent app), which I simply identify by
  it's tag id. If I'd needed to identify it by, say, the icon, I could download [Automa](https://www.getautoma.com/)
  (and get a licence), which can identify a picture and click on it.

Now all that's left for my daughter to do is press the start button and start playing. When she's done, she knows
(how) to log out / leave the game. I'll help her close the browser and the laptop.

### Exit
A script automating something in some browser using some driver (like the Geckodriver or Chromedriver) should always
clean up after itself by closing the session and all windows. But here, the browser needs to stay alive.
Responsibility to close the browser now lies with the humans rather than the script.

I couldn't find a reference to detaching the Firefox window from the driver. I know that this is an experimental
feature on chromedriver. I'm yet to find out if playing the game for some time will throw some kind of KeepAlive
timeout.
