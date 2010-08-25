from django.template import Node
from django.template.context import Context
from django.template.loader import get_template, select_template

class SugarNodeRenderError(Exception):
    pass


class SugarNode(Node):
    def __init__(self, pieces, function, template):
        self.pieces = pieces
        self.function = function
        self.template = template
    
    def render(self, context):
        args = []
        kwargs = {}
        for part, name, value in self.pieces:
            value = part.resolve(context, value)
            if name is None:
                args.append(value)
            else:
                kwargs[name] = value
                
        fn_return = self.function(context, *args, **kwargs)
        
        if self.template:
            if not isinstance(fn_return, dict):
                raise SugarNodeRenderError('render function must return dict if passing a template path to the tag (inclusion tag)')
            t = get_template(self.template)
            return t.nodelist.render(Context(fn_return))
        else:
            return fn_return