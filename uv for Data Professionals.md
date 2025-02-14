# What data professionals need to know about uv

uv is all the rage. It helps you reduce the pain of Python virtual environment management, slow package installs, and unreproducible environments. 

Although uv solves a slew of headaches for Python users it's still in its early days. Although there is a lot of buzz around uv, when I polled a class of data professionals, only a few of them had tried it. 

![Zoolander Mugato meme saying uv so hot right now](img2.jpg)

As a data professional you can use uv to save time and money. Let's see how.

## The current situation

Here's the landscape of existing popular tools.

First, you've got your default Python version managers: venv, virtualenv.

Then, there's your snake-named virtual environment managers: conda, miniconda, mamba.

Next, are your Python version managers: pyenv, tox.

Plus, there are your Python package managers: pip, pipx, poetry.

Don't forget your package dependency version files: requirements.txt and pyproject.toml. And you've got tools such as pipx to help you use them.

And that's a simplified list of the options! It ain't pretty.

The worst part is that when the wires get crossed, it's a time suck. I was reminded of this not long ago. I've been a conda user for years (mamba flavor, lately). Recently, my `base`, default conda environment had some deep package dependency issues that caused tough-to-diagnose problems. I wanted to remove my `base` environment and start fresh, but you can't easily do that, at least not without risking breaking your entire setup. But reinstalling conda yet again and risking a case of "PATH issue-itis" isn't anyone's idea of a good time. 

That's what caused me to make the jump to uv.

uv brings simplicity and speed to the chaos that is Python virtual environment and package management.

## Goal: install uv so you can take advantage of it

First, ensure you aren't already in a Python virtual environment. If you see parentheses around a word such as `(base)` in your terminal prompt, you probably are in a virtual environment. If it's a conda environment, exit it with `conda deactivate`. If it's a venv environment, exit it with `deactivate`. Run those commands until you don't see any parentheses in your prompt.

Check that you don't already have uv installed with:

```bash
uv --version
```

I'm using uv 0.5.25 (Homebrew 2025-01-28) for this example.

Install uv on a Mac or Linux machine with homebrew:

```bash
brew install uv
```

Alternatively, you can install uv with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On a Windows machine you can install uv with:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For more assistance, see the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/).

Now that we have uv installed, let's use it!

## Goal: create a Python virtual environment that will stick around for future use

The ux of uv is lovely. It borrows from the syntax of popular tools.

If you've used `venv` before, you'll feel right at home, just preface your usual virtual environment creation command with `uv` and specify the desired Python version - no need to use a tool such as `pyenv` to install and manage Python versions.

Here's the command to create a virtual environment with Python 3.12:

```bash
uv venv --python 3.12
```

uv will find a Python 3.12 version locally if you have one installed. If you don't have a Python 3.12 version installed, uv will fetch and install the latest stable 3.12 version.

Then, follow the handy command line output instructions to activate your virtual environment:

```bash
source .venv/bin/activate
```

Viola! Your terminal prompt should display the name of a virtual environment in parentheses.

Let's install some Python packages.

## Goal: install packages really fast

uv is orders of magnitude faster than pip when it comes to installing packages into your virtual environment. And the syntax is familiar if you're used to using pip. For example, to install the `prefect` package, just throw `uv` in front of your usual pip command like this:

```bash
uv pip install prefect
```

You upgrade a package and its dependencies, you can use the same `-U` flag that you'd use with pip:

```bash
uv pip install -U prefect
```

See the versions of all your installed packages with:

```bash
uv pip list
```

Now you've got a virtual environment and with the packages you need. Next, say you build a useful project and everything works. Fantastic! Let's make this reproducible.

## Goal: make a reproducible environment

As with pip, you can use the `-r` flag with uv to install all the packages listed in a `requirements.txt` file with a single command.

Say this is your file:

```requirements.txt
polars
plotly
prefect 
```

Then just run the following command:

```bash
uv pip install -r requirements.txt
```

In the past, you might have specified top level package versions in your `requirements.txt` file.

```requirements.txt
prefect==3.11.0
polars==0.7.3
plotly==5.24.1
```

That's a step further toward reproducibility, but sometimes a dependency of one of the packages you've specified will change and break your project. We don't want that, so let's create a lock file.

