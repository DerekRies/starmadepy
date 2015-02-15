# Contributing

### Table of Contents

- - -

# Setup

## Fork on Github
It's recommended that before you do anything else you should fork the [project](https://github.com/DerekRies/starmadepy) on Github.

## Clone your fork locally
Now just clone your forked repo to your local machine, if you're unfamiliar with this process please read the github help pages on [forking](https://help.github.com/articles/fork-a-repo/). Replace `<my-github-name>` with your actual github name.

    git clone https://github.com/<my-github-name>/starmadepy.git

## Pip requirements
Developing for starmadepy comes with several depedencies, all of which can easily be installed by running the following pip command from the root starmadepy directory:

    pip install -r requirements.txt

## Running the tests
Now that you've installed the pip requirements you should be able to run the tests to make sure everything's working. Starmadepy uses the **py.test** library for tests, and the **rerun** package to run scripts on file changes.

Start by running the following command from the starmadepy root directory:

    py.test

**py.test** should find all the tests automatically and run them.  
**Note:** This runs all of the tests, in the course of development you may find you don't want to run all of them (like ones that read and write files), py.test has markers for this. You can exclude particular tests from running with the following command format, where `test-marker-name` is a valid marker.

    py.test -m "not <test-marker-name>"

**Valid markers**

 - filewrite
 - style

- - -

# Writing Code and Tests

## Issues

When you're ready to start writing code for the project please first check out the Issue tracker.

 - If you find any issues with the project please create an issue through github
 - If you're going to work on any of the issues in the tracker, make it known with a comment.
 - If you want a feature implemented or think something is missing, create a new issue through Github. I'd like to talk about it before you spend any time writing any code.

## Setting up a topic-branch

It's recommended that you create a new branch for whatever issue it is you decide to work on, so you can group a set of commits together.

    git checkout -b fix-issue-branch

When you are ready to generate a pull request, either for preliminary review, or for consideration of merging into the project you must first push your local topic branch back up to GitHub:

    git push origin fix-issue-branch

Now when you go to your fork on Github, you will see this branch listed under the "source" tab where it says "Switch Branches". go ahead and select your topic branch from this list, and then click the "Pull request" button.

## Getting that pull-request accepted

There's a few things you can do to make sure your pull-request gets accepted:

 1. Run the tests, and make sure they pass. (it's just `py.test`)
 2. Write new tests for the particular issue you're fixing/implementing
 3. Make sure the style conforms to PEP8 (there is a test for this)
 4. Shoot me a message before you start working on something, either by email, or in an issue comment, or on the starmade irc.

- - -

# Docs

The documentation for this project is written in markdown and hosted through **Readthedocs**. To run the docs locally you will need to have installed all the pip dependencies and use the following command from the starmadepy root directory:

    mkdocs serve

All of the documentation lives in the `/docs` directory, so if you need to make any changes that's where it will be.