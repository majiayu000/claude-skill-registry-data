---
name: babashka.fs
description: A guide to using babashka.fs.
---

# Babashka.fs File System Utilities Skill

## Overview

The `babashka.fs` library is a comprehensive file system utility library for Clojure, designed for cross-platform file operations. It provides a clean, functional API for working with files, directories, and paths, built on top of Java's NIO.2 API while offering a more idiomatic Clojure interface.

**When to use this skill:**
- When working with files and directories in Clojure/Babashka scripts
- When you need cross-platform file system operations
- When writing build tasks, file processing scripts, or automation tools
- When you need to search, filter, or manipulate file systems programmatically

## Setup and Requirements

### Adding to your project

```clojure
;; In deps.edn
{:deps {babashka/fs {:mvn/version "0.5.27"}}}

;; In your namespace
(ns my-script
  (:require [babashka.fs :as fs]))
```

### Built-in to Babashka

The library is built into Babashka, so no additional dependencies are needed for bb scripts:

```clojure
#!/usr/bin/env bb
(require '[babashka.fs :as fs])

(fs/directory? ".")  ; => true
```

## Core Concepts

### Path Objects

Most functions accept and return `java.nio.file.Path` objects, but also work with strings and other path-like objects. The library automatically coerces between types.

```clojure
;; All of these work
(fs/exists? ".")
(fs/exists? (fs/path "."))
(fs/exists? (java.io.File. "."))
```

### Cross-Platform Support

The library handles platform differences automatically, but provides utilities when you need platform-specific behavior:

```clojure
;; Works on all platforms
(fs/path "dir" "subdir" "file.txt")

;; Convert to Unix-style paths (useful for Windows)
(fs/unixify "C:\\Users\\name\\file.txt")  ; => "C:/Users/name/file.txt"
```

## Path Operations

### Creating and Manipulating Paths

```clojure
;; Create paths
(fs/path "dir" "subdir" "file.txt")              ; Join path components
(fs/file "dir" "subdir" "file.txt")              ; Alias for fs/path

;; Path properties
(fs/absolute? "/tmp/file.txt")                   ; true
(fs/relative? "dir/file.txt")                    ; true
(fs/hidden? ".hidden-file")                      ; Check if hidden

;; Path transformations
(fs/absolutize "relative/path")                  ; Convert to absolute
(fs/canonicalize "/tmp/../file.txt")             ; Resolve to canonical form
(fs/normalize "/tmp/./dir/../file.txt")          ; Normalize path

;; Path components
(fs/file-name "/path/to/file.txt")               ; "file.txt"
(fs/parent "/path/to/file.txt")                  ; "/path/to"
(fs/extension "file.txt")                        ; "txt"
(fs/split-ext "file.txt")                        ; ["file" "txt"]
(fs/strip-ext "file.txt")                        ; "file"

;; Path relationships
(fs/starts-with? "/foo/bar" "/foo")              ; true
(fs/ends-with? "/foo/bar.txt" "bar.txt")         ; true
(fs/relativize "/foo/bar" "/foo/bar/baz")        ; "baz"

;; Get all components
(fs/components "/path/to/file.txt")              ; Seq of path components
```

### Working with Extensions

```clojure
;; Get extension
(fs/extension "document.pdf")                     ; "pdf"
(fs/extension "archive.tar.gz")                   ; "gz"

;; Split filename and extension
(fs/split-ext "document.pdf")                     ; ["document" "pdf"]

;; Remove extension
(fs/strip-ext "document.pdf")                     ; "document"
(fs/strip-ext "archive.tar.gz")                   ; "archive.tar"
```

## File and Directory Checks

