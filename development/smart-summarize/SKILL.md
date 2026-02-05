---
name: smart-summarize
description: Create useful, informative summaries of technologies or concepts that are readable in depth and have a digestable summary at the top.
license: Apache
---

This skill describes how to research and report on each subject area to fill out this study guide. The aim of this repository is to create a study guide that can be read like a chapter book, and also reviewed later for refreshers. 

## Format 

The entire write-up for a section should be done within a ReadMe.md file. So if the folder is called 's3', the write-up should exist within the s3/ReadMe.md file. The write-up should start with a summary with small sections that can be reviewed later. This should include a few small paragraphs and bullets of important points to remember. Then, a longer, more detailed write-up should follow. It should vary in length between several pages and a short chapter in a book. 

Avoid emoji's and symbols of any kind. Bullets and numbered lists are acceptable.

## Topics
The write-up should be written for a mid-career machine learning engineer who has on the job experience but may not be familiar with your particular topic. You do not need to explain simple concepts like classes in object oriented programming or basic programming syntax. When in doubt, briefly explain a concept in order to refresh the reader's memory but do not belabor to explain concepts that are probably already understood by a mid-career MLE. 

With that framing in mind, also consider the other topics in the same directory when writing the chapter. For example, in a data format chapter, check the other data format chapters and provide some comparisons, especially trade-offs between two different formats or approaches. Note, this may not be necessary in every case where comparisons aren't helpful. 

The focus should be on practical knowledge for usage and decision-making. Avoid historical information unless is is helpful in understanding the concept or making decisions. 

## Engineering Blogs
You must search engineering.fyi for the topic and use relevant articles. If an article is used from engineering.fyi you must add it to the resources tab for the topic. Note, you can search via url by using 
`https://engineering.fyi/search?q=<topic>`
Spaces are filled with the & symbol. 

## Fact-Finding
Using your ingrained knowledge is fine for most use cases. However, before you start, check the chapter's directory. There may or may not be a 'Resources.md' or 'resources.md' file there. If there is, read this file line by line. For each line, check if the line is a full url or a phrase. If a full URL, use the WebFetch tool and read the content. If a phrase, use the WebSearch  tool and read the first non-sponsered link, then use WebFetch to read its content. If you are unsure of necessary details, use the WebSearch tool on your own, but ensure you append your search phrase to the Resources.md in the same directory (create one if necessary). 

## Before Starting
You MUST NOT start a chapter if there is already text inside the ReadMe.md. 

## When Children Are Present
We also want to create chapters of topics where children are present. For example, 'object-storage' should have a chapter that talks about the use of Object storage in general and compares and contrasts the three child topics (azure-blob, gcs, and s3)