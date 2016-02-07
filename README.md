# *****DEPRECATED***** 

Please check out [Libsass Build](https://github.com/blitzrk/sublime_libsass). It uses sassc exclusively and has **no external dependencies**!!! It is also listed in Package Control.

This was a useful experiment, which I will keep for reflection, but its ultimate contribution was informing how I went about building [Libsass Build](https://github.com/blitzrk/sublime_libsass) from scratch.

Use [Libsass Build](https://github.com/blitzrk/sublime_libsass).

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

Sass Builder
============

Sass Builder is a SASS compiler plugin for Sublime Text 2/3. It utilizes a per-directory config file `.sassbuilder-config.json`, which is stored in the sass/scss source directory, to set the .css output folder, SASS flags [cache, style, debug, line numbers, line comments], and compiler preference.

Sass Builder now supports both the externally installed `sass` Ruby front-end and the `sassc` C++ front-end. The latter doesn't require any outside dependencies and can run significantly faster, but you are (at the present time) more likely to encounter bugs in the implementation.

The plugin works on post save of a .sass/.scss file in Sublime Text. Future versions will utilize Sublime's own build system manager.

Config
======

`project_path` allows for scanning the entire project path for partials.

* Automatically runs on save.
* Create .sassbuilder-config files with ease
  * Tools->Sass Builder Config
  * Ctrl+B + Ctrl+S keystroke
  * Right-click a folder or folders in the side bar.

`.sassbuilder-config.json`:

```js
{
    "project_path": "/project/path",
    "output_path": "/project/path/css",
    "compiler": "sassc", // or "sass"
    "options": {
        "cache":         true,
        "debug":         false,
        "line-comments": true,
        "line-numbers":  true,
        "style":         "nested"
    }
}
```