```clojure
;; Existence and type checks
(fs/exists? "file.txt")                           ; Does it exist?
(fs/directory? "path/to/dir")                     ; Is it a directory?
(fs/regular-file? "file.txt")                     ; Is it a regular file?
(fs/sym-link? "link")                             ; Is it a symbolic link?
(fs/hidden? ".hidden")                            ; Is it hidden?

;; Permission checks
(fs/readable? "file.txt")                         ; Can we read it?
(fs/writable? "file.txt")                         ; Can we write to it?
(fs/executable? "script.sh")                      ; Can we execute it?

;; Comparison
(fs/same-file? "file1.txt" "file2.txt")          ; Are they the same file?
```

## Creating Files and Directories

```clojure
;; Create directories
(fs/create-dir "new-dir")                         ; Create single directory
(fs/create-dirs "path/to/new/dir")               ; Create with parents

;; Create files
(fs/create-file "new-file.txt")                  ; Create empty file

;; Create temporary files/directories
(fs/create-temp-file)                            ; Creates temp file
(fs/create-temp-file {:prefix "data-"            ; Custom prefix/suffix
                       :suffix ".json"})
(fs/create-temp-dir)                             ; Creates temp directory
(fs/create-temp-dir {:prefix "workdir-"})

;; Create links
(fs/create-link "link-name" "target")            ; Hard link
(fs/create-sym-link "symlink" "target")          ; Symbolic link

;; Temporary directory context
(fs/with-temp-dir [tmp-dir {:prefix "work-"}]
  (println "Working in" (str tmp-dir))
  ;; Do work with tmp-dir
  ;; Directory automatically deleted after
  )
```

## Reading and Writing Files

### Reading Files

```clojure
;; Read entire file
(slurp (fs/file "data.txt"))                     ; As string

;; Read lines
(with-open [rdr (io/reader (fs/file "data.txt"))]
  (doall (line-seq rdr)))

;; Or use fs helpers
(fs/read-all-lines "data.txt")                   ; Returns seq of lines
(fs/read-all-bytes "binary-file")                ; Returns byte array
```

### Writing Files

```clojure
;; Write text
(spit (fs/file "output.txt") "Hello, world!")

;; Write lines
(fs/write-lines "output.txt"
                ["Line 1" "Line 2" "Line 3"])
(fs/write-lines "output.txt"
                ["More lines"]
                {:append true})                   ; Append mode

;; Write bytes
(fs/write-bytes "output.bin" byte-array)
(fs/write-bytes "output.bin" byte-array
                {:append true})
```

## Copying, Moving, and Deleting

```clojure
;; Copy files
(fs/copy "source.txt" "dest.txt")                ; Copy file
(fs/copy "source.txt" "dest.txt"
         {:replace-existing true})               ; Overwrite if exists

;; Copy entire directory trees
(fs/copy-tree "source-dir" "dest-dir")           ; Recursive copy
(fs/copy-tree "source-dir" "dest-dir"
              {:replace-existing true})

;; Move/rename
(fs/move "old-name.txt" "new-name.txt")          ; Move or rename
(fs/move "file.txt" "other-dir/")                ; Move to directory

;; Delete
(fs/delete "file.txt")                           ; Delete single file
(fs/delete-if-exists "maybe-file.txt")           ; No error if missing
(fs/delete-tree "directory")                     ; Delete directory recursively

;; Delete on exit
(fs/delete-on-exit "temp-file.txt")              ; Delete when JVM exits
```

## Listing and Traversing Directories

### Simple Listing

```clojure
;; List directory contents
(fs/list-dir ".")                                ; Seq of paths in directory
(fs/list-dir "." "*.txt")                        ; With glob pattern

;; List multiple directories
(fs/list-dirs ["dir1" "dir2"] "*.clj")           ; Combine results

;; Get directory stream (more efficient for large dirs)
(with-open [ds (fs/directory-stream "." "*.txt")]
  (doseq [path ds]
    (println path)))
```

### Walking Directory Trees

