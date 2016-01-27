Sass Builder
============

Sass Builder is a SASS compiler that reads a config file (.sassbuilder-config) stored in a sass/scss source folder. It is a JSON file that sets .css output folder and SASS flags [cache, style, debug, line numbers, line comments].

The plugin works on post save of a .sass/.scss file in Sublime Text.

SassC Compatibility
===================

The fork [blitzrk/SassBuilder-SassC](https://github.com/blitzrk/SassBuilder-SassC) provides the `sassc` binary through a dependency on [blitzrk/sublime-sassc](https://github.com/blitzrk/sublime-sassc) and introduces the (default) option to use either the `sass` or `sassc` compiler.

Config
======

`project_path` has be added to this to allow for scanning in the entire project path when partials are saved.

* Automatically runs on save.
* Create .sassbuilder-config files with ease
  * Tools->Sass Builder Config
  * Ctrl+B + Ctrl+S keystroke
  * Right-click a folder or folders in the side bar.

`.sassbuilder-config.json`:

```json
{
    "project_path": "/project/path",
    "output_path": "/project/path/css",
	"compiler": "sassc"
    "options": {
        "cache":         true,
        "debug":         false,
        "line-comments": true,
        "line-numbers":  true,
        "style":         "nested"
    }
}
```
