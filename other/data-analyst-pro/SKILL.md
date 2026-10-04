---
name: data-analyst
description: Complete the data analysis tasks delegated by the user.If the code needs to operate on files, please ensure that the file is listed in the `upload_files` parameter, and **pay special attention** that, in the code, you should directly use the filename (e.g., `open('data.csv', 'r')`) to access the uploaded files, because they will be placed under the working directory `./`.
---

# Data Analyst

## Overview

This skill provides specialized capabilities for data analyst.

## Instructions

Complete the data analysis tasks delegated by the user.If the code needs to operate on files, please ensure that the file is listed in the `upload_files` parameter, and **pay special attention** that, in the code, you should directly use the filename (e.g., `open('data.csv', 'r')`) to access the uploaded files, because they will be placed under the working directory `./`.


## Usage Notes

- This skill is based on the data_analyst agent configuration
- Template variables (if any) like $DATE$, $SESSION_GROUP_ID$ may require runtime substitution
- Follow the instructions and guidelines provided in the content above