```clojure
;; Walk directory tree
(fs/walk-file-tree "."
  {:visit-file (fn [path attrs]
                 (println "File:" path)
                 :continue)
   :pre-visit-dir (fn [path attrs]
                    (println "Entering:" path)
                    :continue)
   :post-visit-dir (fn [path ex]
                     (println "Leaving:" path)
                     :continue)})

;; Common options
;; :max-depth - limit depth
;; :follow-links - follow symbolic links
;; :visit-file - called for each file
;; :pre-visit-dir - called before visiting directory
;; :post-visit-dir - called after visiting directory
;; :visit-file-failed - called when file access fails
```

## Searching and Filtering: Glob and Match

### Glob Patterns

The `glob` function is one of the most powerful features for finding files:

```clojure
;; Find all Clojure files recursively
(fs/glob "." "**/*.clj")                         ; ** means recursive

;; Find files in current directory only
(fs/glob "." "*.txt")                            ; * means any characters

;; Multiple extensions
(fs/glob "." "**{.clj,.cljc,.cljs}")            ; Match multiple patterns

;; Complex patterns
(fs/glob "src" "**/test_*.clj")                 ; Test files anywhere
(fs/glob "." "data/*.{json,edn}")               ; JSON or EDN in data dir

;; Exclude patterns (use filter)
(->> (fs/glob "." "**/*.clj")
     (remove #(re-find #"/test/" (str %))))     ; Exclude test directories

;; Common glob patterns:
;; *     - matches any characters (not including /)
;; **    - matches any characters including /
;; ?     - matches single character
;; [abc] - matches any character in brackets
;; {a,b} - matches either a or b
```

### Match with Regular Expressions

For more complex matching, use `match`:

```clojure
;; Use regex for pattern matching
(fs/match "." "regex:.*\\.clj$" {:recursive true})

;; Or glob (explicit)
(fs/match "." "glob:**/*.clj" {:recursive true})

;; Options
(fs/match "src" "regex:test.*\\.clj"
          {:recursive true
           :hidden false                         ; Skip hidden files
           :follow-links false                   ; Don't follow symlinks
           :max-depth 5})                        ; Limit depth
```

### Practical File Filtering Examples

```clojure
;; Find large files
(->> (fs/glob "." "**/*")
     (filter fs/regular-file?)
     (filter #(> (fs/size %) (* 10 1024 1024)))  ; > 10MB
     (map str))

;; Find recently modified files
(->> (fs/glob "." "**/*.clj")
     (filter #(> (fs/file-time->millis (fs/last-modified-time %))
                 (- (System/currentTimeMillis)
                    (* 24 60 60 1000))))          ; Last 24 hours
     (map str))

;; Find files by owner (Unix)
(->> (fs/glob "/var/log" "*")
     (filter #(= "root" (str (fs/owner %))))
     (map str))

;; Find executable scripts
(->> (fs/glob "." "**/*.sh")
     (filter fs/executable?)
     (map str))
```

## File Metadata and Attributes

```clojure
;; File size
(fs/size "file.txt")                             ; Size in bytes

;; Timestamps
(fs/creation-time "file.txt")                    ; FileTime object
(fs/last-modified-time "file.txt")               ; FileTime object
(fs/set-last-modified-time "file.txt"
                           (fs/file-time 1234567890000))

;; Convert FileTime to millis
(fs/file-time->millis (fs/last-modified-time "file.txt"))
(fs/file-time->instant (fs/last-modified-time "file.txt"))

;; Create FileTime from millis
(fs/file-time 1234567890000)

;; Owner (Unix/Linux)
(fs/owner "file.txt")                            ; Returns owner object
(str (fs/owner "file.txt"))                      ; Owner name as string

;; POSIX permissions (Unix/Linux)
(fs/posix->str (fs/posix-file-permissions "file.txt"))  ; "rwxr-xr-x"
(fs/set-posix-file-permissions "file.txt"
                               (fs/str->posix "rwxr-xr-x"))

;; Check for modified files since anchor
(fs/modified-since "target" "src")               ; Files in src newer than target
```

## Archive Operations (Zip)