uv can read a list of packages from one file and output a lock file that specifies the exact versions of all top-level packages and their dependencies - and their dependencies' dependencies, all the way down.

Let's specify the top level packages we need in  a `requirements.in` file. Then we'll generate a `requirements.txt` file with the versions of all specified packages and their dependencies with this command:

```bash
uv pip compile requirements.in -o requirements.txt
```

Now our `requirements.txt` file contains the exact versions of all the top level packages and their dependencies, in tree format. When we run our `requirements.txt` install command, we'll get the exact versions of all the packages we want.

So what, you say? pipenv and poetry could do that, too? Fair enough, but let's talk about the need for speed.

![top gun need for speed fast install speed](needspeed.jpg)

## Goal: faster package installs in Docker

Faster package installs shorten feedback loops, increase developer productivity, and speed up CI/CD pipelines, saving time, energy, and money.

uv is written in the famously fast [Rust language](https://www.rust-lang.org/) and takes advantage of clever optimizations to reduce package install times.

I saw over a 5x speedup when using uv as opposed to pip to install 17 Python packages in a Docker image build: 7 seconds vs. 37 seconds. 🤯

Using uv to build a Docker image minor modifications. Just add:

```dockerfile
COPY --from=ghcr .io/astral-sh/uv:latest /uv /uvx /bin/
```

and change:

```dockerfile
RUN pip install my_package
```

to:

```dockerfile
RUN uv pip install --system my_package
```

Or instead of specifying `--system` every time, set the environment variable in your Dockerfile with:

```dockerfile
ENV UV_SYSTEM_PYTHON=1
```

Now let's see some almost magical uv tricks.

## Goal: run a Python script in a single line in a disposable virtual environment 

Use 

```bash
uv run my_script.py
```

Need a package such as polars?

```bash
uv run --with polars my_script.py
```

You can even fire up a Jupyter lab server in a disposable virtual environment with:

```bash
uv run --with jupyter jupyter lab
```

I wish this was a thing when I was learning Python.

# Goal: run a file hosted on the web or in the clipboard

If your file paths are set up correctly, uv will auto-install the dependencies in a script and run them in a temporary virtual environment.

```bash
uv run https://example.com/my_script.py
```

You can do the same thing with code in your clipboard on a Mac with this command:

```bash
pbpaste | uv run - 
```

## Goal: project management

uv also solves pain points for project management. It helps you quickly start a project and provides handy commands for development. Create a project:

```bash
uv init project1
```

This scaffolds a project with a `pyproject.toml` file, a `hello.py` file, and a `README.md` file.
It also adds`.git` and `.gitignore` files for version control. Convenient!

You can declare your Python version as well as your dependencies and project metadata in `pyproject.toml`. This further helps with reproducibility.

Run the script in your project with:

```bash
uv run hello.py
```

Then, uv will automatically create a virtual environment with a `.venv` file and create a lock file with the pinned versions of your dependencies and their dependencies.  

Add and remove packages for your project like this:

```bash
uv add polars
uv remove polars
```

If you want to use the project you created for publishing packages, uv has your back.

## Goal: publish your package

To build source distribution and wheel artifacts, make sure you have the necessary metadata in your `pyproject.toml` file and then run:

```bash
uv build
```

Then, you'll see `project1.egg-info` and `dist` directories in your project.

Once you've set up your PyPI credentials, you can even publish your package to a PyPI-compatible index with:

```bash
uv publish
```

uv provides additional handy commands for working with your package that you can see in the [docs](https://docs.astral.sh/uv/guides/package).

## Conclusion
Although we've covered a lot of uv's functionality, we didn't dig into [tools](https://docs.astral.sh/uv/guides/tools/) and the related `uvx` command, but we might in a future post, so keep an eye out.

At Prefect we're increasingly using uv and seeing the benefits. If you haven't yet tried uv, give it a whirl and I bet you'll see faster development and save time running your CI/CD pipelines.

### Additional resources

Want to keep exploring? Check out these resources:

- [uv docs](https://docs.astral.sh/uv)
- [Good YouTube video](https://www.youtube.com/watch?v=goIwKjsEPOI) on uv with emphasis on its project management features and the source of the stat above on uv's popularity.
- [Nice uv guide](https://www.saaspegasus.com/guides/uv-deep-dive/).
