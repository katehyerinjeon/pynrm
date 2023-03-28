# Contribution Guidelines
Thanks for your interest in contributing! We want to make contributing to this project as easy and transparent as possible whether it is reporting a bug, discussing the current state of the code, submitting a fix, proposing new features, or more.

## Getting Started
We use [GitHub issues](https://github.com/katehyerinjeon/pynrm/issues) to track public bugs. Report a bug by opening a new issue and make sure to include the followings:

- A quick summary of the issue
- Clear and specific steps to reproduce with sample code if possible
- What you expected would happen
- What actually happens
- Side notes possibly including why you think this might be happening or stuff you tried that didn't work

## Making Changes
Pull requests are the best way to propose changes to the codebase as we use [GitHub workflow](https://github.com/katehyerinjeon/pynrm/actions).

1. Fork the repository and create your branch from `main` (or a topic branch from where you want to base your work)
2. Make commits of logical units (rebase your feature branch before submitting if needed) and write commit messages in [proper format](https://github.blog/2022-06-30-write-better-commits-build-better-projects/)
3. Add tests for any new features or code that should be tested
4. Ensure the test suite passes by running `make tests`
5. Make sure your code lints by running `make lint`
6. Push your changes to the topic branch in your fork of the repository and submit a pull request
