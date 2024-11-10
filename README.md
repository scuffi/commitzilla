<p align="center">
  <img src="./icon.png" alt="Icon" />
</p>

Welcome to **commitzilla**! This is a simple git hook that will hijack your commit messages, and translate them into detailed, comprehensive messages, fit for anyone and everyone!

<p align="center">
  <img src="./example.gif" alt="Example GIF" />
</p>

## Installation

Installation is soooooo easy, just pip install the package:

```
pip install commitzilla
```

then navigate to the directory of your local git repo where you want to install the hook, and run:

```
commitzilla install
```

and bob's your uncle.

## Configuration

You can change the character style of the commit message (or add your own custom one) by running:

```
commitzilla character
```

You can edit the OpenAI model (other providers coming soon) and the OpenAPI key with the configure command, for more info, run:

```
commitzilla configure
```

You can also enable a prefix, so your messages will look like this: `[Character] Commit message` so you can keep track of which commits are good and which are bad:

```
commitzilla prefix
```

## Uninstallation

Not sure why you're reading this... but anyways, removing commitzilla is even easier than installing it,
just navigate to the directory you want to remove the hook, and run:

```
commitzilla uninstall
```
