import sublime, sublime_plugin

import os

skeleton = '''{
	"project_path": "/path/to/scss",
	"output_path": "/path/to/css",
	"compiler": "sassc",
	"options": {
		"cache":         true,
		"debug":         true,
		"line-comments": true,
		"line-numbers":  true,
		"style":         "nested"
	}
}'''

class SassBuilderCreateCommand(sublime_plugin.WindowCommand):

	def run(self, paths=[]):
		if len(paths) != 0:
			for path in paths:
				if os.path.isdir(path):
					filename = os.path.join(path, '.sassbuilder-config.json')

					with open(filename, 'w+') as f:
						f.write(skeleton)

					view = self.window.open_file(filename)
		else:
			view = self.window.new_file()
			view.settings().set('default_dir', self.window.folders()[0])
			view.set_name('.sassbuilder-config.json')

			view.run_command('insert_snippet', {'contents': skeleton})