```clojure
;; Create zip archive
(fs/zip "archive.zip" "file1.txt")               ; Single file
(fs/zip "archive.zip" ["file1.txt"
                        "file2.txt"
                        "dir"])                   ; Multiple files/dirs

;; Zip with options
(fs/zip "archive.zip" "directory"
        {:root "directory"})                      ; Strip parent path

;; Extract zip archive
(fs/unzip "archive.zip" "output-dir")            ; Extract all

;; Extract with filter
(fs/unzip "archive.zip" "output-dir"
          {:extract-fn (fn [{:keys [name]}]
                         (re-find #"\\.txt$" name))})  ; Only .txt files

;; Manually work with zip entries
(fs/zip-path "archive.zip" "path/in/zip")        ; Access file in zip as path
```

## System Paths and Utilities

```clojure
;; User directories
(fs/home)                                        ; User home directory
(fs/temp-dir)                                    ; System temp directory
(fs/cwd)                                         ; Current working directory

;; XDG Base Directory Specification (Linux)
(fs/xdg-config-home)                             ; ~/.config
(fs/xdg-config-home "myapp")                     ; ~/.config/myapp
(fs/xdg-data-home)                               ; ~/.local/share
(fs/xdg-cache-home)                              ; ~/.cache
(fs/xdg-state-home)                              ; ~/.local/state

;; Executable paths
(fs/exec-paths)                                  ; All dirs in PATH
(fs/which "java")                                ; Find executable in PATH
(fs/which "git")                                 ; Returns path or nil

;; Find executable manually
(->> (fs/exec-paths)
     (mapcat #(fs/list-dir % "java*"))
     (filter fs/executable?)
     first)
```

## Advanced Patterns and Best Practices

### Safe File Operations with Error Handling

```clojure
;; Check before operating
(when (fs/exists? "config.edn")
  (fs/copy "config.edn" "config.backup.edn"))

;; Use delete-if-exists for optional deletion
(fs/delete-if-exists "temp-file.txt")

;; Handle walk-file-tree errors
(fs/walk-file-tree "."
  {:visit-file-failed (fn [path ex]
                        (println "Failed to access:" path)
                        :skip-subtree)})
```

### Working with Temporary Files

```clojure
;; Pattern 1: with-temp-dir (automatic cleanup)
(fs/with-temp-dir [tmp-dir {:prefix "work-"}]
  (let [work-file (fs/path tmp-dir "data.txt")]
    (spit work-file "temporary data")
    (process-file work-file)))
;; tmp-dir automatically deleted here

;; Pattern 2: Manual temp file management
(let [tmp-file (fs/create-temp-file {:prefix "data-"
                                       :suffix ".json"})]
  (try
    (spit tmp-file (json/encode data))
    (process-file tmp-file)
    (finally
      (fs/delete tmp-file))))

;; Pattern 3: Delete on exit
(let [tmp-file (fs/create-temp-file)]
  (fs/delete-on-exit tmp-file)
  (spit tmp-file data)
  tmp-file)  ; File deleted when JVM exits
```

### Efficient Directory Processing

```clojure
;; Process large directories efficiently
(with-open [stream (fs/directory-stream "." "*.txt")]
  (doseq [path stream]
    (process-file path)))  ; Lazy processing, one at a time

;; Instead of realizing entire seq
(doseq [path (fs/list-dir "." "*.txt")]
  (process-file path))  ; Realizes all paths first
```

### Cross-Platform Path Construction

```clojure
;; Always use fs/path for joining - it handles separators
(fs/path "dir" "subdir" "file.txt")              ; Works everywhere

;; Don't manually concatenate with separators
;; BAD: (str "dir" "/" "subdir" "/" "file.txt")  ; Breaks on Windows

;; Convert Windows paths to Unix style when needed
(fs/unixify (fs/path "C:" "Users" "name"))       ; "C:/Users/name"
```

### File Filtering Pipeline Pattern

