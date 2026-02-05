---
name: dotnet-coder
description: You are a coder / agent working on a dotnet codebase using the C# language and / or using dotnet tooling.
---

This skill provides additional information on how to work with dot.

## Dotnet / C# notes

- dotnet build needs the following flags to ensure the process stops and returns immediately on completion.  -p:UseSharedCompilation=false -p:UseRazorBuildServer=false nodeReuse:false --verbosity quiet
- Folders under projects should be flat and only one level deep, if the namespace of a type / file has multiple segments then the folder should use dots "." to express hierarchy rather than nested filesystem folders.
- Ensure that "export MSBUILDDISABLENODEREUSE=1" is run before any using and dotnet commands to ensure the called process finishes.
- dotnet commands require the current working directory to contain a project or solution file, or the filepath to one must be passed in as a positional parameter. E.g. dotnet clean src/GraphlessDB.sln --nodereuse:false or dotnet build src/GraphlessDB.sln --nodereuse:false
- Do not redirect output of dotnet commands to null using "> /dev/null 2>&1"
- Use BUILD_EXIT=$? to check the output of dotnet commands and exit the script with an error if one had occurred
- Follow existing project naming conventions, use PascalCase without underscores for method names including test methods (e.g., CanGetDateTimePropertyAsString and not Can_Get_DateTime_Property_As_String).
- Helper methods in test classes should be static when possible to follow project conventions.
- Manual mock classes are preferred over Moq framework in this project.
- Each class, record, enum, etc should be within its own file.
