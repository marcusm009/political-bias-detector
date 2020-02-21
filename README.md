# Political Bias Detector
A plugin for chrome that can classify tweets based on how biased they are politically

## How it works
The server consists of a dockerized python app that uses a version of GPT-2 finetuned on tweets. This app can be hosted on any popular cloud service that supports docker containers. The chrome extension can be easily installed and makes api requests to the back-end using the http protocol. The back-end returns a prediction to the extension, which then displays it.

## Installation
Refer to the README files located in the server and extension folders for individual installation instructions.