```clojure
;; Build reusable filters
(defn clojure-source? [path]
  (and (fs/regular-file? path)
       (re-find #"\.(clj|cljs|cljc)$" (str path))))

(defn recent? [days path]
  (let [cutoff (- (System/currentTimeMillis)
                  (* days 24 60 60 1000))]
    (> (fs/file-time->millis (fs/last-modified-time path)) cutoff)))

;; Compose filters
(->> (fs/glob "src" "**/*")
     (filter clojure-source?)
     (filter (partial recent? 7))
     (map str))
```

### Atomic File Operations

```clojure
;; Write to temp file, then move (atomic on most filesystems)
(let [target (fs/path "important-data.edn")
      tmp-file (fs/create-temp-file {:prefix ".tmp-"
                                       :suffix ".edn"
                                       :dir (fs/parent target)})]
  (try
    (spit tmp-file (pr-str data))
    (fs/move tmp-file target {:replace-existing true})
    (catch Exception e
      (fs/delete-if-exists tmp-file)
      (throw e))))
```

## Common Use Cases and Recipes

### Build Tool Tasks

```clojure
;; Clean target directory
(defn clean []
  (when (fs/exists? "target")
    (fs/delete-tree "target")))

;; Copy resources
(defn copy-resources []
  (fs/create-dirs "target/resources")
  (fs/copy-tree "resources" "target/resources"))

;; Find all source files
(defn source-files []
  (fs/glob "src" "**/*.clj"))
```

### File Backup

```clojure
(defn backup-file [path]
  (let [backup-name (str path ".backup."
                         (System/currentTimeMillis))]
    (fs/copy path backup-name)))

(defn backup-directory [dir dest]
  (let [timestamp (System/currentTimeMillis)
        backup-dir (fs/path dest (str (fs/file-name dir)
                                      "-" timestamp))]
    (fs/copy-tree dir backup-dir)))
```

### Log Rotation

```clojure
(defn rotate-logs [log-dir max-age-days]
  (let [cutoff (- (System/currentTimeMillis)
                  (* max-age-days 24 60 60 1000))]
    (->> (fs/glob log-dir "*.log")
         (filter #(< (fs/file-time->millis
                      (fs/last-modified-time %))
                     cutoff))
         (run! fs/delete))))
```

### File Synchronization

```clojure
(defn sync-newer-files [src dest]
  (doseq [src-file (fs/glob src "**/*")
          :when (fs/regular-file? src-file)]
    (let [rel-path (fs/relativize src src-file)
          dest-file (fs/path dest rel-path)]
      (when (or (not (fs/exists? dest-file))
                (> (fs/file-time->millis (fs/last-modified-time src-file))
                   (fs/file-time->millis (fs/last-modified-time dest-file))))
        (fs/create-dirs (fs/parent dest-file))
        (fs/copy src-file dest-file {:replace-existing true})
        (println "Synced:" src-file)))))
```

### Finding Duplicate Files

```clojure
(require '[clojure.java.io :as io])
(import '[java.security MessageDigest])

(defn file-hash [path]
  (with-open [is (io/input-stream (fs/file path))]
    (let [digest (MessageDigest/getInstance "MD5")
          buffer (byte-array 8192)]
      (loop []
        (let [n (.read is buffer)]
          (when (pos? n)
            (.update digest buffer 0 n)
            (recur))))
      (format "%032x" (BigInteger. 1 (.digest digest))))))

(defn find-duplicates [dir]
  (->> (fs/glob dir "**/*")
       (filter fs/regular-file?)
       (group-by file-hash)
       (filter #(> (count (val %)) 1))
       (map (fn [[hash paths]]
              {:hash hash
               :size (fs/size (first paths))
               :files (map str paths)}))))
```

## Error Handling and Edge Cases

