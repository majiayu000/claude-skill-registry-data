---
name: spark-update-demo-code-syntax
description: Add or update the code syntax in demo app from all components
---

# Add Repository Skill

## Overview & Prerequisites

This skill add or update the CodeSyntax classes in *Sources/Scene/Components/XXX/Tools/CodeSyntax* for all components

❗️ If the current folder is not a the demo (spark-ios-demo), ignore this skill ❗️

## Steps

Do this process for all components in *Sources/Scene/Components/* and for SwiftUI and UIKit (it they exist) :

[ ] Get all code syntaxes from the components inits **documentation** (found in dependencies components Views : )
[ ] Put theses codes syntaxes in the *XXXCodeSyntaxes* and *XXXUICodeSyntaxes*
[ ] Create **private static var** for each code syntaxes founded