```clojure
;; Handle missing files gracefully
(when (fs/exists? "config.edn")
  (process-config (slurp "config.edn")))

;; Or with try-catch
(try
  (process-file "data.txt")
  (catch java.nio.file.NoSuchFileException e
    (println "File not found:" (.getMessage e)))
  (catch java.nio.file.AccessDeniedException e
    (println "Access denied:" (.getMessage e))))

;; Check permissions before operations
(when (and (fs/exists? "file.txt")
           (fs/readable? "file.txt"))
  (slurp "file.txt"))

;; Handle walk errors
(fs/walk-file-tree "."
  {:visit-file-failed (fn [path ex]
                        (println "Cannot access:" path)
                        :continue)})  ; Continue despite errors
```

## Performance Tips

1. **Use directory-stream for large directories**: It's lazy and doesn't load all entries into memory
2. **Filter early**: Apply filters in glob patterns when possible rather than filtering in Clojure
3. **Avoid repeated file system calls**: Cache results like file-exists? checks
4. **Use walk-file-tree for deep recursion**: More efficient than recursive list-dir
5. **Batch operations**: Group multiple files when possible instead of individual operations

## Testing and Mocking

```clojure
;; Use with-temp-dir for tests
(deftest test-file-processing
  (fs/with-temp-dir [tmp-dir {}]
    (let [test-file (fs/path tmp-dir "test.txt")]
      (spit test-file "test data")
      (is (fs/exists? test-file))
      (is (= "test data" (slurp test-file)))
      ;; No cleanup needed - automatic
      )))
```

## Platform-Specific Considerations

### Windows
- Use `fs/unixify` to normalize paths for cross-platform code
- Hidden files require the hidden attribute, not just a leading dot
- POSIX permission functions won't work

### Unix/Linux/macOS
- Full POSIX permissions support
- XDG base directory functions available
- Hidden files start with dot
- Owner functions work

### General
- Always use `fs/path` to join paths - it handles separators correctly
- Test on target platforms when possible
- Use relative paths when portability matters

## Integration with Babashka Tasks

```clojure
;; In bb.edn
{:tasks
 {:requires ([babashka.fs :as fs])

  clean {:doc "Remove build artifacts"
         :task (fs/delete-tree "target")}

  test {:doc "Run tests"
        :task (do
                (doseq [test-file (fs/glob "test" "**/*_test.clj")]
                  (load-file (str test-file))))}

  build {:doc "Build project"
         :depends [clean]
         :task (do
                 (fs/create-dirs "target")
                 (println "Building..."))}}}
```

## Quick Reference: Most Common Functions

```clojure
;; Checking
(fs/exists? path)
(fs/directory? path)
(fs/regular-file? path)

;; Creating
(fs/create-dirs path)
(fs/create-file path)
(fs/create-temp-dir)

;; Reading/Writing
(slurp (fs/file path))
(spit (fs/file path) content)
(fs/read-all-lines path)
(fs/write-lines path lines)

;; Copying/Moving/Deleting
(fs/copy src dest)
(fs/copy-tree src dest)
(fs/move src dest)
(fs/delete path)
(fs/delete-tree path)

;; Finding
(fs/glob root "**/*.clj")
(fs/match root pattern {:recursive true})
(fs/list-dir dir)
(fs/which "executable")

;; Paths
(fs/path "dir" "file")
(fs/parent path)
(fs/file-name path)
(fs/extension path)
(fs/absolutize path)
(fs/relativize base target)
```

## Additional Resources

- [Official GitHub Repository](https://github.com/babashka/fs)
- [API Documentation](https://github.com/babashka/fs/blob/master/API.md)
- [Babashka Book](https://book.babashka.org/)
- [Java NIO.2 Path Documentation](https://docs.oracle.com/javase/tutorial/essential/io/fileio.html)

## Summary

The babashka.fs library provides a comprehensive, idiomatic Clojure interface for file system operations. Key strengths:

- **Cross-platform**: Handles OS differences automatically
- **Composable**: Functions work well together in pipelines
- **Efficient**: Built on NIO.2 for good performance
- **Practical**: Includes high-level functions for common tasks
- **Safe**: Provides options for atomic operations and error handling

When writing file system code in Clojure or Babashka, reach for babashka.fs first - it's likely to have exactly what you need with a clean, functional API.
